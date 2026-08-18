import psycopg
from psycopg.rows import dict_row
import random
from datetime import datetime, timezone
from deactivated_python_files.obtain_all_customers import obtain_all_customers
from deactivated_python_files.obtain_all_products import obtain_all_products
import time

all_customers = obtain_all_customers()
all_products = obtain_all_products()

DB_PARAMS = {
    'dbname': "mydatabase", 
    'user': 'admin', 
    'password': 'admin', 
    'host': 'localhost',
    'port': 5433
}    

order_insert_tuple = []
order_details_insert_tuple_start = []
order_details_insert_tuple_final = []
number_insert = 0
update_dict = {}
for order_insert in range(10):
    number_of_random_products = random.randint(1,5)
    random_product_list = [random.choice(all_products) for x in range(number_of_random_products)]
    random_customer = random.choice(all_customers)
    order_timestamp = datetime.now(timezone.utc)

    total_amount = 0
    for x in random_product_list:
        if x['price'] <= 50:
            x['quantity'] = random.randint(1,5)
        else:
            x['quantity'] = 1
        total_amount += x['price'] * x['quantity']
    
    order_insert_tuple.append((random_customer['customer_id'], order_timestamp, 'PENDING', total_amount))

    for order_detail in range(len(order_insert_tuple)):    
        for i, x in enumerate(random_product_list):
            order_details_insert_tuple_start.append([number_insert, i+1, x['product_id'], x['quantity'], x['price']])
        number_insert += 1