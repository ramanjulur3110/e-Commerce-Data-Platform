import psycopg
from psycopg.rows import dict_row
from .processor_logic import *
import time
import random
import signal
import os

running = True

def handle_interrupt(signum, frame):
    global running
    print("\n[!] Stop signal received. Finishing the current cycle...")
    running = False
    raise InterruptedError()
     
def main():
    start_time = time.perf_counter()
    order_list, approved_list, declined_list, timeout_list = retrieve_orders_to_process_payment()
    if order_list:
        update_inital_statuses(order_list)

        conn = psycopg.connect(**DB_PARAMS, row_factory=dict_row)
        cur = conn.cursor()
        print("Updating Final Statuses for Approved Orders")
        update_final_statuses(cur, approved_list, 'PAID', 'APPROVED')

        print("Updating Final Statuses for Declined Orders")
        update_final_statuses(cur, declined_list, 'CANCELLED', 'DECLINED')

        print("Updating Statuses for Timeout Orders. NOTE: After 3 failed attempts an order is DECLINED/CANCELLED")
        update_final_statuses_timeout(cur, timeout_list, 'TIMEOUT')
        conn.commit()

        end_time = time.perf_counter()
        elapsed_seconds = end_time - start_time
        print(f"\nTotal Payment Processing Time: {elapsed_seconds:.6f} seconds")
    else:
        print("Less than 100 orders available to process. Skipping current run.")

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_interrupt)
    signal.signal(signal.SIGTERM, handle_interrupt)

    print("Payment Processor Started. Press Ctrl+C to safely exit after the current iteration finishes.")
    while running:
        main()
        if running:
            print (f"Sleeping for 10 seconds...")
            try: 
                time.sleep(10)
            except InterruptedError:
                print("Current sleep cycle canceled by system signal.")

    print("Shutting down payment processor.")