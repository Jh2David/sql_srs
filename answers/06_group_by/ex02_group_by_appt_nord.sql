SELECT Commune,
    CAST(MEAN(valeur_fonciere) AS INTEGER) as vf
FROM appt_nord
GROUP BY Commune
ORDER BY Commune;