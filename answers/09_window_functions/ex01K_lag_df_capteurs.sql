SELECT
    *,
    LAG(visiteurs_count) OVER (
        PARTITION BY weekday
        ORDER BY date
    ) AS lag_visiteurs_count,
    (visiteurs_count - lag_visiteurs_count) / lag_visiteurs_count AS pct_change
FROM df_capteurs
