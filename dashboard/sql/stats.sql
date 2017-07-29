select concat('lots') as name, count(*) as d
from pluto_16v2
where cd = '${ cd }'
union
select concat('unitsres') as name, sum(unitsres) as d
from pluto_16v2
where cd = '${ cd }'
union
select concat('buildingsres') as name, sum(numbldgs) as d
from pluto_16v2
where cd = '${ cd }'
and unitsres > 0;
