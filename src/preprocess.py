import pandas as pd

# Load datasets
orders = pd.read_csv('data/raw/olist_orders_dataset.csv')
items = pd.read_csv('data/raw/olist_order_items_dataset.csv')
customers = pd.read_csv('data/raw/olist_customers_dataset.csv')
payments = pd.read_csv('data/raw/olist_order_payments_dataset.csv')
products = pd.read_csv('data/raw/olist_products_dataset.csv')

# Convert datetime
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Merge datasets step-by-step
df = orders.merge(items, on='order_id', how='left')
df = df.merge(customers, on='customer_id', how='left')
df = df.merge(payments, on='order_id', how='left')
df = df.merge(products, on='product_id', how='left')

# Feature engineering
df['month'] = df['order_purchase_timestamp'].dt.to_period('M')
df['revenue'] = df['price'] + df['freight_value']

# Clean data
df.drop_duplicates(inplace=True)
df.fillna(0, inplace=True)

# Save processed data
df.to_csv('data/processed/cleaned_data.csv', index=False)

print("✅ Olist data cleaned successfully!")