SELECT
    type_contrat,
    SUM(montant_rembourse)
FROM df_assurance_soins
GROUP BY type_contrat
ORDER BY type_contrat
