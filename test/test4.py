import psycopg
from psycopg.rows import dict_row
import random
import os
# SELECT * FROM generator.orders WHERE order_status = 'PENDING' ;

DB_PARAMS = {
    'dbname': os.getenv("DB_NAME", "mydatabase"),
    'user': os.getenv("DB_USER", "admin"),
    'password': os.getenv("DB_PASSWORD", "admin"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': int(os.getenv("DB_PORT", "5433"))
}

conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
cur = conn.cursor()
cur.execute("TRUNCATE TABLE generator.order_status_history RESTART IDENTITY;")
conn.commit()
cur.close()

conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
cur = conn.cursor()

order_list = cur.execute(
    """
    SELECT * FROM generator.orders WHERE order_status = 'PENDING' ;
    """
).fetchall()

insert_into_order_tuple = []
for x in order_list:
    insert_into_order_tuple.append((x['order_id'], x['order_status'], x['order_date'], True))

query = "INSERT INTO generator.order_status_history(order_id, order_status, effective_start_at, is_current) VALUES (%s, %s, %s, %s)"
cur.executemany(query, insert_into_order_tuple)
conn.commit()