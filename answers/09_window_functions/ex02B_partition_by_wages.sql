SELECT
    *,
    MAX(wage) OVER (PARTITION BY department) AS max_dpt_wage
FROM wages
ORDER BY department
