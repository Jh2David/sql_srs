SELECT
    type_contrat,
    type_acte,
    SUM(montant_rembourse)
FROM df_assurance_soins
GROUP BY
    ROLLUP
    (type_contrat, type_acte)
ORDER BY type_contrat, type_acte
