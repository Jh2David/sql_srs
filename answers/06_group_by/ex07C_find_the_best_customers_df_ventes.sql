WITH mean_sale AS
    (SELECT MEAN(montant) FROM df_ventes)

SELECT client,
MEAN(montant) as total_sales
FROM df_ventes
GROUP BY CLIENT
HAVING total_sales > (SELECT * FROM mean_sale)
ORDER BY client
