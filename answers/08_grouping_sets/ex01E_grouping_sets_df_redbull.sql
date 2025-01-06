SELECT
    store_id,
    SUM(amount) FILTER (WHERE product_name = 'redbull') AS redbull_amount,
    SUM(amount)
FROM df_stores_north
GROUP BY store_id
ORDER BY store_id
