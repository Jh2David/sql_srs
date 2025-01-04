SELECT
  department,
  CASE
      WHEN wage <= 50000 THEN 'Low'
      WHEN wage < 90000 THEN 'Medium'
      ELSE 'High'
  END AS salary_range,
  AVG(wage) AS average_salary
FROM
  wages
GROUP BY
  department,
  CASE
      WHEN wage <= 50000 THEN 'Low'
      WHEN wage < 90000 THEN 'Medium'
      ELSE 'High'
  END
ORDER BY
    average_salary