-- ============================================================
-- ORDER GENERATOR SERVICE ACCOUNT
-- ============================================================

GRANT USAGE ON SCHEMA generator
TO order_generator_svc;

-- Transactional tables: generator creates records
GRANT SELECT, INSERT ON
    generator.orders,
    generator.order_details,
    generator.payment_orders,
    generator.payment_status_history,
    generator.order_status_history
TO order_generator_svc;

-- Reference/source tables: generator only reads these
GRANT SELECT ON
    generator.customers,
    generator.products,
    generator.ref_tax_rates,
    generator.ref_shipping_rates
TO order_generator_svc;

-- Required for identity/sequence-backed inserts
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA generator
TO order_generator_svc;


-- ============================================================
-- PAYMENT PROCESSOR SERVICE ACCOUNT
-- ============================================================

GRANT USAGE ON SCHEMA generator
TO payment_processor_svc;

-- Payment processor reads and updates payment records
GRANT SELECT, UPDATE ON
    generator.payment_orders
TO payment_processor_svc;

-- Approved/failed payments can change order state
GRANT SELECT, UPDATE ON
    generator.orders
TO payment_processor_svc;

-- Payment state history
GRANT SELECT, INSERT, UPDATE ON
    generator.payment_status_history
TO payment_processor_svc;

-- Order state history
GRANT SELECT, INSERT, UPDATE ON
    generator.order_status_history
TO payment_processor_svc;

-- Required for identity/sequence-backed history inserts
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA generator
TO payment_processor_svc;