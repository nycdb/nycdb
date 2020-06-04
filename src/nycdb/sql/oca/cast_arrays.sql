-- In the parsing process there are some columns that are created as text
-- arrays, and when those tables get exported as csv they are formatted as
-- '{"val1", "val2"}' but when you specify an array type in nycdb it simply
-- splits on commas and creates the array. So instead we use simple text type
-- in the nycdb schema and convert them back to arrays here.

ALTER TABLE oca_index
	ALTER COLUMN specialtydesignationtypes TYPE text[] USING specialtydesignationtypes::text[];

ALTER TABLE oca_events
	ALTER COLUMN filingpartiesroles TYPE text[] USING filingpartiesroles::text[];

ALTER TABLE oca_motions
	ALTER COLUMN filingpartiesroles TYPE text[] USING filingpartiesroles::text[];

ALTER TABLE oca_judgments
	ALTER COLUMN creditorsroles TYPE text[] USING creditorsroles::text[],
	ALTER COLUMN debtorsroles TYPE text[] USING debtorsroles::text[];

ALTER TABLE oca_warrants
	ALTER COLUMN propertiesonwarrantcities TYPE text[] USING propertiesonwarrantcities::text[],
	ALTER COLUMN propertiesonwarrantstates TYPE text[] USING propertiesonwarrantstates::text[],
	ALTER COLUMN propertiesonwarrantpostalcodes TYPE text[] USING propertiesonwarrantpostalcodes::text[];
