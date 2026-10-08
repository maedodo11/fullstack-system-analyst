# Решение 6. SQL без неоднозначных метрик

[Задания](../tasks.md) · [Запускаемая лаборатория](../../examples/sql/lab/README.md) · [Оценивание](../assessment.md)

Ниже PostgreSQL 17, таблицы из задания. `created_at` — timestamptz, `amount` — NUMERIC в одной валюте. Сентябрь 2026 считается в UTC; reference time для 90 дней — 2026-10-01T00:00:00Z. Это отдельный пример магазина: локальный месяц клиники из SQL-лаборатории сюда не переносится.

```sql
-- 1. Топ городов по сумме оплаченных заказов, созданных в сентябре.
-- Это учебное определение выручки; для финансового отчёта нужны дата оплаты и возвраты.
SELECT u.city, SUM(o.amount) AS revenue
FROM orders o JOIN users u ON u.id=o.user_id
WHERE o.status='paid'
  AND o.created_at >= TIMESTAMPTZ '2026-09-01 00:00:00+00'
  AND o.created_at < TIMESTAMPTZ '2026-10-01 00:00:00+00'
GROUP BY u.city ORDER BY revenue DESC, u.city NULLS LAST LIMIT 5;

-- 2. Доля зарегистрированных до конца сентября пользователей с >=1 paid-заказом
-- сентября; дата регистрации внутри сентября не исключает пользователя.
WITH conversion AS (
 SELECT u.city, COUNT(*) AS users,
        COUNT(*) FILTER (WHERE EXISTS (
          SELECT 1 FROM orders o WHERE o.user_id=u.id AND o.status='paid'
            AND o.created_at >= TIMESTAMPTZ '2026-09-01 00:00:00+00'
            AND o.created_at < TIMESTAMPTZ '2026-10-01 00:00:00+00')) AS buyers
 FROM users u WHERE u.created_at < TIMESTAMPTZ '2026-10-01 00:00:00+00'
 GROUP BY u.city
)
SELECT city, users, buyers, ROUND(100.0 * buyers / NULLIF(users,0),1) AS conversion_pct
FROM conversion ORDER BY city NULLS LAST;

-- 3. Средний чек за текущую и три предыдущие календарные недели.
-- Генерируем также пустые недели: ROWS не должен перепрыгивать календарные пробелы.
WITH weeks AS (
  SELECT generate_series(DATE '2026-08-10', DATE '2026-09-28', INTERVAL '1 week')::date AS wk
), agg AS (
  SELECT w.wk, COALESCE(SUM(o.amount),0) AS revenue, COUNT(o.id) AS n
  FROM weeks w LEFT JOIN orders o ON o.status='paid'
    AND o.created_at >= (w.wk::timestamp AT TIME ZONE 'UTC')
    AND o.created_at < ((w.wk+7)::timestamp AT TIME ZONE 'UTC')
  GROUP BY w.wk
), rolling AS (
  SELECT wk, SUM(revenue) OVER win / NULLIF(SUM(n) OVER win,0) AS avg_check_4w
  FROM agg WINDOW win AS (ORDER BY wk ROWS BETWEEN 3 PRECEDING AND CURRENT ROW)
)
SELECT * FROM rolling WHERE wk >= DATE '2026-08-31' ORDER BY wk;

-- 4a. Нет ни одного заказа любого статуса за фиксированные последние 90 дней.
SELECT u.id FROM users u LEFT JOIN orders o ON o.user_id=u.id
 AND o.created_at >= TIMESTAMPTZ '2026-10-01 00:00:00+00' - INTERVAL '90 days'
 AND o.created_at < TIMESTAMPTZ '2026-10-01 00:00:00+00'
WHERE o.id IS NULL ORDER BY u.id;

-- 4b. Эквивалентный NOT EXISTS; лучший план определяется на целевых данных.
SELECT u.id FROM users u WHERE NOT EXISTS (
 SELECT 1 FROM orders o WHERE o.user_id=u.id
 AND o.created_at >= TIMESTAMPTZ '2026-10-01 00:00:00+00' - INTERVAL '90 days'
 AND o.created_at < TIMESTAMPTZ '2026-10-01 00:00:00+00') ORDER BY u.id;

-- 5. Все пользователи; сумма оплаченных заказов за всю историю.
WITH per_user_rev AS (
 SELECT u.id,u.city,COALESCE(SUM(o.amount),0) AS rev FROM users u
 LEFT JOIN orders o ON o.user_id=u.id AND o.status='paid' GROUP BY u.id,u.city
)
SELECT id,city,rev,
 ROW_NUMBER() OVER(PARTITION BY city ORDER BY rev DESC,id) AS row_num,
 RANK() OVER(PARTITION BY city ORDER BY rev DESC) AS rank_num,
 DENSE_RANK() OVER(PARTITION BY city ORDER BY rev DESC) AS dense_rank_num
FROM per_user_rev ORDER BY city NULLS LAST, rev DESC,id;
```

Среднее недельных средних отличается от среднего чека всех заказов четырёх недель: второй показатель требует суммы денег / числа заказов. Для ROW_NUMBER нужен детерминированный tie-breaker; добавление id в RANK устранило бы смысл ничьей. NULL-города образуют отдельную группу. План сравнивают по фактическим строкам, чтениям и времени; seq scan сам по себе не ошибка.
