import pandas as pd
import streamlit as st
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="E-commerce Pro Dashboard", layout="wide")

# ==============================
# LOAD DATA
# ==============================
df = pd.read_csv("data/processed/cleaned_data.csv")

# Convert dates
df['order_delivered_customer_date'] = pd.to_datetime(
    df['order_delivered_customer_date'], errors='coerce'
)

df['order_purchase_timestamp'] = pd.to_datetime(
    df['order_purchase_timestamp'], errors='coerce'
)

df = df.dropna(subset=[
    'order_delivered_customer_date',
    'order_purchase_timestamp'
])

# Feature Engineering
df['delivery_time'] = (
    df['order_delivered_customer_date'] - df['order_purchase_timestamp']
).dt.days

# ==============================
# OPTIONAL: Revenue Column
# ==============================
if 'price' in df.columns:
    df['revenue'] = df['price']
else:
    df['revenue'] = 0  # fallback

# ==============================
# SIDEBAR FILTERS
# ==============================
st.sidebar.header("Filters")

status_filter = st.sidebar.multiselect(
    "Order Status",
    df['order_status'].unique(),
    default=df['order_status'].unique()
)

df = df[df['order_status'].isin(status_filter)]

# ==============================
# TITLE
# ==============================
st.title("🚀 FAANG-Level E-commerce Analytics Dashboard")

# ==============================
# KPIs
# ==============================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Orders", len(df))
col2.metric("Avg Delivery Time", round(df['delivery_time'].mean(), 2))
col3.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
col4.metric("Unique Customers", df['customer_id'].nunique())

# ==============================
# 📈 ORDERS OVER TIME (Plotly)
# ==============================
st.subheader("📈 Orders Over Time")

orders_time = df.groupby(df['order_purchase_timestamp'].dt.date).size().reset_index()
orders_time.columns = ['date', 'orders']

fig1 = px.line(orders_time, x='date', y='orders', title="Orders Trend")
st.plotly_chart(fig1, use_container_width=True)

# ==============================
# 💰 REVENUE ANALYSIS
# ==============================
st.subheader("💰 Revenue Over Time")

revenue_time = df.groupby(df['order_purchase_timestamp'].dt.date)['revenue'].sum().reset_index()
fig2 = px.area(revenue_time, x='order_purchase_timestamp', y='revenue',
               title="Revenue Trend")
st.plotly_chart(fig2, use_container_width=True)

# ==============================
# 📦 ORDER STATUS
# ==============================
st.subheader("📦 Order Status Breakdown")

fig3 = px.pie(df, names='order_status', title="Order Status Distribution")
st.plotly_chart(fig3, use_container_width=True)

# ==============================
# 🌍 CITY ANALYSIS (if exists)
# ==============================
if 'customer_city' in df.columns:
    st.subheader("🌍 Orders by City")

    city_data = df['customer_city'].value_counts().head(10).reset_index()
    city_data.columns = ['city', 'orders']

    fig4 = px.bar(city_data, x='city', y='orders', title="Top Cities")
    st.plotly_chart(fig4, use_container_width=True)

# ==============================
# 🤖 ML MODEL (Delivery Prediction)
# ==============================
st.subheader("🤖 Delivery Time Prediction (ML)")

# Basic features
df_ml = df.copy()
df_ml['purchase_day'] = df_ml['order_purchase_timestamp'].dt.day
df_ml['purchase_month'] = df_ml['order_purchase_timestamp'].dt.month

features = ['purchase_day', 'purchase_month']
target = 'delivery_time'

df_ml = df_ml.dropna(subset=features + [target])

X = df_ml[features]
y = df_ml[target]

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestRegressor()
model.fit(X_train, y_train)

# User input
st.write("### Predict Delivery Time")

day = st.slider("Purchase Day", 1, 31, 15)
month = st.slider("Purchase Month", 1, 12, 6)

prediction = model.predict([[day, month]])
st.success(f"Estimated Delivery Time: {round(prediction[0], 2)} days")

# ==============================
# 📋 DATA TABLE
# ==============================
st.subheader("📋 Data Preview")
st.dataframe(df.head(50))