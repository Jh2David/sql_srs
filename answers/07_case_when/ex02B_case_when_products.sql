SELECT
    SUM(
        CASE
            WHEN discount_code = 'DISCOUNT10' THEN quantity * price_per_unit * 0.9
            WHEN discount_code = 'DISCOUNT20' THEN quantity * price_per_unit * 0.8
            ELSE quantity * price_per_unit
        END
    ) AS total_revenue
FROM
    df
GROUP BY
    discount_code
ORDER BY
    total_revenue