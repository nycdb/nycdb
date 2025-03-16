// Initialize database script for NYCDB web application

import { query } from './db';
import { loadSampleData } from './sample-data';

// Function to initialize the database
export async function initializeDatabase() {
  try {
    console.log('Initializing database...');
    
    // Read the SQL migration file
    const fs = require('fs');
    const path = require('path');
    const sqlPath = path.join(process.cwd(), 'migrations', '0001_initial.sql');
    const sql = fs.readFileSync(sqlPath, 'utf8');
    
    // Execute the SQL to create tables
    await query(sql);
    console.log('Database schema created successfully');
    
    // Load sample data
    const result = await loadSampleData();
    if (result.success) {
      console.log('Sample data loaded successfully');
    } else {
      console.error('Error loading sample data:', result.error);
    }
    
    return { success: true };
  } catch (error) {
    console.error('Error initializing database:', error);
    return { success: false, error };
  }
}

// Export a function to reset the database (for testing)
export async function resetDatabase() {
  try {
    console.log('Resetting database...');
    
    // Drop all tables
    await query(`
      DROP TABLE IF EXISTS pluto_latest CASCADE;
      DROP TABLE IF EXISTS hpd_violations CASCADE;
      DROP TABLE IF EXISTS dob_complaints CASCADE;
      DROP TABLE IF EXISTS hpd_registrations CASCADE;
      DROP TABLE IF EXISTS marshal_evictions CASCADE;
    `);
    
    // Re-initialize
    return await initializeDatabase();
  } catch (error) {
    console.error('Error resetting database:', error);
    return { success: false, error };
  }
}
