# Решение 12. Витрина «загрузка врачей»

**Grain факта:** одна строка = одна запись на приём (appointment_sk), обновляемый accumulating snapshot. Визит/отмена/no-show — её взаимоисключающий текущий итог, а не дополнительные строки факта.

**Измерения:**
- dim_doctor(doctor_key SK, doctor_id, fio, specialty, clinic_id FK, valid_from, valid_to) — **SCD Type 2**: имя/специальность меняются, исторические отчёты не должны переписываться.
- dim_clinic(clinic_key, name, city, region)
- dim_date(date_key, day, week, month, is_holiday)
- dim_slot_time(time_key, start_time, duration_min)
- dim_patient_segment(age_band, gender, insurance_type) — обезличенно, без ФИО (privacy, см. кейс 7).

**Fact:**
```sql
CREATE TABLE fact_appointment (
  appointment_sk BIGINT PRIMARY KEY,
  date_key INT REFERENCES dim_date,
  doctor_key INT REFERENCES dim_doctor,
  clinic_key INT REFERENCES dim_clinic,
  time_key INT REFERENCES dim_slot_time,
  patient_segment_key INT REFERENCES dim_patient_segment,
  outcome SMALLINT CHECK (outcome IN (0,1,2,3)), -- booked/visited/cancelled/noshow
  actual_duration_min INT,          -- NULL для cancelled/noshow
  lead_time_days INT,               -- насколько заранее записались
  scheduled_duration_min INT      -- длительность забронированного слота; загрузка рассчитывается отдельно
);
```

**Late arrival (no-show помечается позже загрузки):** факт грузится идемпотентно по appointment_sk через MERGE/UPSERT: первичная загрузка — BOOKED/CANCELLED; апдейт outcomes приходит вторым потоком в окне 48 ч; отчёты за «сегодня» помечаются provisional до закрытия окна (SLA актуальности: окончательные данные — T+2). Альтернатива — accumulate snapshot с двумя датами (scheduled/outcome).

**Пример запроса (доля посещений и средняя длительность по закрытым записям):**
```sql
SELECT c.name, d.specialty,
       COUNT(*) FILTER (WHERE f.outcome=1)*1.0/COUNT(*) AS visit_rate,
       AVG(f.actual_duration_min) FILTER (WHERE f.outcome=1) AS avg_visit_min
FROM fact_appointment f
JOIN dim_clinic c USING (clinic_key)
JOIN dim_doctor d USING (doctor_key)
JOIN dim_date dt USING (date_key)
WHERE dt.day BETWEEN DATE '2026-09-01' AND DATE '2026-09-30'
  AND f.outcome IN (1,2,3) -- незавершённые записи исключаем
GROUP BY 1,2 ORDER BY visit_rate DESC;
```

Чеклист спецификации отчёта (модуль 11): grain, источник каждого поля, обработка NULL/late data, права доступа к сегментам, SLA свежести — всё это идёт в ТЗ на ETL, а не «разберёмся при сборке».

**О загрузке:** процент занятости врача за день = забронированные минуты / доступные минуты расписания ×100. Нужен отдельный факт доступности doctor_day; AVG процента на строках записей даст неправильное взвешивание. FK-фрагмент предполагает созданные dim-таблицы с первичными ключами.
