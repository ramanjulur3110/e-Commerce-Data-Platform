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

product_lists = conn.execute(
    "SELECT * FROM generator.products",
).fetchall()

# print (product_lists)
number_of_random_products = random.randint(1,5)
random_product_list = [random.choice(product_lists) for x in range(number_of_random_products)]

for x in random_product_list:
    if x['price'] <= 50:
        x['quantity'] = random.randint(1,4)
    else:
        x['quantity'] = 1

for x in random_product_list:
    print (x)