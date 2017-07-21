create role anon;
grant usage on schema public to anon;
grant select on all tables in schema public to anon;
grant execute on all functions in schema public to anon;
