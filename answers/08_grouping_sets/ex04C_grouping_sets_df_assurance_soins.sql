SELECT
    type_contrat AS typologie,
    SUM(montant_rembourse)
FROM df_assurance_soins
GROUP BY type_contrat

UNION

SELECT
    type_acte AS typologie,
    SUM(montant_rembourse)
FROM df_assurance_soins
GROUP BY type_acte

ORDER BY typologie
