WITH aggregate_table AS (
    SELECT Commune,
        CAST(MEAN(valeur_fonciere) AS INTEGER) as vf,
        COUNT(*) AS nb_lines
    FROM appt_nord
    GROUP BY Commune
    ORDER BY Commune
)

SELECT * FROM aggregate_table
WHERE nb_lines > 10
