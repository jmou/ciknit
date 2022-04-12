select name, sum(number) as count
from @ref(names)
group by name
order by count desc
limit 5
