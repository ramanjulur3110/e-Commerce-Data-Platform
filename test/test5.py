import psycopg
from psycopg.rows import dict_row
from datetime import datetime, timezone
import os

DB_PARAMS = {
    'dbname': os.getenv("DB_NAME", "mydatabase"),
    'user': os.getenv("DB_USER", "admin"),
    'password': os.getenv("DB_PASSWORD", "admin"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': int(os.getenv("DB_PORT", "5433"))
}

def update_order_status_history(current_status, new_status):
    conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
    cur = conn.cursor()
    order_list = cur.execute(f"SELECT * FROM generator.order_status_history WHERE order_status = '{current_status}'").fetchall()

    insert_into_order_list = []
    insert_into_order_tuple = []
    for x in order_list:
        insert_into_order_list.append(x['order_id'])
        insert_into_order_tuple.append((x['order_id'], new_status, datetime.now(timezone.utc), True))
    placeholders = ', '.join(['%s'] * len(insert_into_order_list))

    query = f"UPDATE generator.order_status_history SET effective_end_at = CURRENT_TIMESTAMP, is_current = FALSE WHERE order_id IN ({placeholders})"
    cur.execute(query, tuple(insert_into_order_list))

    query = "INSERT INTO generator.order_status_history (order_id, order_status, effective_start_at, is_current) VALUES (%s, %s, %s, %s)"
    cur.executemany(query, insert_into_order_tuple)
    conn.commit()

update_order_status_history('PAID', 'SCHEDULED')