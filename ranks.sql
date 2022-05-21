SELECT
  year,
  name,
  SUM(number) AS number,
  ROW_NUMBER() OVER (PARTITION BY year ORDER BY SUM(number) DESC) AS rank
FROM `bigquery-public-data.usa_names.usa_1910_2013`
WHERE gender = 'F'
GROUP BY year, name
