SELECT year, name, number
FROM @ref(ranks)
WHERE rank <= 15
