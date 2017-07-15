select sales.*
from (
	select concat(address, ', ', zipcode) as address,
               saleprice,
	       to_char(saleprice, 'L999,999,999,999') as price,
	       saledate,
               to_char(saledate, 'YYYY-MM-DD') as date,
               commercialunits,
               residentialunits,
               bbl
	 from dof_sales
	 where saledate > (now() - make_interval(months => 6))
      ) as sales
left join pluto_16v2 on pluto_16v2.bbl = sales.bbl
where pluto_16v2.cd = '${ cd }'
order by sales.saleprice desc nulls last
limit 10;
