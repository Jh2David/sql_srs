SELECT
    year,
    SUM(
        CASE
            WHEN region = 'IDF' THEN population
        END
    ) AS idf,
    SUM(population) AS total_pop,
    idf / total_pop
FROM dpts_dfs
GROUP BY "year"
