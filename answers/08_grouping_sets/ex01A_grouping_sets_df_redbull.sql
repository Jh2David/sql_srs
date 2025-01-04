SELECT store_id,
    product_name,
    SUM(amount)
FROM df_stores_north
WHERE product_name = 'redbull'
GROUP BY store_id, product_name
ORDER BY store_id