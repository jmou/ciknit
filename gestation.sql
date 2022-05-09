SELECT
    gestation_weeks,
    SUM(COALESCE(plurality, 1)) AS count
FROM
    @ref(natality)
WHERE
    NOT IS_NAN(gestation_weeks) AND gestation_weeks <> 99
GROUP BY
    gestation_weeks
ORDER BY
    gestation_weeks
