SELECT
    *,
    AVG(visiteurs_count) OVER (
        ORDER BY date
    ) AS total_visiteurs
FROM df_capteurs
ORDER BY date
