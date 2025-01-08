SELECT
    *,
    ROW_NUMBER() OVER () AS index
FROM wages
ORDER BY department
