SELECT p.id, COUNT(a.id) AS total FROM patients p LEFT JOIN appointments a ON a.patient_id=p.id GROUP BY p.id ORDER BY p.id;
