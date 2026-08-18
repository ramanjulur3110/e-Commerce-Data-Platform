import psycopg
from psycopg.rows import dict_row
from datetime import datetime, timezone
import random
import os

DB_PARAMS = {
    'dbname': os.getenv("DB_NAME", "mydatabase"),
    'user': os.getenv("DB_USER", "admin"),
    'password': os.getenv("DB_PASSWORD", "admin"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': int(os.getenv("DB_PORT", "5433"))
}

def order_generator_inserts(batch_metadata):
    conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
    cur = conn.cursor()
    #1. Insert data into generator.orders
    query = "INSERT INTO generator.orders(customer_id, order_date, order_status, subtotal) VALUES (%s, %s, %s, %s) RETURNING order_id"
    cur.executemany(query, batch_metadata['order_insert_tuple'], returning=True)

    insert_into_order_tuple = []
    list_of_generated_order_numbers = []
    insert_row_num = 0
    while True:
        row = cur.fetchone()
        if row:
            batch_metadata['update_dict'][insert_row_num] = row["order_id"]
            # batch_metadata['list_of_generated_order_numbers'].append(row["order_id"])
            list_of_generated_order_numbers.append(row["order_id"])
            insert_into_order_tuple.append((row["order_id"], 'PENDING', datetime.now(timezone.utc), True ))
        if not cur.nextset():
            break
        insert_row_num +=1 

    for x in batch_metadata['order_details_insert_tuple_start']:
        if x[0] in batch_metadata['update_dict']:
            x[0] = batch_metadata['update_dict'][x[0]]
        batch_metadata['order_details_insert_tuple_final'].append(tuple(x))

    #2. Insert data into generator.order_details
    query = "INSERT INTO generator.order_details(order_id, line_number, product_id, quantity, unit_price) VALUES (%s, %s, %s, %s, %s)"
    cur.executemany(query, batch_metadata['order_details_insert_tuple_final'])

    #3. Insert data into generator.payment_status_history
    query = "INSERT INTO generator.order_status_history(order_id, order_status, effective_start_at, is_current) VALUES (%s, %s, %s, %s)"
    cur.executemany(query, insert_into_order_tuple)

    placeholders = ", ".join(["%s"] * len(list_of_generated_order_numbers))
    order_list = cur.execute(
        f"""
        with order_shipping_class as(
        select 
        od.order_id, 
        p.shipping_class,
        sr.shipping_cost,
        CASE
            WHEN p.shipping_class = 'STANDARD' then 3
            WHEN p.shipping_class = 'LARGE' then 2
            WHEN p.shipping_class = 'OVERSIZED' then 1
        END as shipping_class_numeric
        from generator.order_details od
        LEFT JOIN generator.products p
            on od.product_id = p.product_id
        LEFT JOIN generator.ref_shipping_rates sr
            on p.shipping_class = sr.shipping_class
        ), 
        order_shipping_cost as(
        select DISTINCT order_id, shipping_class, shipping_cost
            from (
                    select 
                    *,
                    RANK() over (PARTITION BY order_id ORDER BY shipping_class_numeric ASC) as shipping_rank
                    from order_shipping_class
                ) as sub_query
            where shipping_rank = 1
        )

        SELECT 
            o.*, 
            c.state, 
            tx.tax_rate, 
            sc.shipping_class, 
            sc.shipping_cost,
            ROUND(o.subtotal + (o.subtotal * tx.tax_rate) + sc.shipping_cost, 2) as total_amount
        FROM generator.orders o
        LEFT JOIN order_shipping_cost sc
            on sc.order_id = o.order_id
        LEFT JOIN generator.customers c
            on c.customer_id = o.customer_id
        LEFT JOIN generator.ref_tax_rates tx
            on tx.state_name = c.state
        WHERE o.order_id in ({placeholders})
        """,
        list_of_generated_order_numbers
    ).fetchall()

    order_insert_tuple = []
    random_processor_number = ''
    for x in order_list:
        random_number = random.randint(1,100)
        if random_number > 98:
            random_processor_number = 10
        elif random_number > 95:
            random_processor_number = 9
        elif random_number > 91:
            random_processor_number = 8
        elif random_number > 82:
            random_processor_number = 7
        elif random_number > 68:
            random_processor_number = 6
        elif random_number > 50: 
            random_processor_number = 5
        elif random_number > 46:
            random_processor_number = 4
        elif random_number > 39:
            random_processor_number = 3
        elif random_number > 22:
            random_processor_number = 2
        else:
            random_processor_number = 1
        order_insert_tuple.append((x['order_id'], random_processor_number, x['total_amount']))

    #4. Insert data into generator.payment_orders
    query = "INSERT INTO generator.payment_orders(order_id, payment_type_id, payment_amount) VALUES (%s, %s, %s) RETURNING payment_order_id"
    cur.executemany(query, order_insert_tuple, returning=True)

    payment_order_id_list =[]
    while True:
        row = cur.fetchone()
        if row:
            payment_order_id_list.append((row["payment_order_id"],))
        if not cur.nextset():
            break

    #5. Insert data into generator.order_status_history
    query = "INSERT INTO generator.payment_status_history(payment_order_id) VALUES (%s)"
    cur.executemany(query, payment_order_id_list)

    # Commit changes to the database. 
    conn.commit()



# def insert_into_payment_orders_and_payment_orders_state_history(batch_metadata):
#     placeholders = ", ".join(["%s"] * len(batch_metadata['list_of_generated_order_numbers']))
#     conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
#     cur = conn.cursor()
#     order_list = cur.execute(
#         f"""
#         with order_shipping_class as(
#         select 
#         od.order_id, 
#         p.shipping_class,
#         sr.shipping_cost,
#         CASE
#             WHEN p.shipping_class = 'STANDARD' then 3
#             WHEN p.shipping_class = 'LARGE' then 2
#             WHEN p.shipping_class = 'OVERSIZED' then 1
#         END as shipping_class_numeric
#         from generator.order_details od
#         LEFT JOIN generator.products p
#             on od.product_id = p.product_id
#         LEFT JOIN generator.ref_shipping_rates sr
#             on p.shipping_class = sr.shipping_class
#         ), 
#         order_shipping_cost as(
#         select DISTINCT order_id, shipping_class, shipping_cost
#             from (
#                     select 
#                     *,
#                     RANK() over (PARTITION BY order_id ORDER BY shipping_class_numeric ASC) as shipping_rank
#                     from order_shipping_class
#                 ) as sub_query
#             where shipping_rank = 1
#         )

#         SELECT 
#             o.*, 
#             c.state, 
#             tx.tax_rate, 
#             sc.shipping_class, 
#             sc.shipping_cost,
#             ROUND(o.subtotal + (o.subtotal * tx.tax_rate) + sc.shipping_cost, 2) as total_amount
#         FROM generator.orders o
#         LEFT JOIN order_shipping_cost sc
#             on sc.order_id = o.order_id
#         LEFT JOIN generator.customers c
#             on c.customer_id = o.customer_id
#         LEFT JOIN generator.ref_tax_rates tx
#             on tx.state_name = c.state
#         WHERE o.order_id in ({placeholders})
#         """,
#         batch_metadata['list_of_generated_order_numbers']
#     ).fetchall()

#     order_insert_tuple = []
#     random_processor_number = ''
#     for x in order_list:
#         random_number = random.randint(1,100)
#         if random_number > 98:
#             random_processor_number = 10
#         elif random_number > 95:
#             random_processor_number = 9
#         elif random_number > 91:
#             random_processor_number = 8
#         elif random_number > 82:
#             random_processor_number = 7
#         elif random_number > 68:
#             random_processor_number = 6
#         elif random_number > 50: 
#             random_processor_number = 5
#         elif random_number > 46:
#             random_processor_number = 4
#         elif random_number > 39:
#             random_processor_number = 3
#         elif random_number > 22:
#             random_processor_number = 2
#         else:
#             random_processor_number = 1
#         order_insert_tuple.append((x['order_id'], random_processor_number, x['total_amount']))

#     query = "INSERT INTO generator.payment_orders(order_id, payment_type_id, payment_amount) VALUES (%s, %s, %s) RETURNING payment_order_id"
#     cur.executemany(query, order_insert_tuple, returning=True)

#     payment_order_id_list =[]
#     while True:
#         row = cur.fetchone()
#         if row:
#             payment_order_id_list.append((row["payment_order_id"],))
#         if not cur.nextset():
#             break

#     query = "INSERT INTO generator.payment_orders_state_history(payment_order_id) VALUES (%s)"
#     cur.executemany(query, payment_order_id_list)
#     conn.commit()
    

