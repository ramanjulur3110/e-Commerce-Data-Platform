from .create_batch_orders import create_batch_orders
from src.database.database_retrieve import retrieve_all_customers, retrieve_all_products, truncate_prod_tables
from src.database.database_insert import order_generator_inserts
from src.common.utils import reset_batch_metadata
import random
import signal
import time

running = True

def handle_interrupt(signum, frame):
    global running
    print("\n[!] Stop signal received. Finishing the current cycle...")
    running = False
    raise InterruptedError()

def main():
    start_time = time.perf_counter()

    batch_metadata = {
        'all_customers' :  [],
        'all_products' : [],
        'total_batches': random.randint(1, 10),
        'batch_amount': 100,
        'order_insert_tuple': [],
        'order_details_insert_tuple_start': [],
        'order_details_insert_tuple_final': [],
        'number_insert': 0,
        'update_dict': {}, 
        'list_of_generated_order_numbers': []
    }

    batch_metadata['all_customers'] = retrieve_all_customers()
    batch_metadata['all_products'] = retrieve_all_products()

    for batch_loop in range(batch_metadata['total_batches']):
        #Create batch order data and place that information into corresponding dictionaries
        create_batch_orders(batch_metadata)

        #Inserts data into the following 4 tables:
        #1. generator.orders, 
        #2. generator.order_details, 
        #3. generator.order_status_history, 
        #4. generator.payment_orders, 
        #5. generator.payment_orders_state_history
        order_generator_inserts(batch_metadata)

        #Resets portions of batch metadata after an iteration of batch_loop. 
        reset_batch_metadata(batch_metadata)

    end_time = time.perf_counter()
    elapsed_seconds = end_time - start_time
    elapsed_minutes = elapsed_seconds / 60
    print(f"Created and inserted {batch_metadata['total_batches'] * batch_metadata['batch_amount']} orders ({batch_metadata['total_batches']} batches with each batch consisting of {batch_metadata['batch_amount']} orders)")
    print(f"Total Elapsed time: {elapsed_minutes:.4f} minutes")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    truncate_tables = True
    if truncate_tables:
        truncate_prod_tables()
        print("truncate_tables flag set to True.")
        print("Truncated the following tables:\n#1. generator.orders\n#2. generator.order_details\n#3. generator.order_status_history\n#4. generator.payment_orders\n#5. generator.payment_orders_state_history")
        print("Identity has also been reset for all truncated tables\n")
    
    print("Generating Orders Started. Press Ctrl+C to safely exit after the current iteration finishes.")
    while running:
        main()
        if running:
            random_number = random.randint(1,3) * 60
            print (f"Sleeping for {random_number} seconds...")
            try: 
                time.sleep(random_number)
            except InterruptedError:
                print("Current sleep cycle canceled by system signal.")

    print("Generating Orders Finished and shut down cleanly.")

