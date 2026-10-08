# Кейс 5. Миграция БД без простоя

## Ситуация

Нужно переименовать колонку `appointments.doc_id` → `doctor_id` и сделать `NOT NULL`, на проде, PostgreSQL, сервис 24/7. Dev предлагает: «ALTER TABLE RENAME COLUMN + ALTER SET NOT NULL одним скриптом, downtime 5 минут в 3 ночи».

## Ваш ход

Оцените предложение и напишите корректный план. Учтите: старый и новый код крутится одновременно во время rolling update.

<details>
<summary>Открыть разбор после своего решения</summary>

## Разбор

**Почему план дева опасен:**
- `SET NOT NULL` на большой таблице = полное сканирование (долгая блокировка записи);
- после RENAME все инстансы старой версии кода падают (колонки нет);
- незапланированный простой против SLA.

**Expand-Contract (шаги = отдельные релизы):**

1. **Expand:** `ALTER TABLE appointments ADD COLUMN doctor_id bigint;` (nullable). Приложение пишет в обе колонки. Бэкфилл пачками:
   ```sql
   UPDATE appointments SET doctor_id = doc_id
   WHERE doctor_id IS NULL AND id BETWEEN :lo AND :hi; -- окнами по 10k строк
   ```
2. **Переключение чтения:** новый код читает `doctor_id`; пишем в обе. Индекс — `CREATE INDEX CONCURRENTLY`.
3. **Constraint безопасно:**
   ```sql
   ALTER TABLE appointments ADD CONSTRAINT nn_doctor CHECK (doctor_id IS NOT NULL) NOT VALID;
   ALTER TABLE appointments VALIDATE CONSTRAINT nn_doctor; -- не блокирует запись
   ALTER TABLE appointments ALTER COLUMN doctor_id SET NOT NULL; -- теперь быстро
   ```
4. **Contract/drop:** удалить `doc_id`, когда весь трафик на новом коде и мониторинг показал: чтений старой колонки нет.

Откат на шагах 1–3 = просто откатить деплой кода, схема совместима с обеими версиями.

**Правило для команды:** миграция, ломающая совместимость, существует только как финальный шаг отдельного релиза.

**Типичные ошибки SA:** забыть про одновременную работу двух версий кода; бэкфилл одним UPDATE на миллион строк (long transaction → bloating); не назначить проверку «обе колонки равны» перед drop.


</details>

**Проверка вашего решения:** перечислены факты и неизвестное; указаны ответственный, наблюдаемый эффект, сценарий отказа и способ проверки. Допущения не выдаются за факты проекта.
