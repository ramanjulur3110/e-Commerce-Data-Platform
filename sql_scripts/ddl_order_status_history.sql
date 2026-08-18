CREATE TABLE IF NOT EXISTS generator.order_status_history (
    order_status_history_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    order_id BIGINT NOT NULL REFERENCES generator.orders(order_id),
    order_status VARCHAR NOT NULL,
    effective_start_at  TIMESTAMPTZ NOT NULL,
    effective_end_at TIMESTAMPTZ,
    is_current BOOLEAN NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
)