SELECT *,
RANK() OVER(
    PARTITION BY department
    ORDER BY wage DESC) AS index
FROM wages
LIMIT 10