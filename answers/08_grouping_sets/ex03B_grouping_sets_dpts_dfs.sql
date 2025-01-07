SELECT
    year,
    SUM(population) FILTER (WHERE region = 'IDF') AS idf,
    SUM(population) AS total_pop,
    idf / total_pop
FROM dpts_dfs
GROUP BY "year"
ORDER BY year