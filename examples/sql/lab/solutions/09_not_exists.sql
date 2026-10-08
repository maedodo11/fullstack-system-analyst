SELECT p.id FROM patients p WHERE NOT EXISTS(SELECT 1 FROM appointments a WHERE a.patient_id=p.id AND a.status='CONFIRMED') ORDER BY p.id;
