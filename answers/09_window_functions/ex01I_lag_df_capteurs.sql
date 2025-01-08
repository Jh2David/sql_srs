SELECT
    *,
    LAG(visiteurs_count) OVER () AS ligne_precedente
FROM df_capteurs
WHERE weekday = 7
ORDER BY date
