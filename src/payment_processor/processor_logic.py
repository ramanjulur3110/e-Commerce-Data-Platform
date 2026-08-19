import psycopg
from psycopg.rows import dict_row
from datetime import datetime, timezone
import time
import random
import os

DB_PARAMS = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

def retrieve_orders_to_process_payment():
    conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
    cur = conn.cursor()
    order_list = cur.execute(
        """
        SELECT o.order_id, po.payment_order_id, po.payment_status, po.attempts
        FROM generator.orders o
        LEFT JOIN generator.payment_orders po
            on o.order_id = po.order_id
        WHERE o.order_status in ('PENDING', 'PAYMENT PROCESSING')
        ORDER BY o.order_id ASC
        LIMIT 100
        """).fetchall()

    if len(order_list) >= 100:
        approved_list = []
        declined_list = []
        timeout_list = []
        for x in order_list:
            random_number = random.randint(1,100)
            if x['attempts'] >= 1:
                timeout_random_number = random.randint(1,100)
                if timeout_random_number > 90:
                    new_status = 'DECLINED'
                    declined_message = ''
                    random_number = random.randint(1,100)
                    if random_number > 99:
                        declined_message = 'LOST_OR_STOLEN_CARD'
                    elif random_number > 97:
                        declined_message = 'OTHER'
                    elif random_number > 94:
                        declined_message = 'INVALID_CARD_NUMBER'
                    elif random_number > 90:
                        declined_message = 'CARD_RESTRICTED'
                    elif random_number > 85:
                        declined_message = 'TRANSACTION_NOT_PERMITTED'
                    elif random_number > 80: 
                        declined_message = 'INVALID_CVV'
                    elif random_number > 73:
                        declined_message = 'CARD_EXPIRED'
                    elif random_number > 65:
                        declined_message = 'EXCEEDS_LIMIT'
                    elif random_number > 55:
                        declined_message = 'SUSPECTED_FRAUD'
                    elif random_number > 30:
                        declined_message = 'INSUFFICIENT_FUNDS'
                    else:
                        declined_message = 'DO_NOT_HONOR'
                    declined_list.append({'order_id':x['order_id'], 'payment_order_id':x['payment_order_id'], 'current_status':x['payment_status'], 'new_status':new_status, 'attempts':x['attempts'], 'error_message':declined_message})
                elif timeout_random_number > 70:
                    new_status = 'TIMEOUT'
                    timeout_list.append({'order_id':x['order_id'], 'payment_order_id':x['payment_order_id'], 'current_status':x['payment_status'], 'new_status':new_status, 'attempts':x['attempts']})
                else:
                    new_status = 'APPROVED'
                    approved_list.append({'order_id':x['order_id'], 'payment_order_id':x['payment_order_id'], 'current_status':x['payment_status'], 'new_status':new_status, 'attempts':x['attempts']})
            else:
                if random_number > 97:
                    new_status = 'TIMEOUT'
                    timeout_list.append({'order_id':x['order_id'], 'payment_order_id':x['payment_order_id'], 'current_status':x['payment_status'], 'new_status':new_status, 'attempts':x['attempts']})
                elif random_number > 94:
                    new_status = 'DECLINED'
                    declined_message = ''
                    random_number = random.randint(1,100)
                    if random_number > 99:
                        declined_message = 'LOST_OR_STOLEN_CARD'
                    elif random_number > 97:
                        declined_message = 'OTHER'
                    elif random_number > 94:
                        declined_message = 'INVALID_CARD_NUMBER'
                    elif random_number > 90:
                        declined_message = 'CARD_RESTRICTED'
                    elif random_number > 85:
                        declined_message = 'TRANSACTION_NOT_PERMITTED'
                    elif random_number > 80: 
                        declined_message = 'INVALID_CVV'
                    elif random_number > 73:
                        declined_message = 'CARD_EXPIRED'
                    elif random_number > 65:
                        declined_message = 'EXCEEDS_LIMIT'
                    elif random_number > 55:
                        declined_message = 'SUSPECTED_FRAUD'
                    elif random_number > 30:
                        declined_message = 'INSUFFICIENT_FUNDS'
                    else:
                        declined_message = 'DO_NOT_HONOR'
                    declined_list.append({'order_id':x['order_id'], 'payment_order_id':x['payment_order_id'], 'current_status':x['payment_status'], 'new_status':new_status, 'attempts':x['attempts'], 'error_message':declined_message})
                else:
                    new_status = 'APPROVED'
                    approved_list.append({'order_id':x['order_id'], 'payment_order_id':x['payment_order_id'], 'current_status':x['payment_status'], 'new_status':new_status, 'attempts':x['attempts']})

        print(f"\nThis batch is processing 100 orders (starting with oldest first)")
        print(f"Approved Orders: {len(approved_list)}")
        print(f"Declined Orders: {len(declined_list)}")
        print(f"Timeout Orders: {len(timeout_list)}")

        return order_list, approved_list, declined_list, timeout_list
    else:
        return [], [], [], []


def update_inital_statuses(order_list):
    conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
    cur = conn.cursor()

    # for x in order_list:
    #     print (x)

    payment_id_list = []
    order_id_list = []
    for x in order_list:
        if x['payment_status'] == 'INITIATED':
            order_id_list.append(x['order_id'])
            payment_id_list.append(x['payment_order_id'])
    placeholders_orders = ', '.join(['%s'] * len(order_id_list))
    placeholders_payments = ', '.join(['%s'] * len(payment_id_list))

    if order_id_list:
        query = f"UPDATE generator.orders SET order_status = 'PAYMENT PROCESSING', updated_at = CURRENT_TIMESTAMP WHERE order_id IN ({placeholders_orders})"
        cur.execute(query, order_id_list)

    if payment_id_list:
        query = f"UPDATE generator.payment_orders SET payment_status = 'PROCESSING', updated_at = CURRENT_TIMESTAMP WHERE order_id IN ({placeholders_orders})"
        cur.execute(query, order_id_list)

    if order_id_list:
        query = f"UPDATE generator.order_status_history SET effective_end_at = CURRENT_TIMESTAMP, is_current = FALSE WHERE order_id IN ({placeholders_orders}) AND is_current = TRUE"
        cur.execute(query, order_id_list)

    if payment_id_list:
        query = f"UPDATE generator.payment_status_history SET effective_end_at = CURRENT_TIMESTAMP, is_current = FALSE WHERE payment_order_id IN ({placeholders_payments}) AND is_current = TRUE"
        cur.execute(query, payment_id_list)

    insert_into_order_history_tuple = []
    for x in order_list:
        insert_into_order_history_tuple.append((x['order_id'], 'PAYMENT PROCESSING', datetime.now(timezone.utc), True))

    query = "INSERT INTO generator.order_status_history (order_id, order_status, effective_start_at, is_current) VALUES (%s, %s, %s, %s)"
    cur.executemany(query, insert_into_order_history_tuple)

    insert_into_payment_history_tuple = []
    for x in order_list:
        insert_into_payment_history_tuple.append((x['payment_order_id'], 'PROCESSING', datetime.now(timezone.utc), True))

    query = "INSERT INTO generator.payment_status_history (payment_order_id, payment_status, effective_start_at, is_current) VALUES (%s, %s, %s, %s)"
    cur.executemany(query, insert_into_payment_history_tuple)
    conn.commit()
    print("**************************************************************************************")
    print("Sleeping for 5 seconds to simulate realistic Processor response times...")
    print("**************************************************************************************")
    time.sleep(5)

def update_final_statuses(cur, order_dictionary, new_order_status, new_payment_status):
    if not order_dictionary:
        return
    order_id_list = []  
    payment_order_id_list = []
    for x in order_dictionary:
        order_id_list.append(x['order_id'])
        payment_order_id_list.append(x['payment_order_id'])
    placeholders = ', '.join(['%s'] * len(order_dictionary))

    query = f"UPDATE generator.orders SET order_status = '{new_order_status}', updated_at = CURRENT_TIMESTAMP WHERE order_id IN ({placeholders})"
    cur.execute(query, order_id_list)

    if new_payment_status == 'DECLINED':
        declined_payment_updates = []
        for x in order_dictionary:
            declined_payment_updates.append((new_payment_status, x['error_message'], x['payment_order_id']))
        query = """
            UPDATE generator.payment_orders SET payment_status = %s, attempts = attempts + 1, failure_reason = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE payment_order_id = %s
                """
        cur.executemany(query, declined_payment_updates)
    else:
        query = f"UPDATE generator.payment_orders SET payment_status = '{new_payment_status}', attempts = attempts + 1, updated_at = CURRENT_TIMESTAMP WHERE payment_order_id IN ({placeholders})"
        cur.execute(query, payment_order_id_list)

    query = f"UPDATE generator.order_status_history SET effective_end_at = CURRENT_TIMESTAMP, is_current = FALSE WHERE order_id IN ({placeholders}) AND is_current = TRUE"
    cur.execute(query, order_id_list)

    query = f"UPDATE generator.payment_status_history SET effective_end_at = CURRENT_TIMESTAMP, is_current = FALSE WHERE payment_order_id IN ({placeholders}) AND is_current = TRUE"
    cur.execute(query, payment_order_id_list)

    insert_into_order_history_tuple = []
    for x in order_dictionary:
        insert_into_order_history_tuple.append((x['order_id'], f'{new_order_status}', datetime.now(timezone.utc), True))

    query = "INSERT INTO generator.order_status_history (order_id, order_status, effective_start_at, is_current) VALUES (%s, %s, %s, %s)"
    cur.executemany(query, insert_into_order_history_tuple)

    insert_into_payment_history_tuple = []
    for x in order_dictionary:
        insert_into_payment_history_tuple.append((x['payment_order_id'], f'{new_payment_status}', datetime.now(timezone.utc), True))
    
    query = "INSERT INTO generator.payment_status_history (payment_order_id, payment_status, effective_start_at, is_current) VALUES (%s, %s, %s, %s)"
    cur.executemany(query, insert_into_payment_history_tuple)

def update_final_statuses_timeout(cur, order_dictionary, new_payment_status):
    if not order_dictionary:
        return
    for x in order_dictionary:
        if x['attempts'] < 2:
            query_1 = f"""
            UPDATE generator.payment_orders SET payment_status = '{new_payment_status}', attempts = '{x['attempts'] + 1}', updated_at = CURRENT_TIMESTAMP WHERE payment_order_id = '{x['payment_order_id']}'
            """
            cur.execute(query_1)
            query_2 = f"""
            UPDATE generator.payment_status_history SET effective_end_at = CURRENT_TIMESTAMP, is_current = FALSE WHERE payment_order_id = '{x['payment_order_id']}' AND is_current = TRUE
            """
            cur.execute(query_2)
            query_3 =f"""
                INSERT INTO generator.payment_status_history (payment_order_id, payment_status, effective_start_at, is_current) 
                VALUES ('{x['payment_order_id']}', '{new_payment_status}', CURRENT_TIMESTAMP, True)
                """
            cur.execute(query_3)

        elif x['attempts'] == 2:
            query = f"UPDATE generator.orders SET order_status = 'CANCELLED', updated_at = CURRENT_TIMESTAMP WHERE order_id = '{x['order_id']}'"
            cur.execute(query)
            query = f"UPDATE generator.order_status_history SET effective_end_at = CURRENT_TIMESTAMP, is_current = FALSE WHERE order_id = '{x['order_id']}' AND is_current = TRUE"
            cur.execute(query)
            query = f"""
                INSERT INTO generator.order_status_history (order_id, order_status, effective_start_at, is_current) 
                VALUES ('{x['order_id']}', 'CANCELLED', CURRENT_TIMESTAMP, True)"""
            cur.execute(query)

            query = f"UPDATE generator.payment_orders SET payment_status = 'DECLINED', failure_reason = 'MAX_RETRY_ATTEMPTS_EXCEEDED', attempts = '{x['attempts'] + 1}', updated_at = CURRENT_TIMESTAMP WHERE payment_order_id = '{x['payment_order_id']}'"
            cur.execute(query)
            query = f"UPDATE generator.payment_status_history SET effective_end_at = CURRENT_TIMESTAMP, is_current = FALSE WHERE payment_order_id = '{x['payment_order_id']}' AND is_current = TRUE"
            cur.execute(query)
            query =f"""
                INSERT INTO generator.payment_status_history (payment_order_id, payment_status, effective_start_at, is_current) 
                VALUES ('{x['payment_order_id']}', 'DECLINED', CURRENT_TIMESTAMP, True)"""
            cur.execute(query)