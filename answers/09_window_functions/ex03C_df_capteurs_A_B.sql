WITH moving_avg_visitors AS (
    SELECT
        *,
        AVG(visiteurs_count) OVER (
            PARTITION BY capteur_id, weekday
            ORDER BY date
        ) AS avg_visitors_weekday
    FROM df_capteurs_a_b
    ORDER BY capteur_id, weekday, date
)

SELECT
    *,
    DENSE_RANK() OVER (
        PARTITION BY date
        ORDER BY avg_visitors_weekday DESC
    ) AS updated_ranking
FROM
    moving_avg_visitors
ORDER BY updated_ranking, date
