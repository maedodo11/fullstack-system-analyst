# Курс: Микросервисная архитектура

Полный курс с теорией, разбором примеров и схемами.

## Программа

| Модуль | Тема |
|---|---|
| 1 | [Введение: монолит vs микросервисы](lessons/01_intro_monolith_vs_microservices.md) |
| 2 | [Границы сервисов и Domain-Driven Design](lessons/02_service_boundaries_ddd.md) |
| 3 | [Синхронная коммуникация: REST и gRPC](lessons/03_sync_communication.md) |
| 4 | [Асинхронная коммуникация: брокеры сообщений](lessons/04_async_messaging.md) |
| 5 | [API Gateway](lessons/05_api_gateway.md) |
| 6 | [Service Discovery и балансировка нагрузки](lessons/06_service_discovery.md) |
| 7 | [Управление данными: Database per Service, CQRS, Event Sourcing](lessons/07_data_management.md) |
| 8 | [Распределённые транзакции: Saga](lessons/08_saga.md) |
| 9 | [Отказоустойчивость: Circuit Breaker, Retry, Timeout, Bulkhead](lessons/09_resilience.md) |
| 10 | [Наблюдаемость: логи, метрики, трейсинг](lessons/10_observability.md) |
| 11 | [Развёртывание: Docker, Kubernetes, CI/CD](lessons/11_deployment.md) |
| 12 | [Миграция от монолита: Strangler Fig](lessons/12_migration_strangler_fig.md) |
| 13 | [Когда НЕ нужны микросервисы + итоговый проект](lessons/13_when_not_and_final_project.md) |

Все схемы находятся в папке `images/`.

## Как работать с уроками

Это углубление после [базового маршрута](../START_HERE.md). У каждого урока есть самопроверка; переносите решение на [сквозную оплату](../examples/payment/README.md). Проверяйте не только счастливый путь, но и timeout, повтор и восстановление. Числа и размеры команд — примеры, не универсальные пороги.
