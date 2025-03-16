// Data access layer for NYCDB web application
// This file contains functions to interact with the database

import { query } from './db';
import { Dataset, getDatasetById } from '../app/api/schema';

// Function to get all datasets
export async function getAllDatasets() {
  try {
    // In a real implementation, this would fetch from the database
    // For now, we'll use our schema definitions
    const { datasets } = await import('../app/api/schema');
    return { success: true, data: datasets };
  } catch (error) {
    console.error('Error fetching datasets:', error);
    return { success: false, error };
  }
}

// Function to search within a dataset
export async function searchDataset(datasetId: string, params: any) {
  try {
    const dataset = getDatasetById(datasetId);
    if (!dataset) {
      return { success: false, error: 'Dataset not found' };
    }

    const { field, query: searchQuery, page = 1, limit = 20 } = params;
    const offset = (page - 1) * limit;
    
    let sqlQuery = '';
    let queryParams: any[] = [];
    
    // Build the appropriate query based on the dataset and search parameters
    switch (datasetId) {
      case 'pluto':
        if (field === 'bbl') {
          sqlQuery = `
            SELECT * FROM pluto_latest 
            WHERE bbl = $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [searchQuery, limit, offset];
        } else if (field === 'address') {
          sqlQuery = `
            SELECT * FROM pluto_latest 
            WHERE address ILIKE $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        } else if (field === 'borough') {
          sqlQuery = `
            SELECT * FROM pluto_latest 
            WHERE borough ILIKE $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        } else {
          // Default to searching across multiple fields
          sqlQuery = `
            SELECT * FROM pluto_latest 
            WHERE bbl LIKE $1 OR address ILIKE $1 OR borough ILIKE $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        }
        break;
        
      case 'hpd_violations':
        if (field === 'bbl') {
          sqlQuery = `
            SELECT * FROM hpd_violations 
            WHERE bbl = $1
            ORDER BY novissuedate DESC
            LIMIT $2 OFFSET $3
          `;
          queryParams = [searchQuery, limit, offset];
        } else if (field === 'violationid') {
          sqlQuery = `
            SELECT * FROM hpd_violations 
            WHERE violationid = $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [searchQuery, limit, offset];
        } else if (field === 'novdescription') {
          sqlQuery = `
            SELECT * FROM hpd_violations 
            WHERE novdescription ILIKE $1
            ORDER BY novissuedate DESC
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        } else {
          // Default to searching across multiple fields
          sqlQuery = `
            SELECT * FROM hpd_violations 
            WHERE bbl LIKE $1 OR violationid LIKE $1 OR novdescription ILIKE $1
            ORDER BY novissuedate DESC
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        }
        break;
        
      case 'dob_complaints':
        if (field === 'bbl') {
          sqlQuery = `
            SELECT * FROM dob_complaints 
            WHERE bbl = $1
            ORDER BY dateentered DESC
            LIMIT $2 OFFSET $3
          `;
          queryParams = [searchQuery, limit, offset];
        } else if (field === 'complaintnumber') {
          sqlQuery = `
            SELECT * FROM dob_complaints 
            WHERE complaintnumber = $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [searchQuery, limit, offset];
        } else if (field === 'description') {
          sqlQuery = `
            SELECT * FROM dob_complaints 
            WHERE description ILIKE $1
            ORDER BY dateentered DESC
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        } else {
          // Default to searching across multiple fields
          sqlQuery = `
            SELECT * FROM dob_complaints 
            WHERE bbl LIKE $1 OR complaintnumber LIKE $1 OR description ILIKE $1
            ORDER BY dateentered DESC
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        }
        break;
        
      case 'hpd_registrations':
        if (field === 'bbl') {
          sqlQuery = `
            SELECT * FROM hpd_registrations 
            WHERE bbl = $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [searchQuery, limit, offset];
        } else if (field === 'registrationid') {
          sqlQuery = `
            SELECT * FROM hpd_registrations 
            WHERE registrationid = $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [searchQuery, limit, offset];
        } else if (field === 'ownername') {
          sqlQuery = `
            SELECT * FROM hpd_registrations 
            WHERE ownername ILIKE $1 OR ownerbusinessname ILIKE $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        } else {
          // Default to searching across multiple fields
          sqlQuery = `
            SELECT * FROM hpd_registrations 
            WHERE bbl LIKE $1 OR registrationid LIKE $1 OR ownername ILIKE $1 OR ownerbusinessname ILIKE $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        }
        break;
        
      case 'evictions':
        if (field === 'bbl') {
          sqlQuery = `
            SELECT * FROM marshal_evictions 
            WHERE bbl = $1
            ORDER BY executeddate DESC
            LIMIT $2 OFFSET $3
          `;
          queryParams = [searchQuery, limit, offset];
        } else if (field === 'eviction_id') {
          sqlQuery = `
            SELECT * FROM marshal_evictions 
            WHERE eviction_id = $1
            LIMIT $2 OFFSET $3
          `;
          queryParams = [searchQuery, limit, offset];
        } else if (field === 'address') {
          sqlQuery = `
            SELECT * FROM marshal_evictions 
            WHERE address ILIKE $1
            ORDER BY executeddate DESC
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        } else {
          // Default to searching across multiple fields
          sqlQuery = `
            SELECT * FROM marshal_evictions 
            WHERE bbl LIKE $1 OR eviction_id LIKE $1 OR address ILIKE $1
            ORDER BY executeddate DESC
            LIMIT $2 OFFSET $3
          `;
          queryParams = [`%${searchQuery}%`, limit, offset];
        }
        break;
        
      default:
        return { success: false, error: 'Invalid dataset' };
    }
    
    // Get the total count for pagination
    const countQuery = sqlQuery.replace(/SELECT \*/, 'SELECT COUNT(*)').split('LIMIT')[0];
    const countResult = await query(countQuery, queryParams.slice(0, -2));
    const total = parseInt(countResult.rows[0].count, 10);
    
    // Execute the search query
    const result = await query(sqlQuery, queryParams);
    
    return { 
      success: true, 
      data: {
        results: result.rows,
        pagination: {
          total,
          page,
          limit,
          pages: Math.ceil(total / limit)
        }
      }
    };
  } catch (error) {
    console.error(`Error searching dataset ${datasetId}:`, error);
    return { success: false, error };
  }
}

// Function to get property information by BBL
export async function getPropertyByBBL(bbl: string) {
  try {
    // Get basic property info from PLUTO
    const plutoQuery = `
      SELECT * FROM pluto_latest 
      WHERE bbl = $1
      LIMIT 1
    `;
    const plutoResult = await query(plutoQuery, [bbl]);
    const plutoData = plutoResult.rows[0] || null;
    
    // Get HPD violations
    const violationsQuery = `
      SELECT * FROM hpd_violations 
      WHERE bbl = $1
      ORDER BY novissuedate DESC
      LIMIT 10
    `;
    const violationsResult = await query(violationsQuery, [bbl]);
    
    // Get violation count
    const violationsCountQuery = `
      SELECT COUNT(*) as total,
             SUM(CASE WHEN currentstatus = 'OPEN' THEN 1 ELSE 0 END) as open
      FROM hpd_violations 
      WHERE bbl = $1
    `;
    const violationsCountResult = await query(violationsCountQuery, [bbl]);
    const violationsCount = violationsCountResult.rows[0] || { total: 0, open: 0 };
    
    // Get DOB complaints
    const complaintsQuery = `
      SELECT * FROM dob_complaints 
      WHERE bbl = $1
      ORDER BY dateentered DESC
      LIMIT 10
    `;
    const complaintsResult = await query(complaintsQuery, [bbl]);
    
    // Get complaints count
    const complaintsCountQuery = `
      SELECT COUNT(*) as total,
             SUM(CASE WHEN status = 'ACTIVE' THEN 1 ELSE 0 END) as open
      FROM dob_complaints 
      WHERE bbl = $1
    `;
    const complaintsCountResult = await query(complaintsCountQuery, [bbl]);
    const complaintsCount = complaintsCountResult.rows[0] || { total: 0, open: 0 };
    
    // Get HPD registration
    const registrationQuery = `
      SELECT * FROM hpd_registrations 
      WHERE bbl = $1
      ORDER BY lastregistrationdate DESC
      LIMIT 1
    `;
    const registrationResult = await query(registrationQuery, [bbl]);
    const registrationData = registrationResult.rows[0] || null;
    
    // Get evictions
    const evictionsQuery = `
      SELECT * FROM marshal_evictions 
      WHERE bbl = $1
      ORDER BY executeddate DESC
      LIMIT 10
    `;
    const evictionsResult = await query(evictionsQuery, [bbl]);
    
    // Get evictions count
    const evictionsCountQuery = `
      SELECT COUNT(*) as total
      FROM marshal_evictions 
      WHERE bbl = $1
    `;
    const evictionsCountResult = await query(evictionsCountQuery, [bbl]);
    const evictionsCount = evictionsCountResult.rows[0]?.total || 0;
    
    // Compile all data
    return {
      success: true,
      data: {
        bbl,
        property: plutoData,
        datasets: {
          pluto: { 
            found: !!plutoData, 
            data: plutoData 
          },
          hpdViolations: { 
            found: violationsResult.rows.length > 0, 
            count: {
              total: parseInt(violationsCount.total, 10),
              open: parseInt(violationsCount.open, 10)
            },
            recent: violationsResult.rows 
          },
          dobComplaints: { 
            found: complaintsResult.rows.length > 0, 
            count: {
              total: parseInt(complaintsCount.total, 10),
              open: parseInt(complaintsCount.open, 10)
            },
            recent: complaintsResult.rows 
          },
          hpdRegistrations: { 
            found: !!registrationData, 
            data: registrationData 
          },
          evictions: { 
            found: evictionsResult.rows.length > 0, 
            count: parseInt(evictionsCount, 10),
            recent: evictionsResult.rows 
          }
        }
      }
    };
  } catch (error) {
    console.error(`Error getting property by BBL ${bbl}:`, error);
    return { success: false, error };
  }
}
