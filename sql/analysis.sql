-- Total Revenue
SELECT SUM(revenue) FROM cleaned_data;

-- Monthly Revenue
SELECT month, SUM(revenue)
FROM cleaned_data
GROUP BY month
ORDER BY month;

-- Top Categories
SELECT product_category_name, SUM(revenue) AS revenue
FROM cleaned_data
GROUP BY product_category_name
ORDER BY revenue DESC
LIMIT 10;

-- Customer Retention
SELECT customer_unique_id, COUNT(order_id) AS orders
FROM cleaned_data
GROUP BY customer_unique_id
HAVING COUNT(order_id) > 1;

-- Delivery Performance
SELECT AVG(DATEDIFF(order_delivered_customer_date, order_purchase_timestamp)) AS avg_delivery_days
FROM cleaned_data;