-- This aggregate function returns the value from the first or last input row 
-- in each group, ignoring NULL rows. 

-- NOTE: NULLs are ignored automatically by the STRICT declaration, documented here:
-- https://www.postgresql.org/docs/current/sql-createaggregate.html

-- FROM: https://wiki.postgresql.org/wiki/First/last_(aggregate)

-- Create a function that always returns the first non-NULL item
DROP FUNCTION IF EXISTS public.first_agg(anyelement, anyelement) CASCADE;
CREATE OR REPLACE FUNCTION public.first_agg ( anyelement, anyelement )
RETURNS anyelement LANGUAGE SQL IMMUTABLE STRICT AS $$
        SELECT $1;
$$;
 
-- And then wrap an aggregate around it
CREATE AGGREGATE public.FIRST (
        sfunc    = public.first_agg,
        basetype = anyelement,
        stype    = anyelement
);
 
-- Create a function that always returns the last non-NULL item
DROP FUNCTION IF EXISTS public.last_agg(anyelement, anyelement) CASCADE;
CREATE OR REPLACE FUNCTION public.last_agg ( anyelement, anyelement )
RETURNS anyelement LANGUAGE SQL IMMUTABLE STRICT AS $$
        SELECT $2;
$$;
 
-- And then wrap an aggregate around it
CREATE AGGREGATE public.LAST (
        sfunc    = public.last_agg,
        basetype = anyelement,
        stype    = anyelement
);
