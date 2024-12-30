SELECT *
FROM order_client cc
LEFT JOIN df_products products
ON cc.product_id = products.product_id;
