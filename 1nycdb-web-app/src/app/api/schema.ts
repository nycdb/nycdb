// Database schema definitions for NYCDB datasets

export interface Dataset {
  id: string;
  name: string;
  description: string;
  tableName: string;
  category: string;
  fields: Field[];
  sampleQuery?: string;
}

export interface Field {
  name: string;
  type: string;
  description: string;
  searchable?: boolean;
  filterable?: boolean;
  displayInResults?: boolean;
}

// Define the datasets we'll support in our web app
export const datasets: Dataset[] = [
  {
    id: 'pluto',
    name: 'PLUTO',
    description: 'Primary Land Use Tax Lot Output - Property data from the Department of City Planning',
    tableName: 'pluto_latest',
    category: 'Property',
    fields: [
      { name: 'bbl', type: 'text', description: 'Borough, Block, and Lot number', searchable: true, filterable: true, displayInResults: true },
      { name: 'address', type: 'text', description: 'Property address', searchable: true, filterable: false, displayInResults: true },
      { name: 'borough', type: 'text', description: 'Borough', searchable: true, filterable: true, displayInResults: true },
      { name: 'block', type: 'integer', description: 'Tax block', searchable: true, filterable: true, displayInResults: true },
      { name: 'lot', type: 'integer', description: 'Tax lot', searchable: true, filterable: true, displayInResults: true },
      { name: 'zipcode', type: 'text', description: 'Zipcode', searchable: true, filterable: true, displayInResults: true },
      { name: 'landuse', type: 'text', description: 'Land use category', searchable: false, filterable: true, displayInResults: true },
      { name: 'yearbuilt', type: 'integer', description: 'Year built', searchable: false, filterable: true, displayInResults: true },
      { name: 'numfloors', type: 'numeric', description: 'Number of floors', searchable: false, filterable: true, displayInResults: true },
      { name: 'unitsres', type: 'integer', description: 'Residential units', searchable: false, filterable: true, displayInResults: true },
    ],
    sampleQuery: 'SELECT * FROM pluto_latest WHERE borough = $1 LIMIT 100'
  },
  {
    id: 'hpd_violations',
    name: 'HPD Violations',
    description: 'Housing violations issued by the Department of Housing Preservation and Development',
    tableName: 'hpd_violations',
    category: 'Violations',
    fields: [
      { name: 'violationid', type: 'text', description: 'Violation ID', searchable: true, filterable: true, displayInResults: true },
      { name: 'bbl', type: 'text', description: 'Borough, Block, and Lot number', searchable: true, filterable: true, displayInResults: true },
      { name: 'building', type: 'text', description: 'Building number', searchable: true, filterable: false, displayInResults: true },
      { name: 'street', type: 'text', description: 'Street name', searchable: true, filterable: false, displayInResults: true },
      { name: 'zip', type: 'text', description: 'Zipcode', searchable: true, filterable: true, displayInResults: true },
      { name: 'apartment', type: 'text', description: 'Apartment', searchable: true, filterable: false, displayInResults: true },
      { name: 'novdescription', type: 'text', description: 'Description of violation', searchable: true, filterable: false, displayInResults: true },
      { name: 'novissuedate', type: 'date', description: 'Date issued', searchable: false, filterable: true, displayInResults: true },
      { name: 'class', type: 'text', description: 'Violation class', searchable: false, filterable: true, displayInResults: true },
      { name: 'currentstatus', type: 'text', description: 'Current status', searchable: false, filterable: true, displayInResults: true },
    ],
    sampleQuery: 'SELECT * FROM hpd_violations WHERE bbl = $1 ORDER BY novissuedate DESC LIMIT 100'
  },
  {
    id: 'dob_complaints',
    name: 'DOB Complaints',
    description: 'Complaints filed with the Department of Buildings',
    tableName: 'dob_complaints',
    category: 'Complaints',
    fields: [
      { name: 'complaintnumber', type: 'text', description: 'Complaint number', searchable: true, filterable: true, displayInResults: true },
      { name: 'bbl', type: 'text', description: 'Borough, Block, and Lot number', searchable: true, filterable: true, displayInResults: true },
      { name: 'housenumber', type: 'text', description: 'House number', searchable: true, filterable: false, displayInResults: true },
      { name: 'streetname', type: 'text', description: 'Street name', searchable: true, filterable: false, displayInResults: true },
      { name: 'zip', type: 'text', description: 'Zipcode', searchable: true, filterable: true, displayInResults: true },
      { name: 'dateentered', type: 'date', description: 'Date entered', searchable: false, filterable: true, displayInResults: true },
      { name: 'status', type: 'text', description: 'Status', searchable: false, filterable: true, displayInResults: true },
      { name: 'description', type: 'text', description: 'Description', searchable: true, filterable: false, displayInResults: true },
    ],
    sampleQuery: 'SELECT * FROM dob_complaints WHERE bbl = $1 ORDER BY dateentered DESC LIMIT 100'
  },
  {
    id: 'hpd_registrations',
    name: 'HPD Registrations',
    description: 'Property registrations with the Department of Housing Preservation and Development',
    tableName: 'hpd_registrations',
    category: 'Property',
    fields: [
      { name: 'registrationid', type: 'text', description: 'Registration ID', searchable: true, filterable: true, displayInResults: true },
      { name: 'bbl', type: 'text', description: 'Borough, Block, and Lot number', searchable: true, filterable: true, displayInResults: true },
      { name: 'housenumber', type: 'text', description: 'House number', searchable: true, filterable: false, displayInResults: true },
      { name: 'streetname', type: 'text', description: 'Street name', searchable: true, filterable: false, displayInResults: true },
      { name: 'zip', type: 'text', description: 'Zipcode', searchable: true, filterable: true, displayInResults: true },
      { name: 'ownername', type: 'text', description: 'Owner name', searchable: true, filterable: false, displayInResults: true },
      { name: 'registrationenddate', type: 'date', description: 'Registration end date', searchable: false, filterable: true, displayInResults: true },
    ],
    sampleQuery: 'SELECT * FROM hpd_registrations WHERE bbl = $1 LIMIT 100'
  },
  {
    id: 'evictions',
    name: 'Marshal Evictions',
    description: 'Eviction data from NYC marshals',
    tableName: 'marshal_evictions',
    category: 'Evictions',
    fields: [
      { name: 'id', type: 'text', description: 'Eviction ID', searchable: true, filterable: true, displayInResults: true },
      { name: 'bbl', type: 'text', description: 'Borough, Block, and Lot number', searchable: true, filterable: true, displayInResults: true },
      { name: 'address', type: 'text', description: 'Address', searchable: true, filterable: false, displayInResults: true },
      { name: 'borough', type: 'text', description: 'Borough', searchable: true, filterable: true, displayInResults: true },
      { name: 'zip', type: 'text', description: 'Zipcode', searchable: true, filterable: true, displayInResults: true },
      { name: 'executeddate', type: 'date', description: 'Date executed', searchable: false, filterable: true, displayInResults: true },
      { name: 'residentialcommercialind', type: 'text', description: 'Residential or Commercial', searchable: false, filterable: true, displayInResults: true },
    ],
    sampleQuery: 'SELECT * FROM marshal_evictions WHERE bbl = $1 ORDER BY executeddate DESC LIMIT 100'
  }
];

// Helper function to get a dataset by ID
export function getDatasetById(id: string): Dataset | undefined {
  return datasets.find(dataset => dataset.id === id);
}

// Helper function to get all searchable fields for a dataset
export function getSearchableFields(datasetId: string): Field[] {
  const dataset = getDatasetById(datasetId);
  return dataset ? dataset.fields.filter(field => field.searchable) : [];
}

// Helper function to get all filterable fields for a dataset
export function getFilterableFields(datasetId: string): Field[] {
  const dataset = getDatasetById(datasetId);
  return dataset ? dataset.fields.filter(field => field.filterable) : [];
}
