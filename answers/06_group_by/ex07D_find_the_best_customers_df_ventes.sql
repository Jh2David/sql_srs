WITH TOTAL_SALES_PER_CLIENT AS (
    SELECT SUM(montant) AS total_sales
    FROM df_ventes
    GROUP BY client
),

MEAN_TOTAL_SALES AS (
    SELECT MEAN(total_sales)
    FROM TOTAL_SALES_PER_CLIENT
)

SELECT client,
SUM(montant) as total_sales
FROM df_ventes
GROUP BY CLIENT
HAVING total_sales >
(SELECT * FROM MEAN_TOTAL_SALES)
ORDER BY client
