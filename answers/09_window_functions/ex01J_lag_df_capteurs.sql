SELECT
    *,
    LAG(visiteurs_count) OVER (
        PARTITION BY weekday
        ORDER BY date
    ) AS lag_visiteurs_count
FROM df_capteurs
