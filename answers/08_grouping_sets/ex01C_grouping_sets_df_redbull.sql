SELECT store_id,
product_name,
COALESCE(product_name, 'tous_produits') AS product_name,
SUM(amount) as sum_amount
FROM df_stores_north
GROUP BY
GROUPING SETS ((store_id, product_name), store_id)
ORDER BY store_id, product_name, sum_amount
