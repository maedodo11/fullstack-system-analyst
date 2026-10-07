# Модуль 4. Асинхронная коммуникация: брокеры сообщений

## 4.1. Два стиля обмена

- **Queue (точка-точка)**: сообщение потребляется ровно одним консьюмером. RabbitMQ (классика), AWS SQS.
- **Pub/Sub (тема/топик)**: одно событие получают все подписчики. Kafka, Redis Streams, SNS+SQS, Google Pub/Sub.

Для микросервисов — событийный стиль почти всегда pub/sub: `OrderPlaced` интересен одновременно складу, аналитике, нотификациям.

## 4.2. Kafka vs RabbitMQ — короткий разбор

| Критерий | Kafka | RabbitMQ |
|---|---|---|
| Модель | журнал (log), consumer читает по offset | очередь, сообщение удаляется после ack |
| Повторное чтение истории | ✅ (retention) | ❌ |
| Throughput | сотни тыс. msg/s | десятки тыс. msg/s |
| Routing-гибкость (headers, topics exchange) | примитивнее | богаче |
| Типичное применение | event sourcing, аналитика, шина событий | задачи, RPC-подобные очереди, work queues |

## 4.3. Формат события

```json
{
  "event_id": "e-9f2c...",
  "type": "shop.order.Placed.v1",
  "occurred_at": "2026-10-07T18:30:00Z",
  "producer": "order-service",
  "aggregate_id": "order-1042",
  "data": {
    "user_id": "u-7",
    "total": 4990,
    "currency": "RUB",
    "items": [{"sku": "A-1", "qty": 2}]
  }
}
```

Правила:
- **Тонкие события** (только ключевые поля) предпочтительнее толстых: меньше утечки внутренней модели. Толстые — когда потребителю прямо нужны данные и нельзя ходить обратно в API.
- Версия в имени типа (`...Placed.v1`). Новый формат — новая тема/тип, старый период сосуществует.
- Idempotency key (`event_id`) обязателен: доставка — «at least once».

## 4.4. Гарантии доставки

- **At most once** — потеря допустима (метрики).
- **At least once** — стандарт Kafka/Rabbit при корректных ack; возможны дубли ⇒ консьюмеры идемпотентны.
- **Exactly once** — лишь иллюзия в распределённых системах; достигается связкой at-least-once + идемпотентная обработка + транзакционный outbox.

### Идемпотентный консьюмер (пример)

```python
def handle(event):
    if seen_before(event["event_id"]):   # запись в таблицу processed_events
        return COMMIT                    # ACK без повторной обработки
    do_business_logic(event)
    mark_processed(event["event_id"])
```

## 4.5. Transactional Outbox — главная проблема интеграции

Сервис пишет заказ в БД и публикует событие в Kafka. Это две разные системы — классическая двухфазная рассылка ненадёжна (упал между commit и publish).

Решение — **Outbox**: событие пишется в таблицу `outbox` в той же ACID-транзакции, что и бизнес-данные; отдельный релей (debezium/canal или self-made poller) отправляет в брокер и помечает отправленным.

```sql
BEGIN;
INSERT INTO orders(id,status) VALUES('o-1','PLACED');
INSERT INTO outbox(id,type,payload) VALUES('e-1','OrderPlaced','{...}');
COMMIT;
-- relay: SELECT ... FROM outbox WHERE sent_at IS NULL FOR UPDATE SKIP LOCKED
```

## 4.6. Dead Letter Queue

Консьюмер не может обработать сообщение (баг, невалидные данные) → после N попыток уходит в DLQ. Оператор разбирается, переотправляет. Без DLQ ядовитые сообщения зацикливают консьюмера.

## 4.7. Schema Registry и эволюция схем

Kafka + Confluent Schema Registry (Avro/Protobuf/JSON Schema): совместимость схем проверяется на publish (backward/forward compatibility). Лечит главную боль событийных систем — молчаливо ломающиеся контракты.

**Дальше → [Модуль 5. API Gateway](05_api_gateway.md)**
