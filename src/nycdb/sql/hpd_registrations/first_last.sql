-- updated to change "anyarray" to "anycompatiblearray" and "anyelement" to "anycompatible" for postgreSQL version > 13


-- Create a function that always returns the first non-NULL item
DROP FUNCTION IF EXISTS public.first_agg ( anyelement, anyelement ) CASCADE;
CREATE OR REPLACE FUNCTION public.first_agg ( anycompatible, anycompatible )
RETURNS anycompatible LANGUAGE SQL IMMUTABLE STRICT AS $$
        SELECT $1;
$$;
 
-- And then wrap an aggregate around it
DROP AGGREGATE IF EXISTS public.FIRST (anyelement) CASCADE;
DROP AGGREGATE IF EXISTS public.FIRST (anycompatible);

CREATE AGGREGATE public.FIRST (
        sfunc    = public.first_agg,
        basetype = anycompatible,
        stype    = anycompatible
);
 
-- Create a function that always returns the last non-NULL item
DROP FUNCTION IF EXISTS public.last_agg ( anyelement, anyelement ) CASCADE;
CREATE OR REPLACE FUNCTION public.last_agg ( anycompatible, anycompatible )
RETURNS anycompatible LANGUAGE SQL IMMUTABLE STRICT AS $$
        SELECT $2;
$$;
 
-- And then wrap an aggregate around it
DROP AGGREGATE IF EXISTS public.LAST ( anyelement ) CASCADE;
DROP AGGREGATE IF EXISTS public.LAST ( anycompatible );
CREATE AGGREGATE public.LAST (
        sfunc    = public.last_agg,
        basetype = anycompatible,
        stype    = anycompatible
);
