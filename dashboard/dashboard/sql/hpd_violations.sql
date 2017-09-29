select a.bbl, b.cd, CONCAT(a.housenumber, ' ', a.streetname) as address ,
	count(case when a.violationclass = 'A' then 1 else null end) as class_a,
	count(case when a.violationclass = 'B' then 1 else null end) as class_b,
	count(case when a.violationclass = 'C' then 1 else null end) as class_c,
    count(a.violationclass) as total
from hpd_violations a
left join pluto_16v2 b on a.bbl = b.bbl
where a.novissueddate >= '2017-07-01' and a.novissueddate < '2017-08-01' AND b.cd = '${ cd }'
group by a.bbl, b.cd, a.housenumber, a.streetname
having count(a.violationclass) > 9
order by total desc;