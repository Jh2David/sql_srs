SELECT client, MEAN(montant) as total_ventes
FROM df_ventes
GROUP BY client
ORDER BY client
