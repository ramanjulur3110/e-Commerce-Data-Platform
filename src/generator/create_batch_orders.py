from datetime import datetime, timezone
import random

def create_batch_orders(batch_metadata):
    for order_insert in range(batch_metadata['batch_amount']):
        number_of_random_products = random.randint(1,5)
        # random_product_list = [random.choice(batch_metadata['all_products']) for x in range(number_of_random_products)]

        all_products_standard = [x for x in batch_metadata['all_products'] if x['shipping_class'] == 'STANDARD']
        all_products_large = [x for x in batch_metadata['all_products'] if x['shipping_class'] == 'LARGE']
        all_products_oversized = [x for x in batch_metadata['all_products'] if x['shipping_class'] == 'OVERSIZED']

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


        random_customer = random.choice(batch_metadata['all_customers'])
        order_timestamp = datetime.now(timezone.utc)

        total_amount = 0
        for x in random_product_list:
            if x['price'] <= 50 and x['shipping_class'] == 'STANDARD':
            # if x['price'] <= 50:
                x['quantity'] = random.randint(1,5)
            else:
                x['quantity'] = 1
            total_amount += x['price'] * x['quantity']
        
        batch_metadata['order_insert_tuple'].append((random_customer['customer_id'], order_timestamp, 'PENDING', total_amount))

        for i, x in enumerate(random_product_list):
            batch_metadata['order_details_insert_tuple_start'].append([batch_metadata['number_insert'], i+1, x['product_id'], x['quantity'], x['price']])
        batch_metadata['number_insert'] += 1