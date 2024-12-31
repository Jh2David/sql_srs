SELECT Commune,
    COUNT(*)
FROM appt_nord
GROUP BY Commune
ORDER BY Commune;
