--
-- PostgreSQL database dump
--

\restrict Mx8QAqdBCbKSlwKMbBIHIp44R87zmkEFNy21mGdtzeUjlBdNsDIw70V4IMieWW0

-- Dumped from database version 17.10 (Debian 17.10-1.pgdg12+1)
-- Dumped by pg_dump version 17.10 (Debian 17.10-1.pgdg12+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: generator; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA generator;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: customers; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.customers (
    customer_id bigint NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    email character varying(255) NOT NULL,
    phone character varying(30),
    street_address character varying(255),
    city character varying(100),
    state character varying(100),
    postal_code character varying(20),
    country character varying(100) DEFAULT 'United States'::character varying NOT NULL,
    date_of_birth date,
    customer_since date DEFAULT CURRENT_DATE NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: customers_customer_id_seq; Type: SEQUENCE; Schema: generator; Owner: -
--

ALTER TABLE generator.customers ALTER COLUMN customer_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME generator.customers_customer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: order_details; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.order_details (
    order_detail_id bigint NOT NULL,
    order_id bigint NOT NULL,
    line_number integer NOT NULL,
    product_id bigint NOT NULL,
    quantity integer NOT NULL,
    unit_price numeric(10,2) NOT NULL,
    CONSTRAINT order_details_line_number_check CHECK ((line_number > 0)),
    CONSTRAINT order_details_quantity_check CHECK ((quantity > 0)),
    CONSTRAINT order_details_unit_price_check CHECK ((unit_price >= (0)::numeric))
);


--
-- Name: order_details_order_detail_id_seq; Type: SEQUENCE; Schema: generator; Owner: -
--

ALTER TABLE generator.order_details ALTER COLUMN order_detail_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME generator.order_details_order_detail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: order_status_history; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.order_status_history (
    order_status_history_id bigint NOT NULL,
    order_id bigint NOT NULL,
    order_status character varying NOT NULL,
    effective_start_at timestamp with time zone NOT NULL,
    effective_end_at timestamp with time zone,
    is_current boolean NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: order_status_history_order_status_history_id_seq; Type: SEQUENCE; Schema: generator; Owner: -
--

ALTER TABLE generator.order_status_history ALTER COLUMN order_status_history_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME generator.order_status_history_order_status_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: orders; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.orders (
    order_id bigint NOT NULL,
    customer_id bigint NOT NULL,
    order_date timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    order_status character varying(20) NOT NULL,
    subtotal numeric(12,2) NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT chk_orders_status CHECK (((order_status)::text = ANY ((ARRAY['PENDING'::character varying, 'PAYMENT PROCESSING'::character varying, 'PAID'::character varying, 'SHIPPED'::character varying, 'DELIVERED'::character varying, 'CANCELLED'::character varying])::text[]))),
    CONSTRAINT chk_orders_total CHECK ((subtotal >= (0)::numeric))
);


--
-- Name: orders_order_id_seq; Type: SEQUENCE; Schema: generator; Owner: -
--

ALTER TABLE generator.orders ALTER COLUMN order_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME generator.orders_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: payment_orders; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.payment_orders (
    payment_order_id bigint NOT NULL,
    order_id bigint NOT NULL,
    payment_type_id integer NOT NULL,
    payment_amount numeric(10,2) NOT NULL,
    payment_status character varying DEFAULT 'INITIATED'::character varying NOT NULL,
    failure_reason character varying,
    processed_at timestamp with time zone,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    attempts integer DEFAULT 0
);


--
-- Name: payment_orders_payment_order_id_seq; Type: SEQUENCE; Schema: generator; Owner: -
--

ALTER TABLE generator.payment_orders ALTER COLUMN payment_order_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME generator.payment_orders_payment_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: payment_status_history; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.payment_status_history (
    payment_state_history_id bigint NOT NULL,
    payment_order_id bigint NOT NULL,
    payment_status character varying DEFAULT 'INITIATED'::character varying NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    effective_start_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    effective_end_at timestamp with time zone,
    is_current boolean DEFAULT true NOT NULL
);


--
-- Name: payment_orders_state_history_payment_state_history_id_seq; Type: SEQUENCE; Schema: generator; Owner: -
--

ALTER TABLE generator.payment_status_history ALTER COLUMN payment_state_history_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME generator.payment_orders_state_history_payment_state_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: payment_type; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.payment_type (
    payment_type_id integer NOT NULL,
    payment_type character varying NOT NULL,
    is_active boolean NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: product_categories; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.product_categories (
    category_id bigint NOT NULL,
    category_name character varying(100) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: product_categories_category_id_seq; Type: SEQUENCE; Schema: generator; Owner: -
--

ALTER TABLE generator.product_categories ALTER COLUMN category_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME generator.product_categories_category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: product_subcategories; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.product_subcategories (
    subcategory_id bigint NOT NULL,
    category_id bigint NOT NULL,
    subcategory_name character varying(100) NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: product_subcategories_subcategory_id_seq; Type: SEQUENCE; Schema: generator; Owner: -
--

ALTER TABLE generator.product_subcategories ALTER COLUMN subcategory_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME generator.product_subcategories_subcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: products; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.products (
    product_id bigint NOT NULL,
    sku character varying(30) NOT NULL,
    product_name character varying(150) NOT NULL,
    category character varying(50) NOT NULL,
    subcategory character varying(75),
    brand character varying(100),
    price numeric(10,2) NOT NULL,
    cost numeric(10,2) NOT NULL,
    weight_lbs numeric(8,2),
    length_in numeric(8,2),
    width_in numeric(8,2),
    height_in numeric(8,2),
    shipping_class character varying(20) DEFAULT 'STANDARD'::character varying NOT NULL,
    stock_quantity integer DEFAULT 0 NOT NULL,
    is_active boolean DEFAULT true NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT products_cost_check CHECK ((cost >= (0)::numeric)),
    CONSTRAINT products_price_check CHECK ((price >= (0)::numeric)),
    CONSTRAINT products_shipping_class_check CHECK (((shipping_class)::text = ANY ((ARRAY['STANDARD'::character varying, 'LARGE'::character varying, 'OVERSIZED'::character varying])::text[]))),
    CONSTRAINT products_stock_quantity_check CHECK ((stock_quantity >= 0)),
    CONSTRAINT products_weight_check CHECK (((weight_lbs IS NULL) OR (weight_lbs >= (0)::numeric)))
);


--
-- Name: products_product_id_seq; Type: SEQUENCE; Schema: generator; Owner: -
--

ALTER TABLE generator.products ALTER COLUMN product_id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME generator.products_product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: ref_shipping_rates; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.ref_shipping_rates (
    shipping_class character varying(20) NOT NULL,
    shipping_cost numeric(10,2) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: ref_tax_rates; Type: TABLE; Schema: generator; Owner: -
--

CREATE TABLE generator.ref_tax_rates (
    state_code character varying(2) NOT NULL,
    state_name character varying NOT NULL,
    tax_rate numeric(5,4) NOT NULL,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


--
-- Name: customers customers_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.customers
    ADD CONSTRAINT customers_pkey PRIMARY KEY (customer_id);


--
-- Name: order_details order_details_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.order_details
    ADD CONSTRAINT order_details_pkey PRIMARY KEY (order_detail_id);


--
-- Name: order_status_history order_status_history_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.order_status_history
    ADD CONSTRAINT order_status_history_pkey PRIMARY KEY (order_status_history_id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);


--
-- Name: payment_orders payment_orders_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.payment_orders
    ADD CONSTRAINT payment_orders_pkey PRIMARY KEY (payment_order_id);


--
-- Name: payment_status_history payment_orders_state_history_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.payment_status_history
    ADD CONSTRAINT payment_orders_state_history_pkey PRIMARY KEY (payment_state_history_id);


--
-- Name: payment_type payment_type_payment_type_key; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.payment_type
    ADD CONSTRAINT payment_type_payment_type_key UNIQUE (payment_type);


--
-- Name: payment_type payment_type_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.payment_type
    ADD CONSTRAINT payment_type_pkey PRIMARY KEY (payment_type_id);


--
-- Name: product_categories product_categories_name_key; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.product_categories
    ADD CONSTRAINT product_categories_name_key UNIQUE (category_name);


--
-- Name: product_categories product_categories_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.product_categories
    ADD CONSTRAINT product_categories_pkey PRIMARY KEY (category_id);


--
-- Name: product_subcategories product_subcategories_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.product_subcategories
    ADD CONSTRAINT product_subcategories_pkey PRIMARY KEY (subcategory_id);


--
-- Name: product_subcategories product_subcategories_unique; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.product_subcategories
    ADD CONSTRAINT product_subcategories_unique UNIQUE (category_id, subcategory_name);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (product_id);


--
-- Name: products products_sku_key; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.products
    ADD CONSTRAINT products_sku_key UNIQUE (sku);


--
-- Name: ref_shipping_rates ref_shipping_rates_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.ref_shipping_rates
    ADD CONSTRAINT ref_shipping_rates_pkey PRIMARY KEY (shipping_class);


--
-- Name: ref_tax_rates ref_tax_rates_pkey; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.ref_tax_rates
    ADD CONSTRAINT ref_tax_rates_pkey PRIMARY KEY (state_code);


--
-- Name: ref_tax_rates ref_tax_rates_state_name_key; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.ref_tax_rates
    ADD CONSTRAINT ref_tax_rates_state_name_key UNIQUE (state_name);


--
-- Name: order_details uq_order_line; Type: CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.order_details
    ADD CONSTRAINT uq_order_line UNIQUE (order_id, line_number);


--
-- Name: order_details fk_order_details_order; Type: FK CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.order_details
    ADD CONSTRAINT fk_order_details_order FOREIGN KEY (order_id) REFERENCES generator.orders(order_id);


--
-- Name: orders fk_orders_customer; Type: FK CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.orders
    ADD CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) REFERENCES generator.customers(customer_id);


--
-- Name: order_status_history order_status_history_order_id_fkey; Type: FK CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.order_status_history
    ADD CONSTRAINT order_status_history_order_id_fkey FOREIGN KEY (order_id) REFERENCES generator.orders(order_id);


--
-- Name: payment_orders payment_orders_order_id_fkey; Type: FK CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.payment_orders
    ADD CONSTRAINT payment_orders_order_id_fkey FOREIGN KEY (order_id) REFERENCES generator.orders(order_id);


--
-- Name: payment_orders payment_orders_payment_type_id_fkey; Type: FK CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.payment_orders
    ADD CONSTRAINT payment_orders_payment_type_id_fkey FOREIGN KEY (payment_type_id) REFERENCES generator.payment_type(payment_type_id);


--
-- Name: payment_status_history payment_orders_state_history_payment_order_id_fkey; Type: FK CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.payment_status_history
    ADD CONSTRAINT payment_orders_state_history_payment_order_id_fkey FOREIGN KEY (payment_order_id) REFERENCES generator.payment_orders(payment_order_id);


--
-- Name: product_subcategories product_subcategories_category_fk; Type: FK CONSTRAINT; Schema: generator; Owner: -
--

ALTER TABLE ONLY generator.product_subcategories
    ADD CONSTRAINT product_subcategories_category_fk FOREIGN KEY (category_id) REFERENCES generator.product_categories(category_id);


--
-- PostgreSQL database dump complete
--

\unrestrict Mx8QAqdBCbKSlwKMbBIHIp44R87zmkEFNy21mGdtzeUjlBdNsDIw70V4IMieWW0

