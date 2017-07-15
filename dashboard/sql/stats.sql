select concat('lots') as name, count(*) as d
from pluto_16v2
where cd = '${ cd }'
union
select concat('unitsres'), sum(unitsres) as d
from pluto_16v2
where cd = '${ cd }'
