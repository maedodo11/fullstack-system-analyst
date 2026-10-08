WITH ranked AS (SELECT id,event_id,ROW_NUMBER() OVER(PARTITION BY event_id ORDER BY received_at DESC,id DESC) AS rn FROM delivery_events) SELECT id,event_id FROM ranked WHERE rn=1 ORDER BY event_id;
