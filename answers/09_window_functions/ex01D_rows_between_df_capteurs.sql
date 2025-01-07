SELECT
    *,
    AVG(visiteurs_count) OVER (
        ORDER BY date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_days_moving_average
FROM df_capteurs
