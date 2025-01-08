SELECT
    *,
    ROW_NUMBER()
        OVER (
            PARTITION BY sex
            ORDER BY wage DESC
        )
        AS index
FROM wages
LIMIT 10
