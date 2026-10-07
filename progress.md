# Трекер прогресса

Отмечайте `[x]` пройденные пункты. Курс рассчитан на ~10–12 недель по 4–6 часов в неделю.

## Маршруты

**Маршрут A — быстрый онбординг (2 недели, для вошедших в роль SA):**
1 → 2 → 3 → 5 → 6 → 12

**Маршрут B — полный (8–10 недель):** все модули по порядку + итоговый проект.

**Маршрут C — микросервисный трек:** B + бонус-курс `course/` (уроки 1–13).

## Чеклист

### Модули

- [ ] **01 Требования и аналитика** — BR/UR/FR/NFR, INVEST, Gherkin, трассировка · Практика: ☐ · Мини-кейс: ☐
- [ ] **02 UML и BPMN** — Use Case, Sequence, State Machine, ER, BPMN · Практика: ☐ · Мини-кейс: ☐
- [ ] **03 Интеграции и API** — REST/gRPC/GraphQL, OpenAPI, идемпотентность, webhooks · Практика: ☐ · Мини-кейс: ☐
- [ ] **04 Базы данных и SQL** — нормализация, SQL, индексы, NoSQL, миграции · Практика: ☐ · Мини-кейс: ☐
- [ ] **05 Архитектура** — стили, SLA, CAP/BASE, Saga/CQRS/Outbox, ADR · Практика: ☐ · Мини-кейс: ☐
- [ ] **06 Безопасность** — OAuth2/PKCE, JWT, RBAC, OWASP, STRIDE · Практика: ☐ · Мини-кейс: ☐
- [ ] **07 Тестирование** — пирамида, BDD, контракты, метрики · Практика: ☐ · Мини-кейс: ☐
- [ ] **08 DevOps и CI/CD** — pipeline, canary/blue-green, K8s, алерты · Практика: ☐ · Мини-кейс: ☐
- [ ] **09 Frontend и веб** — SPA/SSR, CORS/keши, Web Vitals, a11y · Практика: ☐ · Мини-кейс: ☐
- [ ] **10 Backend-практики** — слои, retry/jitter, конкурентность, кеши · Практика: ☐ · Мини-кейс: ☐
- [ ] **11 Данные и аналитика** — star-schema, ETL/ELT, CDC, data quality · Практика: ☐ · Мини-кейс: ☐
- [ ] **12 Процессы и Agile** — роли, DoR/DoD, тулинг, оценка · Практика: ☐ · Мини-кейс: ☐

### Бонус-курс микросервисов (`course/`, маршрут C)

- [ ] Уроки 1–4 (границы, коммуникация sync/async)
- [ ] Уроки 5–8 (gateway, discovery, данные, Saga)
- [ ] Уроки 9–13 (отказоустойчивость, наблюдаемость, деплой, миграция, «когда не надо»)

### AI-модуль

- [ ] **13 AI-assisted analysis** (`modules_extra/13_ai_assisted_analysis/`) — промпты для аналитика, спецификации через LLM, границы применения

### Практикум

- [ ] Задания практикума (`practice/`) — 12 задач
- [ ] Сверка с решениями (`practice/solutions/`)

### Шаблоны (использовать в работе)

- [ ] Спецификация ФТ · [templates/spec-ft.md](templates/spec-ft.md)
- [ ] ADR · [templates/adr.md](templates/adr.md)
- [ ] Контракт интеграции · [templates/integration-contract.md](templates/integration-contract.md)
- [ ] NFR-чеклист · [templates/nfr-checklist.md](templates/nfr-checklist.md)
- [ ] Threat model · [templates/threat-model.md](templates/threat-model.md)
- [ ] Декомпозиция и оценка · [templates/decomposition-estimation.md](templates/decomposition-estimation.md)

### Итоговый зачётный проект

Домен: «сервис записи к врачу». Пакет артефактов — см. README.

- [ ] 1. Иерархия требований BR → UR → FR/NFR с метриками
- [ ] 2. Use Case + 2 sequence + state machine + BPMN
- [ ] 3. OpenAPI-контракт с идемпотентностью + схема событий
- [ ] 4. Модель данных PostgreSQL + обоснование индексов
- [ ] 5. ADR: стиль архитектуры и брокер + расчёт SLA цепочки
- [ ] 6. Threat model + матрица RBAC
- [ ] 7. План тестирования + нагрузочный сценарий
- [ ] 8. Pipeline релиза с feature flag
- [ ] 9. Спецификация виджета записи (состояния, WCAG AA)
- [ ] 10. Витрина star-schema + SLA актуальности
- [ ] 11. DoR/DoD команды + декомпозиция

### Дополнительно

- [ ] Пройти мини-кейсы с разборами (`cases/`)
