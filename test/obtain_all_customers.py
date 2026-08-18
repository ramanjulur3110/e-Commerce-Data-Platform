import psycopg
from psycopg.rows import dict_row
import random
from datetime import datetime, timezone

DB_PARAMS = {
    'dbname': "mydatabase", 
    'user': 'admin', 
    'password': 'admin', 
    'host': 'localhost',
    'port': 5433
}    
conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
cur = conn.cursor()

customer_results = cur.execute(
    "SELECT * FROM generator.customers",
).fetchall()
print (customer_results[random.randint(1, len(customer_results))])