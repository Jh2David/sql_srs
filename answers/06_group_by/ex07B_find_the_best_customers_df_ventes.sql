SELECT client,
MEAN(montant) as mean_sales
FROM df_ventes
GROUP BY CLIENT
HAVING mean_sales >
(SELECT MEAN(montant) FROM df_ventes)
ORDER BY client
