import psycopg
import os
import csv

DB_PARAMS = {
    'dbname': os.getenv("DB_NAME", "mydatabase"),
    'user': os.getenv("DB_USER", "admin"),
    'password': os.getenv("DB_PASSWORD", "admin"),
    'host': os.getenv("DB_HOST", "localhost"),
    'port': int(os.getenv("DB_PORT", "5433"))
}

conn = psycopg.connect(**DB_PARAMS)
cur = conn.cursor()
updated_rows = []
with open("src_data/ecommerce_products_1000_review.csv", mode="r", newline='') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    for row in reader:
        row['price'] = (row['price'].replace(',', ''))
        row['cost'] = (row['cost'].replace(',', ''))
        updated_rows.append(row)

with open("src_data/ecommerce_products_1000_review.csv", mode="w", newline="", encoding="utf-8") as f:
  writer = csv.DictWriter(f, fieldnames=fieldnames)
  writer.writeheader()
  writer.writerows(updated_rows)

with open("src_data/ecommerce_products_1000_review.csv", "r", encoding="utf-8") as f:
    sql = "COPY generator.products" \
    "(sku, product_name, category, subcategory, brand, price, cost, weight_lbs, length_in, width_in, height_in, shipping_class, stock_quantity, is_active)" \
    " FROM STDIN WITH (FORMAT CSV, HEADER);"
    cur.copy_expert(sql, f)

conn.commit()
cur.close()
conn.close()