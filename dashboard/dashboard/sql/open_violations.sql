select count(*) as buildings,
       sum(ov.c) as number_of_violations
from (
	select bbl, count(*) as c
     	from hpd_open_violations
    	group by bbl
      ) as ov
left join pluto_16v2 on pluto_16v2.bbl = ov.bbl
where pluto_16v2.cd = '${ cd }';
