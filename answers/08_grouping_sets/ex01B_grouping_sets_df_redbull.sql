WITH total_sales AS (
    SELECT
        store_id,
        SUM(amount) AS total_sales
    FROM df_stores_north
    GROUP BY store_id
),

pct_sales AS (
    SELECT
        *,
        amount / total_sales AS pct_sales
    FROM df_stores_north
    LEFT JOIN total_sales
        ON df_stores_north.store_id = total_sales.store_id
)

SELECT
    store_id,
    total_sales,
    SUM(amount),
    SUM(pct_sales) AS product_pct_of_sales
FROM pct_sales
WHERE product_name = 'redbull'
GROUP BY store_id, amount, total_sales
ORDER BY store_id, amount, total_sales
