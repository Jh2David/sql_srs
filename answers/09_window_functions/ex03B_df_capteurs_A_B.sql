SELECT *,
AVG(visiteurs_count) OVER(
    PARTITION BY capteur_id, weekday
    ORDER BY Date
    ) AS avg_visitors_weekday
FROM df_capteurs_A_B
ORDER BY capteur_id, weekday, date
