SELECT
    year,
    region,
    SUM(population)
FROM dfpop
GROUP BY
    GROUPING SETS ((year, region), year)
ORDER BY region, year
