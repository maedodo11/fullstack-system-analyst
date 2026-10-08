SELECT patient_id, COUNT(*) AS total FROM appointments GROUP BY patient_id HAVING COUNT(*)>=2 ORDER BY patient_id;
