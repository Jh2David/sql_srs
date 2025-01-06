SELECT
    store_id,
    SUM(
        CASE WHEN product_name = 'redbull' THEN amount
        END
    ) AS product_amount,
    SUM(amount) AS total_amount,
    SUM(
        CASE WHEN product_name = 'redbull' THEN amount
        END
    ) / SUM(amount) AS pct_amount
FROM df_stores_north
GROUP BY store_id
ORDER BY store_id
