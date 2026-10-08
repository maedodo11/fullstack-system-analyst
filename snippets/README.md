# Snippets — готовые куски для спецификаций

Копипаст для аналитика: шаблоны формулировок, типовые контракты и чеклисты. Подставьте имена сущностей и используйте в спецификациях ФТ (шаблон — [templates/spec-ft.md](../templates/spec-ft.md)).

## 1. Формулировки NFR (без воды, с цифрами)

```markdown
**Производительность.** P95 времени ответа `POST /api/v1/orders` ≤ 300 мс при нагрузке
200 rps (замер на стенде pre-prod, тест k6 — см. модуль 8).

**Доступность.** API расчёта тарифов: SLO 99.9% за месяц (бюджет ошибок ≈ 43 мин).
Допустима деградация: отдавать последний актуальный тариф (stale ≤ 5 мин) при
недоступности сервиса котировок.

**Масштабируемость.** Рост базы пользователей ×3 без изменения схемы БД; горизонтальное
масштабирование stateless-сервисов (HPA при CPU > 70%).

**Безопасность.** Все внешние вызовы только по TLS 1.2+; секреты — только из vault;
PII не попадает в логи (маскирование по маске документа).

**Восстановление.** RPO ≤ 15 мин (репликация WAL), RTO ≤ 1 ч (автовосстановление из
бэкапа, учебный drill раз в квартал).
```

Разбор: каждая строка содержит **метрику + условие измерения + следствие**. Требование должно быть объективно проверяемым; не всегда нужна цифра: «токены не записываются в логи» проверяется аудитом. Для производительности нужны числовые пороги (модуль 1).

## 2. Критерии приёмки: Gherkin с краевыми случаями

```gherkin
Feature: Оформление заказа с промокодом

  Background:
    Given пользователь "anna" авторизован
    And в корзине заказ на 1000 руб

  Scenario: Валидный промокод на 10%
    When применяет промокод "SALE10"
    Then итоговая сумма 900 руб
    And промокод помечен использованным

  Scenario Outline: Невалидные промокоды
    Given EXPIRED10 просрочен, USED10 уже использован, пустой код недопустим
    When применяет промокод "<code>"
    Then ошибка "<error>" с HTTP 422
    And сумма осталась 1000 руб

    Examples:
      | code        | error                  |
      | EXPIRED10   | PROMOCODE_EXPIRED      |
      | USED10      | PROMOCODE_USED         |
      | ""          | PROMOCODE_REQUIRED     |
      | hax'));--   | PROMOCODE_INVALID      |
```

Разбор: `Scenario Outline` + таблица = компактное покрытие краевых случаев; пустое значение и инъекция — обязательные проверки «грязных» входов (модуль 7).

## 3. Идемпотентный POST (паттерн заголовка)

```http
POST /api/v1/payments HTTP/1.1
Idempotency-Key: 7f9c1e2a-...-uuid
Content-Type: application/json

{"order_id": 42, "amount": 90000, "currency": "RUB"}
```

Семантика для спецификации:
- первый запрос → 201, ответ кешируется под ключом на 24 ч;
- повтор с тем же ключом и тем же телом → тот же 201 из кеша (side-effect НЕ повторяется);
- повтор с тем же ключом, но другим телом → 409 `IDEMPOTENCY_CONFLICT` (выбранная семантика курса).

Когда требовать: любой POST с деньгами, списаниями, отправкой SMS/email (модуль 3).

## 4. OpenAPI-фрагмент: пагинация + единая схема ошибок

```yaml
components:
  parameters:
    Page:
      in: query
      name: page
      schema: { type: integer, minimum: 1, default: 1 }
    PageSize:
      in: query
      name: page_size
      schema: { type: integer, minimum: 1, maximum: 100, default: 20 }
  schemas:
    Error:
      required: [code, message, request_id]
      properties:
        code:       { type: string, example: VALIDATION_FAILED }
        message:    { type: string, example: "Поле 'email' не является адресом" }
        request_id: { type: string, description: correlation-id для поиска в логах }
        details:
          type: array
          items:
            type: object
            properties:
              field:   { type: string }
              reason:  { type: string }
```

Правило: единая схема ошибки во всём API — фронт пишет один обработчик, поддержка — один поиск по `request_id` (correlation-id — модуль 10).

## 5. SQL-шаблоны для ТЗ на отчёты

```sql
-- PostgreSQL: оплаченные суммы, копейки -> рубли, календарные дни UTC.
-- Возвраты здесь не учитываются: метрика gross, не net revenue.
WITH calendar AS (
  SELECT generate_series(
    (now() AT TIME ZONE 'UTC')::date - 89,
    (now() AT TIME ZONE 'UTC')::date,
    interval '1 day')::date AS d
), daily AS (
  SELECT (created_at AT TIME ZONE 'UTC')::date AS d,
         sum(amount)/100.0 AS revenue
  FROM orders
  WHERE status = 'PAID'
    AND created_at >= ((now() AT TIME ZONE 'UTC')::date - 89) AT TIME ZONE 'UTC'
  GROUP BY 1
), filled AS (
  SELECT c.d, coalesce(d.revenue, 0) AS revenue
  FROM calendar c LEFT JOIN daily d ON d.d = c.d
)
SELECT d, revenue,
       avg(revenue) OVER (ORDER BY d ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS ma7
FROM filled ORDER BY d;
-- Первые 6 строк имеют неполное окно; для полного окна загрузите ещё 6 дней истории.

-- Дедупликация событий при at-least-once доставке (загрузка в DWH)
SELECT * FROM (
  SELECT *, row_number() OVER (PARTITION BY event_id ORDER BY ingested_at DESC) rn
  FROM stg.payments_events
) t WHERE rn = 1;
```

Разбор: второй запрос — обязательный слой защиты при CDC/Kafka-загрузке: at-least-once допускает дубли; повтор не должен повторять бизнес-эффект. Конфликт одинакового event_id с разным содержимым требует расследования (модуль 11).

## 6. Чеклист ревью интеграционного контракта (перед sign-off)

- [ ] Версионирование пути (`/v1`) или заголовка — что выбрано и почему
- [ ] Пагинация: параметр, максимум страницы, поведение при удалении элемента посреди листания
- [ ] Идемпотентность всех write-операций
- [ ] Коды ошибок: машинный `code` + человекочитаемое `message` + `request_id`
- [ ] Таймауты и retry-политика потребителя (не больше бюджета провайдера!)
- [ ] Лимиты размера payload и rate limit (429 + Retry-After)
- [ ] Nullable-поля помечены; enum расширяется безопасно (unknown value → graceful)
- [ ] Владелец breaking change-процесса и длительность deprecation-периода

## 7. PATCH / partial update (merge-patch)

```http
PATCH /api/v1/users/42
Content-Type: application/merge-patch+json

{"phone": "+7-900-000-00-00", "newsletter": null}
```

Семантика для спецификации: `null` = удалить поле, отсутствие ключа = не менять. Отдельно зафиксировать, какие поля PATCH-доступны какой роли (admin vs сам пользователь) — иначе получите mass assignment (OWASP, модуль 6).

---
Инструменты курса: [templates/](../templates/) · [practice/tasks.md](../practice/tasks.md) · [GLOSSARY.md](../GLOSSARY.md)

**Перед копированием:** согласуйте коды статусов и имя заголовка с целевым API. В этом курсе стандартный учебный заголовок — Idempotency-Key; X-Idempotency-Key допустим как отдельная договорённость. Учебные TTL и нагрузка не являются готовыми настройками продакшна.
