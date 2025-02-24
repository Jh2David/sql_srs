SELECT Commune,
    CAST(MEAN(valeur_fonciere) AS INTEGER) as vf,
    COUNT(*) AS nb_lines
FROM appt_nord
GROUP BY Commune
ORDER BY Commune;