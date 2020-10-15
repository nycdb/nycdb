-- Information about any given case is spread across 11 different tables and
-- includes ton of detail, but for analysis purposes it is helpful to have a
-- simplified summary table in which each case is represented by a single row.
-- To create this summary table we aggregate each table grouping by case id
-- and taking some summary of the relevant columns and then joining all of
-- these together. These summary indicators are often a count of records in
-- one of the tables (eg. the number of motions, warrants, etc.), or the value
-- of one of the columns for the first or last record that appears for that
-- case (eg. the reason or status listed for the most recent warrant). These
-- first() and last() functions are defined in "first_last.sql"

DROP TABLE IF EXISTS oca_case_summary;		
CREATE TABLE IF NOT EXISTS oca_case_summary AS (
	with index as (
		-- Each row is a case, we'll join everything else onto this after other
		-- tables are aggregated to one row per case
		SELECT
			indexnumberid,
			extract(year from fileddate) AS filed_year,
			fileddate AS filed_date,
			court,
			CASE 
				WHEN court ~* '(new york)|(harlem)'				THEN 'Manhattan'
				WHEN court ~* 'bronx' 							THEN 'Bronx'
				WHEN court ~* '(brooklyn)|(kings)|(redhook)' 	THEN 'Brooklyn'
				WHEN court ~* 'queens' 							THEN 'Queens'
				WHEN court ~* 'richmond' 						THEN 'Staten Island'
			END AS court_boro,
			-- TODO: get someone with expertise to look through specialtydesignationtypes, 
			-- any others we are interested in catching?
			coalesce(specialtydesignationtypes::text ~* 'NYCHA', false) AS is_nycha,
			coalesce(specialtydesignationtypes::text ~* '(condo|co.?op)', false) AS is_condo_coop,
			propertytype AS property_type,
			classification,
			specialtydesignationtypes AS specialty_designation_types,
			status,
			disposeddate AS disposed_date,
			disposedreason AS disposed_reason,
			firstpaper AS first_paper,
			primaryclaimtotal AS primary_claim_total,
			dateofjurydemand AS jury_demand_date
		FROM oca_index
	),

	addresses as (
		-- There is almost always one address row per case, but where there are
		-- multiple we just keep the first one.
		SELECT
			indexnumberid,
			first(city order by indexnumberid) AS city,
			substr(first(postalcode order by indexnumberid), 1, 5) AS zip5
		FROM oca_addresses
		GROUP BY indexnumberid
	),

	parties as (
		SELECT
			indexnumberid,
			max((role = 'Petitioner' and representationtype  = 'Counsel')::int)::boolean AS petitioner_rep_any,
			max((role = 'Respondent' and representationtype  = 'Counsel')::int)::boolean AS respondent_rep_any,
			max((role = 'Respondent' and representationtype != 'No Appearance')::int)::boolean AS respondent_appear_ever
			-- TODO: party type? (Person, Business, Agency) - Maybe any business?
			-- TODO: undertenants? (True/False) - Maybe "(petitioner|respondent)_undertenant_any"
		FROM oca_parties
		GROUP BY indexnumberid
	),

	causes as (
		SELECT
			indexnumberid,
			array_agg(causeofactiontype) AS cause_of_action_types
		FROM oca_causes
		GROUP BY indexnumberid
	),

	events as (
		SELECT
			-- TODO: are any of these useful? I'm not completely clear on the
			-- difference between events and appearances. In the old version of the
			-- data I've used there was no events table so I'm not familiar and just
			-- mimicked what I had done for appearances
			indexnumberid,
			count(*) AS events_num,
			first(e.eventname order by e.fileddate::date) AS event_name_first,
			first(e.fileddate order by e.fileddate::date) AS event_date_first,
			last(e.eventname order by e.fileddate::date) AS event_name_last,
			last(e.fileddate order by e.fileddate::date) AS event_date_last
		FROM oca_events AS e
		GROUP BY indexnumberid
	),

	appearances as (
		SELECT
			indexnumberid,
			count(*) AS appearances_num,
			min(ap.appearancedatetime)::date AS appear_date_first,
			first(apo.appearanceoutcometype order by ap.appearancedatetime) AS appear_outcomes_first,
			max(ap.appearancedatetime)::date AS appear_date_last,
			last(apo.appearanceoutcometype order by ap.appearancedatetime)AS appear_outcomes_last,
			sum((apo.appearanceoutcometype ~* 'adjourn')::int) AS adjournments_num
		FROM oca_appearances AS ap
		LEFT JOIN oca_appearance_outcomes as apo USING(indexnumberid, appearanceid)
		GROUP BY indexnumberid
	),

	motions as (			
		SELECT
			indexnumberid,
			count(*) AS motions_num
		FROM oca_motions AS m
		GROUP BY indexnumberid
	),

	motions_show_cause as (			
		SELECT
			m.indexnumberid,
			count(*) AS motions_show_cause_num,
			last(ap.appearancedatetime order by ap.appearancedatetime)::date AS motion_show_cause_date_last,
			last(m.motiondecision order by ap.appearancedatetime) ~* 'granted' AS motion_show_cause_last_granted
		FROM oca_motions AS m
		-- Join to oca_apperances to get date associated with motion
		LEFT JOIN oca_appearances AS ap 
			ON m.indexnumberid = ap.indexnumberid AND
				 m.sequence = ap.motionsequence
		WHERE m.motiontype = 'Order to Show Cause'
		GROUP BY m.indexnumberid
	),

	decisions as (			
		SELECT
			indexnumberid,
			count(*) AS decisions_num,
			last(resultof order by sequence) AS decision_resultof_last,
			last(highlight order by sequence) AS decision_highlight_last
		FROM oca_decisions AS d
		GROUP BY indexnumberid
	),

	judgments as (	 
		SELECT
			indexnumberid,
			count(*) AS judgments_num,
			last(j.judgmenttype order by j.sequence) AS judgment_type_last,
			last(j.withpossession order by j.sequence) AS judgment_last_with_possession
		FROM oca_judgments AS j
		GROUP BY indexnumberid
	),

	warrants as (
		-- TODO: There is probably a lot more that is worth capturing here. Maybe
		-- we can even link these to the address-level marshals evictions dataset
		SELECT
			indexnumberid,
			count(*) AS warrants_num,
			first(w.ordereddate order by w.ordereddate) AS warrant_ordered_date_first,
			last(w.ordereddate order by w.ordereddate) AS warrant_ordered_date_last,
			last(w.executiondate order by w.executiondate) AS warrant_execution_date_last,
			last(w.vacateddate order by w.vacateddate) AS warrant_vacated_date_last,
			last(w.returneddate order by w.returneddate) AS warrant_returned_date_last,
			last(w.returnedreason order by w.returneddate) AS warrant_returned_reason_last
		FROM oca_warrants AS w
		GROUP BY indexnumberid
	)
	
	SELECT
		i.indexnumberid,
		i.filed_year,
		i.filed_date,
		i.court,
		i.court_boro,
		i.is_nycha,
		i.is_condo_coop,
		i.property_type,
		i.classification,
		i.specialty_designation_types,
		i.status,
		i.disposed_date,
		i.disposed_reason,
		i.first_paper,
		i.primary_claim_total,
		i.jury_demand_date,

		ad.city,
		ad.zip5,

		p.petitioner_rep_any,
		p.respondent_rep_any,
		p.respondent_appear_ever,

		c.cause_of_action_types,

		coalesce(e.events_num, 0) AS events_num,
		e.event_name_first,
		e.event_date_first,
		e.event_date_first - i.filed_date AS days_to_event_first,
		e.event_name_last,
		e.event_date_last,
		e.event_date_last - i.filed_date AS days_to_event_last,

		coalesce(ap.appearances_num, 0) AS appearances_num,
		coalesce(ap.adjournments_num, 0) AS adjournments_num,
		ap.appear_date_first,
		ap.appear_date_first - i.filed_date AS days_to_appear_first,
		ap.appear_date_last,
		ap.appear_date_last - i.filed_date AS days_to_appear_last,

		coalesce(m.motions_num, 0) AS motions_num,

		coalesce(msc.motions_show_cause_num, 0) AS motions_show_cause_num,
		msc.motion_show_cause_date_last,
		msc.motion_show_cause_date_last - i.filed_date AS days_to_show_cause_motion_last,
		msc.motion_show_cause_last_granted,

		coalesce(d.decisions_num, 0) AS decisions_num,
		d.decision_resultof_last,
		d.decision_highlight_last,

		coalesce(j.judgments_num, 0) AS judgments_num,
		j.judgment_type_last,
		j.judgment_last_with_possession,

		coalesce(w.warrants_num, 0) AS warrants_num,
		w.warrant_ordered_date_first,
		w.warrant_ordered_date_last,
		w.warrant_execution_date_last,
		w.warrant_execution_date_last - i.filed_date AS warrant_days_to_execution_last,
		w.warrant_vacated_date_last,
		w.warrant_returned_date_last,
		w.warrant_returned_reason_last

	FROM index AS i
	LEFT JOIN addresses AS ad USING(indexnumberid)
	LEFT JOIN parties AS p USING(indexnumberid)
	LEFT JOIN causes AS c USING(indexnumberid)
	LEFT JOIN events AS e USING(indexnumberid)
	LEFT JOIN appearances AS ap USING(indexnumberid)
	LEFT JOIN motions AS m USING(indexnumberid)
	LEFT JOIN motions_show_cause AS msc USING(indexnumberid)
	LEFT JOIN decisions AS d USING(indexnumberid)
	LEFT JOIN judgments AS j USING(indexnumberid)
	LEFT JOIN warrants AS w USING(indexnumberid)
);

ALTER TABLE oca_case_summary ADD PRIMARY KEY (indexnumberid);
CREATE INDEX ON oca_case_summary (filed_date);
CREATE INDEX ON oca_case_summary (zip5);
