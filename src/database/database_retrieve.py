import psycopg
from psycopg.rows import dict_row
import os

DB_PARAMS = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def truncate_prod_tables():
    conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE generator.order_details, generator.orders, generator.payment_orders, generator.order_status_history, generator.payment_status_history RESTART IDENTITY;")
    conn.commit()
    cur.close()
    # print ("Tables Truncated")

def retrieve_all_customers():
    conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
    cur = conn.cursor()

    customer_results = cur.execute(
        "SELECT * FROM generator.customers",
    ).fetchall()
    return customer_results

def retrieve_all_products():
    conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
    cur = conn.cursor()

    product_lists = cur.execute(
        "SELECT * FROM generator.products",
    ).fetchall()
    return(product_lists)