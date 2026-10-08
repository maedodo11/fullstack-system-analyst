SELECT event_id, COUNT(*) AS deliveries FROM delivery_events GROUP BY event_id HAVING COUNT(*)>1 ORDER BY event_id;
