# Решение 3. Sequence-диаграмма оформления заказа

```plantuml
@startuml
autonumber
actor Покупатель as P
participant "Сайт (SPA)" as W
participant "Order Service" as O
participant "Payment Service" as PS
participant "Stock Service" as ST
queue "Kafka" as K
participant "Notification" as N
database "PostgreSQL" as DB

P -> W: нажать "Оформить заказ"
W -> O: POST /orders (Idempotency-Key)
O -> ST: POST /reserve (sync, timeout 500ms)
alt недостаточно на складе
  ST --> O: 409 OUT_OF_STOCK
  O --> W: 409 + список недоступных позиций
else резерв ок
  O -> DB: INSERT order(status=CREATED)
  O --> W: 201 {orderId}
  W -> PS: открыть форму оплаты
  PS --> W: callback payment.succeeded (redirect)
  alt платёж отклонён
    PS --> W: declined
    W -> O: POST /orders/{id}/cancel
    O -> ST: release reservation (sync)
    O -> K: order.cancelled
  else платёж успешен
    O -> PS: GET /payments/{id} (server-side verify!)
    O -> DB: UPDATE status=PAID
    O -> K: publish order.paid (outbox)
    K -> N: consume order.paid
    N --> P: email/SMS подтверждение
  end
end
@enduml
```

Ключевые моменты разбора:
- Резерв склада **до** оплаты (иначе платят за отсутствующий товар), с TTL резерва.
- Результат оплаты проверяется серверно (`GET /payments`), а не «пришёл redirect → значит ок» (подделываемый callback).
- Notification — async через очередь: медленное письмо не блокирует заказ.
- Idempotency-Key на POST /orders — защита от двойного клика.
