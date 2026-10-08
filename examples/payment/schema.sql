-- PostgreSQL 17+; illustrative DDL, not a production migration.
CREATE TABLE orders (
 order_id text PRIMARY KEY,
 customer_id text NOT NULL,
 amount_minor bigint NOT NULL CHECK (amount_minor > 0),
 currency char(3) NOT NULL CHECK (currency = 'RUB'),
 status text NOT NULL CHECK (status IN ('UNPAID', 'PAID', 'CANCELLED'))
);
CREATE TABLE payments (
 payment_id text PRIMARY KEY,
 order_id text NOT NULL REFERENCES orders(order_id),
 customer_id text NOT NULL,
 operation text NOT NULL DEFAULT 'FULL_PAYMENT' CHECK (operation = 'FULL_PAYMENT'),
 idempotency_key text NOT NULL,
 request_hash text NOT NULL,
 amount_minor bigint NOT NULL CHECK (amount_minor > 0),
 currency char(3) NOT NULL CHECK (currency = 'RUB'),
 status text NOT NULL CHECK (status IN ('PENDING','UNKNOWN','SUCCESS','FAILED','CANCELLED')),
 provider_operation_id text UNIQUE,
 created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE (customer_id, operation, idempotency_key)
);
CREATE UNIQUE INDEX one_active_payment ON payments(order_id)
 WHERE status IN ('PENDING','UNKNOWN');
CREATE UNIQUE INDEX one_successful_payment ON payments(order_id)
 WHERE status = 'SUCCESS';
CREATE TABLE payment_inbox (
 provider text NOT NULL,
 event_id text NOT NULL,
 payload jsonb NOT NULL,
 processed_at timestamptz,
 PRIMARY KEY (provider, event_id)
);
CREATE TABLE outbox (
 event_id text PRIMARY KEY,
 aggregate_id text NOT NULL,
 event_type text NOT NULL,
 payload jsonb NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now(),
 published_at timestamptz
);
-- Application transaction: lock order; verify owner and amount; create payment.
-- Result transaction: verify allowed transition; update payment + order + outbox.
-- Relay can publish an event twice; consumers must deduplicate by event_id.
