SELECT * FROM df_customers
LEFT JOIN detailed_order
USING(customer_id);

