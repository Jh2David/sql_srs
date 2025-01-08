SELECT
    *,
    ROW_NUMBER() OVER (PARTITION BY department) AS index
FROM wages
