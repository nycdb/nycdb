select id, job, doc, borough, house, streetname, bbl, bin, address,
        jobtype, jobstatus, jobstatusdescription, latestactiondate,
        buildingtype, applicantname, ownername, 
        existingheight, proposedheight, existingnoofstories, proposednoofstories,
        existingdwelling, proposeddwellingunits, jobdescription
from dobjobs
where jobtype = 'NB' 
AND communityboard = '${ cd }'
order by latestactiondate desc
limit 10;
