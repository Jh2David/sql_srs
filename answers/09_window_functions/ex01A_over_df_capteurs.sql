SELECT
    *,
    SUM(visiteurs_count) OVER () AS total_visiteurs
FROM df_capteurs
ORDER BY weekday
