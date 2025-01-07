WITH sales_totals AS (
    SELECT
        store_id,
        COALESCE(product_name, 'tout_le_magasin') AS product_name,
        SUM(amount) AS sum_amount
    FROM df_stores_north
    GROUP BY
        GROUPING SETS ((store_id, product_name), store_id)
    ORDER BY store_id
)

SELECT
    ls.store_id,
    ls.product_name AS l_product_name,
    rs.product_name AS r_product_name,
    ls.sum_amount AS product_sum_amount,
    rs.sum_amount AS store_sum_amount,
    product_sum_amount / store_sum_amount AS product_pct
FROM sales_totals AS ls
INNER JOIN sales_totals AS rs
    ON ls.store_id = rs.store_id
WHERE ls.product_name = 'redbull' AND rs.product_name = 'tout_le_magasin'
ORDER BY ls.store_id, l_product_name
