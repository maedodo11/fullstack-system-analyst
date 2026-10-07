# Модуль 10. Backend-практики

Что происходит на сервере и как это описывать в требованиях: код, паттерны, производительность.

## Теория

### 1. Анатомия HTTP-запроса на бэкенде (Spring Boot пример)
```java
@RestController @RequestMapping("/v1/orders")
class OrderController(orders: OrderService) {
  @PostMapping
  ResponseEntity<OrderDto> create(@Valid @RequestBody CreateOrderReq req,
                                  @RequestHeader("Idempotency-Key") UUID key) {
    var created = orders.create(req.toCommand(key));   // command → service → repo
    return ResponseEntity.created(location(created.id())).body(OrderDto.from(created));
  }
}
```
Слои: controller (валидация формы запроса) → service (бизнес-правила, транзакция `@Transactional`) → repository (доступ к данным). Аналитик требует DTO-контракты вместо сущностей БД — иначе схема протекает в API.

### 2. Паттерны, важные для спецификаций
- **Dependency Injection** — конфигурируемость, тестируемость.
- **Repository/Unit of Work** — абстракция хранилища.
- **CQRS/Saga/Outbox** — см. модуль архитектуры и курс микросервисов.
- **Retry + Backoff + Jitter** — повтор с экспоненциальной задержкой; без jitter клиенты синхронно «стучат» в восстановившийся сервис (thundering herd). Разбор инцидента: после отключения провайдера ретраи 500 клиентов каждые 1с уронили его повторно.

### 3. Конкурентность простыми словами
Тред-пул ограничивает параллельность: 200 потоков × блокирующий JDBC = потолок пропускной способности. Пул соединений к БД = 10 → при p99 запроса 500 мс максимум ~20 RPS на инстанс. Аналитик может посчитать ёмкость сервиса из NFR и заложить в требования масштабирование.

### 4. Логирование и трассировка требований
Структурированные логи (JSON), correlation-id на весь путь запроса, уровни DEBUG/INFO/WARN/ERROR, запрет PII в логах. Требование аналитика: «по номеру заявления найти все шаги обработки» = correlation id во всех сервисах + централизованный лог (ELK/Loki).

### 5. Кешение на бэкенде
Cache-aside (промах → БД → запись в Redis TTL), invalidate по событию изменения. Проблема протухания: кеш остатков TTL 60с при распродаже → oversell. Решение для критичных данных: не кеш, а атомарное списание (`UPDATE ... WHERE stock >= n`).

### 6. Идемпотентность и exactly-once иллюзии
Гарантия доставки usually at-least-once → дедупликация на потребителе (idempotency table / unique constraint). Разбор: платёж прошёл один раз, webhook доставлен трижды, баланс пополнен трижды — нет ключа идемпотентности `payment_id` в обработчике.

## Ссылки
- Spring docs: https://docs.spring.io/spring-framework/reference/
- Google SRE — retry budgets: https://sre.google/workbook/handling-overload/
- Exponential backoff & jitter (AWS): https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/
- 12-factor app: https://12factor.net/

## Практика
- [ ] Опишите обработку «создание перевода» слоями: валидации каждого слоя, где транзакция, что в DTO ответа при ошибке лимита.
- [ ] Посчитайте нужное число реплик сервиса: p95 200 мс, 800 RPS, пул БД 10 коннектов на под.
- [ ] Составьте требования к correlation-id и формату логов для сквозного поиска по заявке.

Задание 11 практикума + мини-кейсы 2–3: [конкурентность](../cases/case02_double_booking.md), [дубли webhook](../cases/case03_duplicate_webhook.md), [разбор инцидента](../practice/solutions/sol11_incident.md)
Дальше: [Модуль 11 — Данные и аналитика](../11_data_engineering/README.md)
