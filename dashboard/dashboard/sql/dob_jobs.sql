SELECT
	dobjobs.bbl,
	first(pluto.address) as address,
	first(pluto.unitsres) as residentialunits,
	first(corpnames) as corpnames,
	count(case when dobjobs.jobtype ='A1' then 1 else null end) as a1,
	count(case when dobjobs.jobtype='A2' then 1 else null end) as a2,
	count(case when dobjobs.jobtype='DM' then 1 else null end) as dm,

	sum(case
		when dobjobs.jobtype = 'A1' then 1
		when dobjobs.jobtype = 'A2' then 1
		when dobjobs.jobtype = 'DM' then 1
		else 0 end) as total
FROM dobjobs
LEFT JOIN pluto_16v2 pluto on dobjobs.bbl = pluto.bbl
INNER JOIN rentstab c on c.ucbbl = dobjobs.bbl
LEFT JOIN hpd_registrations_grouped_by_bbl_with_contacts d on d.bbl = dobjobs.bbl
WHERE
   pluto.cd = '${ cd }'
   AND dobjobs.latestactiondate >= date_trunc('month', current_date - interval '1 month')
   AND (uc2007 > 0 or
       uc2008 > 0 or
       uc2009 > 0 or
       uc2010 > 0 or
       uc2011 > 0 or
       uc2012 > 0 or
       uc2013 > 0 or
       uc2014 > 0 or
       uc2015 > 0 or
       uc2016 > 0)
GROUP BY dobjobs.bbl
HAVING ( sum(case
		when dobjobs.jobtype = 'A1' then 1
		when dobjobs.jobtype = 'A2' then 1
		when dobjobs.jobtype = 'DM' then 1
		else 0 end) > 0 )
order by total desc
