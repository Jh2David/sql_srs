SELECT
    *,
    LAG(visiteurs_count) OVER () AS ligne_precedente
FROM df_capteurs
ORDER BY date
