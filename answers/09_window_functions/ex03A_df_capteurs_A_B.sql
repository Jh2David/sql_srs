SELECT
    *,
    AVG(visiteurs_count) OVER (
        PARTITION BY capteur_id
        ORDER BY date
    ) AS avg_visitors_weekday
FROM df_capteurs_a_b
WHERE weekday = 7
ORDER BY capteur_id, date
