SELECT
    department,
    MAX(wage)
FROM wages
GROUP BY department
ORDER BY department
