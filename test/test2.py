import psycopg
from psycopg.rows import dict_row
import os
import random

DB_PARAMS = {
    'dbname': os.getenv("DB_NAME", "mydatabase"),
    'user': os.getenv("DB_USER", "admin"),
    'password': os.getenv("DB_PASSWORD", "admin"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': int(os.getenv("DB_PORT", "5433"))
}
def retrieve_all_products():
    conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
    cur = conn.cursor()

    product_lists = cur.execute(
        "SELECT * FROM generator.products",
    ).fetchall()
    return(product_lists)

all_products = retrieve_all_products()
all_products_standard = [x for x in all_products if x['shipping_class'] == 'STANDARD']
all_products_large = [x for x in all_products if x['shipping_class'] == 'LARGE']
all_products_oversized = [x for x in all_products if x['shipping_class'] == 'OVERSIZED']

number_of_random_products = random.randint(1,5)
random_product_list = []
for x in range(number_of_random_products):
    weighted_number = random.randint(1,100)
    if weighted_number <=85:
        random_product_list.append(random.choice(all_products_standard))
    elif weighted_number <=95:
        random_product_list.append(random.choice(all_products_large))
    else:
        random_product_list.append(random.choice(all_products_oversized))

# random_product_list = [random.choice(all_products) for x in range(number_of_random_products)]

for x in random_product_list:
    print (x['product_id'], x['shipping_class'])



# print (len(all_products_standard))
# print (len(all_products_large))
# print (len(all_products_oversized))