// Sample data loader for NYCDB web application
// This script will load sample data into the database for testing

import { query } from '../lib/db';

// Sample PLUTO data
const plutoSampleData = [
  {
    bbl: '1000010001',
    borough: 'MANHATTAN',
    block: 1,
    lot: 1,
    address: '1 CENTRE STREET',
    zipcode: '10007',
    landuse: '08',
    yearbuilt: 1950,
    numfloors: 15,
    unitsres: 0,
    unitstotal: 100,
    ownertype: 'C',
    ownername: 'NYC DEPARTMENT OF CITYWIDE ADMINISTRATIVE SERVICES',
    assesstot: 328215000,
    exemptland: 73567000,
    exempttot: 328215000
  },
  {
    bbl: '1000020001',
    borough: 'MANHATTAN',
    block: 2,
    lot: 1,
    address: '1 BROADWAY',
    zipcode: '10004',
    landuse: '05',
    yearbuilt: 1920,
    numfloors: 12,
    unitsres: 0,
    unitstotal: 50,
    ownertype: 'P',
    ownername: 'INTERNATIONAL PLACE LLC',
    assesstot: 125000000,
    exemptland: 0,
    exempttot: 0
  },
  {
    bbl: '3000010001',
    borough: 'BROOKLYN',
    block: 1,
    lot: 1,
    address: '225 ADAMS STREET',
    zipcode: '11201',
    landuse: '05',
    yearbuilt: 1985,
    numfloors: 30,
    unitsres: 0,
    unitstotal: 200,
    ownertype: 'P',
    ownername: 'ADAMS STREET PROPERTIES LLC',
    assesstot: 200000000,
    exemptland: 0,
    exempttot: 0
  },
  {
    bbl: '3002010023',
    borough: 'BROOKLYN',
    block: 201,
    lot: 23,
    address: '123 COURT STREET',
    zipcode: '11201',
    landuse: '03',
    yearbuilt: 1925,
    numfloors: 6,
    unitsres: 25,
    unitstotal: 30,
    ownertype: 'P',
    ownername: 'COURT STREET APARTMENTS LLC',
    assesstot: 15000000,
    exemptland: 0,
    exempttot: 0
  },
  {
    bbl: '2002730001',
    borough: 'BRONX',
    block: 273,
    lot: 1,
    address: '1520 GRAND CONCOURSE',
    zipcode: '10457',
    landuse: '03',
    yearbuilt: 1940,
    numfloors: 6,
    unitsres: 50,
    unitstotal: 55,
    ownertype: 'P',
    ownername: 'GRAND CONCOURSE HOLDINGS LLC',
    assesstot: 8500000,
    exemptland: 0,
    exempttot: 0
  }
];

// Sample HPD Violations data
const hpdViolationsSampleData = [
  {
    violationid: 'V123456',
    bbl: '3002010023',
    building: '123',
    street: 'COURT STREET',
    zip: '11201',
    apartment: '3A',
    novdescription: 'SECTION 27-2005 ADMIN CODE: REPAIR THE BROKEN OR DEFECTIVE PLASTERED SURFACES AND PAINT IN A UNIFORM COLOR CEILING IN THE 1ST ROOM FROM NORTH AT EAST',
    novissuedate: '2024-01-15',
    class: 'B',
    currentstatus: 'OPEN',
    currentstatusdate: '2024-01-15',
    inspectiondate: '2024-01-10',
    approveddate: null,
    communityboard: '302'
  },
  {
    violationid: 'V123457',
    bbl: '3002010023',
    building: '123',
    street: 'COURT STREET',
    zip: '11201',
    apartment: '4B',
    novdescription: 'SECTION 27-2005 ADMIN CODE: PROPERLY REPAIR THE BROKEN OR DEFECTIVE FAUCETS IN THE BATHROOM SINK',
    novissuedate: '2024-01-20',
    class: 'B',
    currentstatus: 'OPEN',
    currentstatusdate: '2024-01-20',
    inspectiondate: '2024-01-18',
    approveddate: null,
    communityboard: '302'
  },
  {
    violationid: 'V123458',
    bbl: '2002730001',
    building: '1520',
    street: 'GRAND CONCOURSE',
    zip: '10457',
    apartment: '2C',
    novdescription: 'SECTION 27-2028 ADMIN CODE: PROVIDE ADEQUATE HEAT FROM 10/1 THROUGH 5/31 FOR DWELLING. MINIMUM TEMPERATURE 68 DEGREES FAHRENHEIT WHEN OUTDOOR TEMPERATURE FALLS BELOW 55 DEGREES',
    novissuedate: '2024-02-01',
    class: 'C',
    currentstatus: 'OPEN',
    currentstatusdate: '2024-02-01',
    inspectiondate: '2024-01-30',
    approveddate: null,
    communityboard: '204'
  },
  {
    violationid: 'V123459',
    bbl: '2002730001',
    building: '1520',
    street: 'GRAND CONCOURSE',
    zip: '10457',
    apartment: '3D',
    novdescription: 'SECTION 27-2017.4 ADMIN CODE: REPAIR OR REPLACE THE CARBON MONOXIDE DETECTING DEVICE(S). SUCH DEVICE(S) SHALL BE INSTALLED WITHIN 15 FEET OF EVERY ROOM USED FOR SLEEPING',
    novissuedate: '2024-02-05',
    class: 'B',
    currentstatus: 'OPEN',
    currentstatusdate: '2024-02-05',
    inspectiondate: '2024-02-03',
    approveddate: null,
    communityboard: '204'
  },
  {
    violationid: 'V123460',
    bbl: '2002730001',
    building: '1520',
    street: 'GRAND CONCOURSE',
    zip: '10457',
    apartment: '5A',
    novdescription: 'SECTION 27-2005 ADMIN CODE: REPAIR THE BROKEN OR DEFECTIVE PLASTERED SURFACES AND PAINT IN A UNIFORM COLOR CEILING IN THE BATHROOM',
    novissuedate: '2024-01-25',
    class: 'A',
    currentstatus: 'CLOSED',
    currentstatusdate: '2024-02-10',
    inspectiondate: '2024-01-23',
    approveddate: '2024-02-10',
    communityboard: '204'
  }
];

// Sample DOB Complaints data
const dobComplaintsSampleData = [
  {
    complaintnumber: 'C123456',
    bbl: '3002010023',
    housenumber: '123',
    streetname: 'COURT STREET',
    zip: '11201',
    dateentered: '2024-01-05',
    status: 'ACTIVE',
    description: 'ILLEGAL CONVERSION: WORK BEING DONE TO CONVERT BASEMENT INTO APARTMENT',
    dispositiondate: null,
    dispositioncode: null,
    inspectiondate: '2024-01-10',
    communityboard: '302'
  },
  {
    complaintnumber: 'C123457',
    bbl: '3002010023',
    housenumber: '123',
    streetname: 'COURT STREET',
    zip: '11201',
    dateentered: '2024-01-15',
    status: 'ACTIVE',
    description: 'ELEVATOR NOT WORKING',
    dispositiondate: null,
    dispositioncode: null,
    inspectiondate: '2024-01-18',
    communityboard: '302'
  },
  {
    complaintnumber: 'C123458',
    bbl: '2002730001',
    housenumber: '1520',
    streetname: 'GRAND CONCOURSE',
    zip: '10457',
    dateentered: '2024-02-01',
    status: 'ACTIVE',
    description: 'FACADE APPEARS UNSAFE WITH LOOSE BRICKS',
    dispositiondate: null,
    dispositioncode: null,
    inspectiondate: '2024-02-05',
    communityboard: '204'
  }
];

// Sample HPD Registrations data
const hpdRegistrationsSampleData = [
  {
    registrationid: 'R123456',
    bbl: '3002010023',
    housenumber: '123',
    streetname: 'COURT STREET',
    zip: '11201',
    ownername: 'JOHN SMITH',
    ownerbusinessname: 'COURT STREET APARTMENTS LLC',
    owneraddress: '100 MAIN STREET, BROOKLYN, NY 11201',
    registrationenddate: '2025-09-01',
    lastregistrationdate: '2023-09-01'
  },
  {
    registrationid: 'R123457',
    bbl: '2002730001',
    housenumber: '1520',
    streetname: 'GRAND CONCOURSE',
    zip: '10457',
    ownername: 'JANE DOE',
    ownerbusinessname: 'GRAND CONCOURSE HOLDINGS LLC',
    owneraddress: '200 BROADWAY, NEW YORK, NY 10007',
    registrationenddate: '2025-06-01',
    lastregistrationdate: '2023-06-01'
  }
];

// Sample Marshal Evictions data
const marshalEvictionsSampleData = [
  {
    eviction_id: 'E123456',
    bbl: '3002010023',
    address: '123 COURT STREET, APT 2B',
    borough: 'BROOKLYN',
    zip: '11201',
    executeddate: '2023-11-15',
    residentialcommercialind: 'RESIDENTIAL'
  },
  {
    eviction_id: 'E123457',
    bbl: '2002730001',
    address: '1520 GRAND CONCOURSE, APT 4C',
    borough: 'BRONX',
    zip: '10457',
    executeddate: '2023-12-01',
    residentialcommercialind: 'RESIDENTIAL'
  }
];

// Function to load sample data
export async function loadSampleData() {
  try {
    console.log('Loading sample data...');
    
    // Load PLUTO data
    for (const item of plutoSampleData) {
      await query(
        `INSERT INTO pluto_latest (
          bbl, borough, block, lot, address, zipcode, landuse, yearbuilt, 
          numfloors, unitsres, unitstotal, ownertype, ownername, assesstot, 
          exemptland, exempttot
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
        ON CONFLICT (bbl) DO NOTHING`,
        [
          item.bbl, item.borough, item.block, item.lot, item.address, 
          item.zipcode, item.landuse, item.yearbuilt, item.numfloors, 
          item.unitsres, item.unitstotal, item.ownertype, item.ownername, 
          item.assesstot, item.exemptland, item.exempttot
        ]
      );
    }
    console.log(`Loaded ${plutoSampleData.length} PLUTO records`);
    
    // Load HPD Violations data
    for (const item of hpdViolationsSampleData) {
      await query(
        `INSERT INTO hpd_violations (
          violationid, bbl, building, street, zip, apartment, novdescription,
          novissuedate, class, currentstatus, currentstatusdate, inspectiondate,
          approveddate, communityboard
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
        ON CONFLICT (violationid) DO NOTHING`,
        [
          item.violationid, item.bbl, item.building, item.street, item.zip,
          item.apartment, item.novdescription, item.novissuedate, item.class,
          item.currentstatus, item.currentstatusdate, item.inspectiondate,
          item.approveddate, item.communityboard
        ]
      );
    }
    console.log(`Loaded ${hpdViolationsSampleData.length} HPD Violations records`);
    
    // Load DOB Complaints data
    for (const item of dobComplaintsSampleData) {
      await query(
        `INSERT INTO dob_complaints (
          complaintnumber, bbl, housenumber, streetname, zip, dateentered,
          status, description, dispositiondate, dispositioncode, inspectiondate,
          communityboard
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        ON CONFLICT (complaintnumber) DO NOTHING`,
        [
          item.complaintnumber, item.bbl, item.housenumber, item.streetname,
          item.zip, item.dateentered, item.status, item.description,
          item.dispositiondate, item.dispositioncode, item.inspectiondate,
          item.communityboard
        ]
      );
    }
    console.log(`Loaded ${dobComplaintsSampleData.length} DOB Complaints records`);
    
    // Load HPD Registrations data
    for (const item of hpdRegistrationsSampleData) {
      await query(
        `INSERT INTO hpd_registrations (
          registrationid, bbl, housenumber, streetname, zip, ownername,
          ownerbusinessname, owneraddress, registrationenddate, lastregistrationdate
        ) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        ON CONFLICT (registrationid) DO NOTHING`,
        [
          item.registrationid, item.bbl, item.housenumber, item.streetname,
          item.zip, item.ownername, item.ownerbusinessname, item.owneraddress,
          item.registrationenddate, item.lastregistrationdate
        ]
      );
    }
    console.log(`Loaded ${hpdRegistrationsSampleData.length} HPD Registrations records`);
    
    // Load Marshal Evictions data
    for (const item of marshalEvictionsSampleData) {
      await query(
        `INSERT INTO marshal_evictions (
          eviction_id, bbl, address, borough, zip, executeddate,
          residentialcommercialind
        ) VALUES ($1, $2, $3, $4, $5, $6, $7)
        ON CONFLICT (eviction_id) DO NOTHING`,
        [
          item.eviction_id, item.bbl, item.address, item.borough,
          item.zip, item.executeddate, item.residentialcommercialind
        ]
      );
    }
    console.log(`Loaded ${marshalEvictionsSampleData.length} Marshal Evictions records`);
    
    console.log('Sample data loading complete!');
    return { success: true };
  } catch (error) {
    console.error('Error loading sample data:', error);
    return { success: false, error };
  }
}

// Export sample data for testing
export {
  plutoSampleData,
  hpdViolationsSampleData,
  dobComplaintsSampleData,
  hpdRegistrationsSampleData,
  marshalEvictionsSampleData
};
