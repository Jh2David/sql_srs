SELECT *
FROM df_orders
LEFT JOIN df_order_details
USING (order_id);
