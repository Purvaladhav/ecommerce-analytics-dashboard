import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

# =========================
# 📦 LOAD DATA (FROM GITHUB)
# =========================
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/Purvaladhav/ecommerce-dataset/main/cleaned_data.csv"
    return pd.read_csv(url)

try:
    df = load_data()
except:
    st.error("🚨 Failed to load dataset. Check your URL.")
    st.stop()

# =========================
# 🧹 DATA CLEANING
# =========================
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'], errors='coerce')
df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'], errors='coerce')

df = df.dropna(subset=[
    'order_purchase_timestamp',
    'order_delivered_customer_date'
])

df['delivery_time'] = (
    df['order_delivered_customer_date'] - df['order_purchase_timestamp']
).dt.days

# =========================
# 🎯 KPIs
# =========================
st.title("📊 E-commerce Analytics Dashboard")

col1, col2, col3, col4 = st.columns(4)

total_orders = df.shape[0]
avg_delivery = round(df['delivery_time'].mean(), 2)

# revenue (if exists)
if 'price' in df.columns:
    total_revenue = df['price'].sum()
else:
    total_revenue = 0

unique_cities = df['customer_city'].nunique() if 'customer_city' in df.columns else 0

col1.metric("📦 Total Orders", total_orders)
col2.metric("💰 Total Revenue", f"{total_revenue:,.0f}")
col3.metric("🚚 Avg Delivery (days)", avg_delivery)
col4.metric("🌍 Cities", unique_cities)

st.markdown("---")

# =========================
# 📈 ORDERS OVER TIME
# =========================
st.subheader("📈 Orders Over Time")

df['order_date'] = df['order_purchase_timestamp'].dt.date
orders_trend = df.groupby('order_date').size().reset_index(name='orders')

fig = px.line(orders_trend, x='order_date', y='orders', title="Orders Trend")
st.plotly_chart(fig, use_container_width=True)

# =========================
# 📦 ORDER STATUS
# =========================
if 'order_status' in df.columns:
    st.subheader("📦 Order Status Breakdown")

    status_counts = df['order_status'].value_counts().reset_index()
    status_counts.columns = ['status', 'count']

    fig2 = px.pie(status_counts, names='status', values='count')
    st.plotly_chart(fig2, use_container_width=True)

# =========================
# 🌍 CITY ANALYSIS
# =========================
if 'customer_city' in df.columns:
    st.subheader("🌍 Top Cities by Orders")

    city_counts = df['customer_city'].value_counts().head(10).reset_index()
    city_counts.columns = ['city', 'orders']

    fig3 = px.bar(city_counts, x='city', y='orders', title="Top Cities")
    st.plotly_chart(fig3, use_container_width=True)

# =========================
# 💰 REVENUE ANALYSIS
# =========================
if 'price' in df.columns:
    st.subheader("💰 Revenue Over Time")

    revenue_trend = df.groupby('order_date')['price'].sum().reset_index()

    fig4 = px.line(revenue_trend, x='order_date', y='price', title="Revenue Trend")
    st.plotly_chart(fig4, use_container_width=True)

# =========================
# 📋 RAW DATA VIEW
# =========================
st.subheader("📋 Sample Data")
st.dataframe(df.head(100))
