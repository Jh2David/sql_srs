SELECT *,
AVG(visiteurs_count) OVER(
    PARTITION BY capteur_id
    ORDER BY Date
    ) AS avg_visitors_weekday
FROM df_capteurs_A_B
WHERE weekday = 7
ORDER BY capteur_id, date
