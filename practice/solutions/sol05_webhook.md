# Решение 5. Контракт webhook `order.updated`

**Payload (CloudEvents):**
```json
{
  "specversion": "1.0",
  "id": "evt_01H...",
  "type": "com.example.order.updated.v1",
  "source": "/orders",
  "time": "2026-10-07T14:03:11Z",
  "datacontenttype": "application/json",
  "data": { "order_id": "ord_123", "status": "PAID", "updated_fields": ["status"] }
}
```
(`id` — стабильный идентификатор события, НЕ id попытки доставки)

Headers: `X-Webhook-Signature: t=1696680191,v1=<hex hmac_sha256(secret, t + "." + body)>`, `User-Agent`, `X-Delivery-Attempt`.

**Подпись:** HMAC с секретом клиента; сверка timing-safe сравнением; принимать timestamp ±5 мин (replay protection). Секрет per-client, ротация через dual-secret период.

**Ретраи при недоступности получателя:** backoff 1m, 5m, 30m, 2h, 6h, 24h (at-least-once). После исчерпа — пометить endpoint «failing», деактивировать через N часов, показать в dashboard + уведомить. Хранение неотправленных — 7 дней, ручной replay.

**Защита получателя (прописать в документации!):** идемпотентность по `event.id` (processed_events UNIQUE), tolerant reader (дополнительные поля допускаются по контракту; неизвестный тип события явно маршрутизируется или отклоняется, обязательные поля проверяются), отвечать 2xx быстро (<5 с), тяжёлую обработку — в свою очередь.

**Версионирование:** major в типе (`order.updated.v1`); additive-поля без смены версии; breaking = новый type + параллельная доставка 6 мес.

**НЕ кладём:** данные карт, токены, ПИИ сверх минимума — webhook как «пинг» (thin event), получатель дотянет детали по REST по `order_id`. Причина: payload копируется в логи партнёров, контроль утечки потерян.

**Метрики поставщика:** delivery success rate, latency p95, retries per endpoint, signature failures (индикатор атаки/утечки секрета).
