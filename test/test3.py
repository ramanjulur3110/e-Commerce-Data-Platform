import psycopg
from psycopg.rows import dict_row
import random
import os

DB_PARAMS = {
    'dbname': os.getenv("DB_NAME", "mydatabase"),
    'user': os.getenv("DB_USER", "admin"),
    'password': os.getenv("DB_PASSWORD", "admin"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': int(os.getenv("DB_PORT", "5433"))
}
    
conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
cur = conn.cursor()
cur.execute("TRUNCATE TABLE generator.order_details, generator.orders, generator.payment_orders, generator.payment_orders_state_history RESTART IDENTITY;")
conn.commit()
cur.close()