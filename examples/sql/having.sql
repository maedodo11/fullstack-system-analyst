DROP TABLE IF EXISTS training_store_sales;
CREATE TABLE training_store_sales (
 id INTEGER PRIMARY KEY,
 city VARCHAR(100) NOT NULL,
 amount INTEGER NOT NULL,
 status VARCHAR(20) NOT NULL
);
INSERT INTO training_store_sales (id, city, amount, status) VALUES
 (1, 'Иркутск', 7000, 'paid'),
 (2, 'Иркутск', 8000, 'paid'),
 (3, 'Иркутск', 50000, 'cancelled'),
 (4, 'Казань', 12000, 'paid'),
 (5, 'Москва', 10000, 'paid'),
 (6, 'Новосибирск', 20000, 'pending');
SELECT city, SUM(amount) AS total_amount
FROM training_store_sales
WHERE status = 'paid'
GROUP BY city
HAVING SUM(amount) > 10000
ORDER BY total_amount DESC, city ASC;
