# Глоссарий: EN → RU для системного аналитика

Термины, которые встречаются в документации, вакансиях и собеседованиях на английском.

## Требования и анализ

| English | Русский | Комментарий |
|---|---|---|
| stakeholder | заинтересованное лицо | в официальных документах — не «стейкхолдер» |
| requirement elicitation | выявление требований | техника сбора требований |
| acceptance criteria (AC) | критерии приёмки | Gherkin: Given/When/Then |
| user story | пользовательская история | «Как X, я хочу Y, чтобы Z» |
| definition of ready (DoR) | готовность к разработке | чеклист перед взятием в спринт |
| definition of done (DoD) | определение завершённости | критерии приёмки задачи командой |
| EARS (Easy Approach to Requirements Syntax) | формальный шаблон формулировки требований | 5 шаблонов: Ubiquitous / When / While / If / Where, см. модуль 1 |
| SPIDR | паттерн декомпозиции эпиков | Spike · Paths · Interfaces · Data · Rules; исследование, пути, интерфейсы, данные, правила |
| MoSCoW | приоритизация требований | Must / Should / Could / Won't this time |
| Kano model | классификация ожиданий пользователя | базовые / линейные / wow-свойства |
| design constraint | ограничение проектирования | не путать с NFR: «только managed Postgres», 152-ФЗ |
| change control | управление изменениями требований | request → impact analysis → решение → baseline |
| requirements volatility | волатильность требований | метрика доли изменённых требований после baseline |
| Dreyfus model of skill acquisition | модель уровня мастерства экспертов | подсказка, как интервьюировать: спрашивать про конкретные случаи, а не правила |
| backlog refinement / grooming | уточнение бэклога | регулярная проработка задач |
| traceability matrix | матрица трассировки | цепочка BR → UR → дизайн → тест |
| out of scope | вне рамок проекта | всегда фиксируйте в спецификации |
| as-is / to-be | как есть / как должно быть | текущий и целевой процесс |

## Архитектура и интеграции

| English | Русский | Комментарий |
|---|---|---|
| single point of failure (SPOF) | единая точка отказа | устраняется репликацией |
| coupling / cohesion | связанность / сплочённость | low coupling, high cohesion |
| bottleneck | узкое место | ограничение производительности |
| idempotency | идемпотентность | повтор запроса безопасен |
| rate limiting | ограничение частоты запросов | ответ 429 Too Many Requests |
| circuit breaker | автоматический выключатель | состояния closed/open/half-open |
| fallback | резервный путь обработки | что делаем при отказе зависимости |
| contract testing | контрактное тестирование | Pact: соглашение consumer↔provider |
| payload | полезная нагрузка | тело запроса/сообщения |
| endpoint | конечная точка | URL операции API |
| reverse proxy | обратный прокси | так работает API Gateway |
| service mesh | сервисная сетка | Istio/Linkerd: sidecar-прокси |
| eventual consistency | согласованность в конечном счёте | BASE вместо ACID |
| orchestration / choreography | оркестрация / хореография | два стиля координации Saga |
| compensation | компенсирующая операция | отмена шага саги |

## Данные

| English | Русский | Комментарий |
|---|---|---|
| primary / foreign key | первичный / внешний ключ | PK/FK |
| normalization | нормализация | 1NF–3NF; denormalization — избыточность ради скорости |
| index | индекс | ускоряет чтение, замедляет запись |
| query plan | план запроса | смотреть через EXPLAIN ANALYZE |
| sharding | шардирование | горизонтальное разбиение данных |
| replication lag | задержка репликации | причина stale reads из реплики |
| CDC (change data capture) | захват изменений данных | Debezium, binlog |
| ETL / ELT | извлечение-преобразование-загрузка | T vs L: где происходит преобразование |
| star schema | схема «звезда» | fact-таблица + dimension-таблицы |
| cardinality | кардинальность связи | 1:1, 1:N, M:N в ER-модели |
| soft delete | мягкое удаление | флаг is_deleted вместо DELETE |
| migration | миграция схемы БД | стратегия expand-contract |

## Безопасность

| English | Русский | Комментарий |
|---|---|---|
| authentication / authorization | аутентификация / авторизация | «кто ты» / «что тебе можно» |
| token leakage | утечка токена | не хранить JWT в localStorage бездумно |
| brute force | перебор паролей | защита: rate limit, lockout |
| privilege escalation | повышение привилегий | IDOR → доступ к чужим данным |
| encryption at rest / in transit | шифрование при хранении / передаче | TLS — это in transit |
| salted hash | хеш с солью | пароли: bcrypt/argon2 |
| audit log | журнал аудита | кто, когда, что изменил |
| threat modeling | моделирование угроз | метод STRIDE |
| least privilege | минимальные привилегии | роль получает ровно необходимый доступ |

## DevOps и качество

| English | Русский | Комментарий |
|---|---|---|
| rolling / blue-green / canary deployment | последовательный / сине-зелёный / канареечный выкат | стратегии деплоя |
| rollback | откат | возврат предыдущей версии |
| feature flag | флаг функции | включение фичи без деплоя |
| observability | наблюдаемость | метрики + логи + трейсы |
| SLO / SLA / error budget | цель / соглашение / бюджет ошибок | 99.9% ≈ 43 мин downtime/мес |
| flaky test | нестабильный («плавающий») тест | зависит от окружения, не от кода |
| staging environment | предпродажный стенд | pre-prod |
| CI / CD | непрерывная интеграция / доставка | pipeline: build → test → deploy |
| incident / blameless postmortem | инцидент / разбор без поиска виноватых | культура после сбоев |
| technical debt | технический долг | осознанные упрощения с ценой |

## Фронтенд и веб

| English | Русский | Комментарий |
|---|---|---|
| SPA / SSR / SSG | одностраничное приложение / серверный рендеринг / статическая генерация | выбор влияет на SEO и TTFB |
| hydration | гидратация | оживление SSR-HTML джаваскриптом |
| CORS | политика межсетевого происхождения (Cross-Origin Resource Sharing) | preflight OPTIONS-запрос |
| cache invalidation | инвалидация кеша | Cache-Control, ETag |
| debounce / throttle | дебаунс / троттлинг | оптимизация частых событий |
| accessibility (a11y) | доступность | WCAG, скринридеры |
| Core Web Vitals | ключевые показатели веба | LCP, INP, CLS |

## Процессы

| English | Русский | Комментарий |
|---|---|---|
| kickoff | стартовая встреча | старт проекта |
| sign-off | формальное согласование | утверждение документа |
| follow-up | последующие шаги | итоги встречи |
| one-pager | одностраничник | краткая сводка |
| proof of concept (PoC) | подтверждение концепции | проверка гипотезы, не продукт |
| MVP | минимально жизнеспособный продукт | первая полезная версия |
| RACI | матрица ответственности | Responsible/Accountable/Consulted/Informed |
| onboarding | ввод в должность | адаптация сотрудника/клиента |
| handover / knowledge transfer | передача / передача знаний | финал этапа поддержки |
| estimation | оценка трудозатрат | planning poker, story points |

---
← [Оглавление курса](README.md) · [Прогресс-трекер](progress.md) · [Вопросы собеседований](interview.md)
