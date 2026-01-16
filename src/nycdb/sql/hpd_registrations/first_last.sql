-- updated to change "anyarray" to "anycompatiblearray" and "anyelement" to "anycompatibleelement" for postgreSQL version > 13


-- Create a function that always returns the first non-NULL item
CREATE OR REPLACE FUNCTION public.first_agg ( anycompatibleelement, anycompatibleelement )
RETURNS anycompatibleelement LANGUAGE SQL IMMUTABLE STRICT AS $$
        SELECT $1;
$$;
 
-- And then wrap an aggregate around it
DROP AGGREGATE IF EXISTS public.FIRST (anycompatibleelement);

CREATE AGGREGATE public.FIRST (
        sfunc    = public.first_agg,
        basetype = anycompatibleelement,
        stype    = anycompatibleelement
);
 
-- Create a function that always returns the last non-NULL item
CREATE OR REPLACE FUNCTION public.last_agg ( anycompatibleelement, anycompatibleelement )
RETURNS anycompatibleelement LANGUAGE SQL IMMUTABLE STRICT AS $$
        SELECT $2;
$$;
 
-- And then wrap an aggregate around it
DROP AGGREGATE IF EXISTS public.LAST ( anycompatibleelement );
CREATE AGGREGATE public.LAST (
        sfunc    = public.last_agg,
        basetype = anycompatibleelement,
        stype    = anycompatibleelement
);
