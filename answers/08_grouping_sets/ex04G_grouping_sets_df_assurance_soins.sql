SELECT
    type_contrat,
    type_acte,
    groupe_age,
    sexe,
    annee,
    SUM(montant_rembourse)
FROM df_assurance_soins
GROUP BY
    ROLLUP
    (type_contrat, type_acte, groupe_age, sexe, annee)
ORDER BY type_contrat, type_acte, groupe_age, sexe, annee
