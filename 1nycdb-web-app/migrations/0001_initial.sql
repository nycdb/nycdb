-- Initial database schema for NYCDB web application
-- This will create tables for a subset of NYCDB datasets

-- Create schema if it doesn't exist
CREATE SCHEMA IF NOT EXISTS public;

-- PLUTO dataset (simplified schema)
CREATE TABLE IF NOT EXISTS pluto_latest (
    id SERIAL PRIMARY KEY,
    bbl TEXT NOT NULL,
    borough TEXT,
    block INTEGER,
    lot INTEGER,
    address TEXT,
    zipcode TEXT,
    landuse TEXT,
    yearbuilt INTEGER,
    numfloors NUMERIC,
    unitsres INTEGER,
    unitstotal INTEGER,
    ownertype TEXT,
    ownername TEXT,
    assesstot NUMERIC,
    exemptland NUMERIC,
    exempttot NUMERIC,
    CONSTRAINT pluto_bbl_unique UNIQUE (bbl)
);

-- HPD Violations dataset (simplified schema)
CREATE TABLE IF NOT EXISTS hpd_violations (
    id SERIAL PRIMARY KEY,
    violationid TEXT NOT NULL,
    bbl TEXT NOT NULL,
    building TEXT,
    street TEXT,
    zip TEXT,
    apartment TEXT,
    novdescription TEXT,
    novissuedate DATE,
    class TEXT,
    currentstatus TEXT,
    currentstatusdate DATE,
    inspectiondate DATE,
    approveddate DATE,
    communityboard TEXT,
    CONSTRAINT hpd_violations_id_unique UNIQUE (violationid)
);

-- DOB Complaints dataset (simplified schema)
CREATE TABLE IF NOT EXISTS dob_complaints (
    id SERIAL PRIMARY KEY,
    complaintnumber TEXT NOT NULL,
    bbl TEXT,
    housenumber TEXT,
    streetname TEXT,
    zip TEXT,
    dateentered DATE,
    status TEXT,
    description TEXT,
    dispositiondate DATE,
    dispositioncode TEXT,
    inspectiondate DATE,
    communityboard TEXT,
    CONSTRAINT dob_complaints_number_unique UNIQUE (complaintnumber)
);

-- HPD Registrations dataset (simplified schema)
CREATE TABLE IF NOT EXISTS hpd_registrations (
    id SERIAL PRIMARY KEY,
    registrationid TEXT NOT NULL,
    bbl TEXT NOT NULL,
    housenumber TEXT,
    streetname TEXT,
    zip TEXT,
    ownername TEXT,
    ownerbusinessname TEXT,
    owneraddress TEXT,
    registrationenddate DATE,
    lastregistrationdate DATE,
    registrationenddate DATE,
    CONSTRAINT hpd_registrations_id_unique UNIQUE (registrationid)
);

-- Marshal Evictions dataset (simplified schema)
CREATE TABLE IF NOT EXISTS marshal_evictions (
    id SERIAL PRIMARY KEY,
    eviction_id TEXT NOT NULL,
    bbl TEXT,
    address TEXT,
    borough TEXT,
    zip TEXT,
    executeddate DATE,
    residentialcommercialind TEXT,
    CONSTRAINT marshal_evictions_id_unique UNIQUE (eviction_id)
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_pluto_bbl ON pluto_latest (bbl);
CREATE INDEX IF NOT EXISTS idx_hpd_violations_bbl ON hpd_violations (bbl);
CREATE INDEX IF NOT EXISTS idx_dob_complaints_bbl ON dob_complaints (bbl);
CREATE INDEX IF NOT EXISTS idx_hpd_registrations_bbl ON hpd_registrations (bbl);
CREATE INDEX IF NOT EXISTS idx_marshal_evictions_bbl ON marshal_evictions (bbl);

-- Create text search indexes for search functionality
CREATE INDEX IF NOT EXISTS idx_pluto_address_search ON pluto_latest USING gin(to_tsvector('english', address));
CREATE INDEX IF NOT EXISTS idx_hpd_violations_desc_search ON hpd_violations USING gin(to_tsvector('english', novdescription));
CREATE INDEX IF NOT EXISTS idx_dob_complaints_desc_search ON dob_complaints USING gin(to_tsvector('english', description));
