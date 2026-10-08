# Решение 7. ER сервиса доставки

```plantuml
@startuml
entity Restaurant {
  *id PK
  name
  is_active
}
entity Category { *id PK; *restaurant_id FK; name; sort_order }
entity Dish { *id PK; *category_id FK; name; is_available }
entity DishOption { *id PK; *dish_id FK; name; price_delta }
entity DishPriceHistory {
  *dish_id FK
  *valid_from
  valid_to
  price
}
entity Customer { *id PK; name; phone }
entity Address { *id PK; *customer_id FK; line; slot_start; slot_end }
entity Order {
  *id PK
  *customer_id FK
  *address_id FK
  status
  total
}
entity OrderItem { *id PK; *order_id FK; *dish_id FK; qty; unit_price }
entity Courier { *id PK; name }
entity Delivery { *id PK; *order_id FK 1:1; *courier_id FK; eta; status }

Restaurant ||--o{ Category
Category ||--o{ Dish
Dish ||--o{ DishOption
Dish ||--o{ DishPriceHistory
Customer ||--o{ Address
Customer ||--o{ Order
Address ||--o{ Order
Order ||--|{ OrderItem
Dish ||--o{ OrderItem
Order ||--o| Delivery
Courier ||--o{ Delivery
@enduml
```

Ключевые решения:
- **OrderItem.unit_price** — снимок цены на момент заказа (неизменяем): пересчёт задним числом ломает чеки и бухгалтерию. История цен — DishPriceHistory (valid_from/valid_to), паттерн SCD2.
- **Order.address_id + snapshot-поля адреса** — адрес клиента мог измениться после заказа, аналогично.
- Category/DishOption здесь имеют самостоятельный id; FK задаёт владельца. Если имя должно быть уникально у родителя, добавьте UNIQUE(parent_id, name). OrderItem имеет собственный id, иначе PK только по order_id разрешил бы лишь одну позицию заказа.
- Delivery отдельно от Order: courier/eta меняются после создания заказа; связь 1:1, но свой жизненный цикл.
- Many-to-many dish↔option — через выбор в корзине (OrderItemOption при необходимости).
