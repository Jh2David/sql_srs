SELECT
    *,
    AVG(visiteurs_count) OVER (
        PARTITION BY capteur_id, weekday
        ORDER BY date
    ) AS avg_visitors_weekday
FROM df_capteurs_a_b
ORDER BY capteur_id, weekday, date
