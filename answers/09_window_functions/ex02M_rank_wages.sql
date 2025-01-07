SELECT
    *,
    DENSE_RANK() OVER (
        PARTITION BY sex
        ORDER BY wage DESC
    ) AS index
FROM wages
