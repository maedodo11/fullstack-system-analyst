# Модуль 11. Данные, интеграционные платформы и аналитика

Отчётность, витрины и потоки данных — частая часть задач системного аналитика в enterprise.

## Теория

### 1. OLTP vs OLAP
OLTP — транзакции (десятки строк за запрос, нормализовано). OLAP — аналитика (миллионы строк, денормализованные схемы). Аналитику нельзя требовать «сводный отчёт по всем заказам» с prod-OLTP без индексов/реплик — это деградация транзакционной системы.

### 2. Хранилище данных: подходы
- **Kimball (dimensional modeling)**: fact-таблицы + dimension, grain = строка факта. Пример: `fact_sales(order_id, product_key, date_key, qty, amount)`.
- **Inmon**: сначала нормализованное корпоративное хранилище → data marts.
SCD Type 2 для измерений, меняющих свойства: адрес клиента историзируется (`valid_from/valid_to/is_current`) — иначе «клиент из Москвы» превращается в «всегда был из Казани».

### 3. ETL vs ELT и инструменты
ETL (Transform до загрузки — Informatica, Airbyte+dbt hybrid) / ELT (сырьё в озеро → трансформации внутриwarehouse — dbt + ClickHouse/Snowflake). Оркестрация: Airflow DAG, зависимости, backfill, алерты на падение. Разбор: отчёт «выручка вчера» сходился с CRM — потому что два разных определения «оплаченного заказа» (CRM: статус paid; DWH: факт оплаты без учёта refunds). Лечение: единый metrics layer / каталог определений метрик (dbt docs, DataHub).

### 4. Потоковая обработка
CDC (Change Data Capture): Debezium читает WAL Postgres → топики Kafka с изменениями таблиц → real-time дашборды, репликация в search/ES. Требование аналитика: «данные в витрине не старше 5 минут» = CDC + streaming вместо ночного batch.

### 5. Качество данных (Data Quality)
Правила на ingestion: уникальность PK, referential integrity, диапазоны, полнота, свежесть. Метрики DQ: % строк с нарушениями, время обнаружения. Кейс: выгрузка из старой ERP с кодировкой cp1251 ломала UTF-8 пайплайн молча — битые ФИО попали в рассылку; фикс — схема-валидатор + dead-letter для бракованных строк.

### 6. Роли в данных
Data owner (бизнес-владелец), steward (качество), data engineer (пайплайны), аналитик (требования к витринам и отчётам). Спецификация отчёта аналитика включает: источник, grain, фильтры, формулы метрик, права доступа, расписание актуализации, SLA задержки.

## Ссылки
- The Data Warehouse Toolkit (Kimball) — конспект: https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/
- dbt docs: https://docs.getdbt.com/
- Debezium: https://debezium.io/documentation/
- Airflow concepts: https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html
- DataHub (каталог): https://datahubproject.io/docs/

## Практика
- [ ] Спроектируйте star-schema для отчёта « retention пользователей по когортам»: факты, измерения, grain.
- [ ] Опишите спецификацию отчёта «воронка оформления заказа» по всем пунктам раздела 6.
- [ ] Для требования «остатки на сайте ≤ 2 мин после продажи на складе» выберите паттерн интеграции и обоснуйте.

Задание 12 практикума: [tasks](../practice/tasks.md) · [разбор star-schema](../practice/solutions/sol12_star_schema.md) · мини-кейс 7 про ПДн: [разбор](../cases/case07_pii_request.md)
Дальше: [Модуль 12 — Процессы, Agile и инструменты](../12_process_agile_tools/README.md)
