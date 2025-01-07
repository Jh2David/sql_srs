SELECT
    *,
    ROW_NUMBER() OVER (
        PARTITION BY sex
    ) AS index
FROM wages
