# Решение 6. SQL-запросы

```sql
-- 1. Топ-5 городов по выручке за сентябрь
SELECT u.city, SUM(o.amount) AS revenue
FROM orders o JOIN users u ON u.id = o.user_id
WHERE o.status = 'paid'
  AND o.created_at >= DATE '2026-09-01' AND o.created_at < DATE '2026-10-01'
GROUP BY u.city ORDER BY revenue DESC LIMIT 5;

-- 2. Конверсия по городам
SELECT u.city,
       COUNT(DISTINCT u.id) AS users,
       COUNT(DISTINCT o.user_id) FILTER (WHERE o.status='paid') AS buyers,
       ROUND(100.0 * COUNT(DISTINCT o.user_id) FILTER (WHERE o.status='paid')
             / NULLIF(COUNT(DISTINCT u.id),0), 1) AS conv_pct
FROM users u LEFT JOIN orders o ON o.user_id = u.id
GROUP BY u.city;

-- 3. Скользящий средний чек по неделям
SELECT date_trunc('week', created_at) AS wk,
       AVG(AVG(amount)) OVER (ORDER BY date_trunc('week', created_at)
                              ROWS BETWEEN 3 PRECEDING AND CURRENT ROW) AS ma4
FROM orders WHERE status='paid' GROUP BY 1 ORDER BY 1;

-- 4a. LEFT JOIN ... IS NULL
SELECT u.id FROM users u
LEFT JOIN orders o ON o.user_id = u.id
  AND o.created_at >= now() - interval '90 days'
GROUP BY u.id HAVING COUNT(o.id) = 0;

-- 4b. NOT EXISTS (обычно лучше: анти-джойн, не раздувает строки)
SELECT u.id FROM users u
WHERE NOT EXISTS (SELECT 1 FROM orders o
                  WHERE o.user_id = u.id
                    AND o.created_at >= now() - interval '90 days');

-- 5. Ранжирование внутри города
SELECT *,
       RANK()       OVER (PARTITION BY city ORDER BY rev DESC) -- ties: равный ранг, следующий пропускается
     , DENSE_RANK() OVER (PARTITION BY city ORDER BY rev DESC) -- ties: равный ранг без пропусков
     , ROW_NUMBER() OVER (PARTITION BY city ORDER BY rev DESC) -- всегда уникален, tie-break недетерминирован
FROM per_user_rev;
```

Разбор: условие `o.status='paid'` при LEFT JOIN ставить в **ON**, а не в WHERE (в WHERE джойн превращается во inner join — классическая ошибка №1). Индекс под запрос 1: `orders(status, created_at) INCLUDE (user_id, amount)` или partial `WHERE status='paid'`. EXPLAIN — обязательная часть ответа: seq scan на 10 млн строк = пересмотреть индекс.
