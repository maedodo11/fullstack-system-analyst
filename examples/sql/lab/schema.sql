PRAGMA foreign_keys = ON;
CREATE TABLE patients(id INTEGER PRIMARY KEY, name TEXT NOT NULL, city TEXT);
CREATE TABLE doctors(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE slots(id INTEGER PRIMARY KEY, doctor_id INTEGER NOT NULL REFERENCES doctors(id), starts_at TEXT NOT NULL, ends_at TEXT NOT NULL, published INTEGER NOT NULL CHECK(published IN (0,1)), CHECK(ends_at > starts_at));
CREATE TABLE appointments(id INTEGER PRIMARY KEY, slot_id INTEGER NOT NULL REFERENCES slots(id), patient_id INTEGER NOT NULL REFERENCES patients(id), status TEXT NOT NULL CHECK(status IN ('CONFIRMED','CANCELLED','COMPLETED','NO_SHOW')), created_at TEXT NOT NULL);
CREATE UNIQUE INDEX one_active_booking ON appointments(slot_id) WHERE status='CONFIRMED';
CREATE TABLE delivery_events(id INTEGER PRIMARY KEY, event_id TEXT NOT NULL, appointment_id INTEGER NOT NULL REFERENCES appointments(id), received_at TEXT NOT NULL);
