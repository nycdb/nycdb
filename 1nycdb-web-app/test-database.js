// Test script for database connection and initialization
const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

// Database connection configuration
const dbConfig = {
  user: 'nycdb',
  password: 'nycdb',
  host: 'localhost',
  port: 5432,
  database: 'nycdb',
};

// Create a new pool instance
const pool = new Pool(dbConfig);

async function testDatabaseConnection() {
  console.log('Testing database connection...');
  
  try {
    // Test connection
    const client = await pool.connect();
    console.log('✅ Successfully connected to PostgreSQL database');
    
    // Test query
    const result = await client.query('SELECT NOW() as time');
    console.log(`✅ Database query successful. Server time: ${result.rows[0].time}`);
    
    // Release client
    client.release();
    
    return true;
  } catch (error) {
    console.error('❌ Database connection test failed:', error.message);
    return false;
  }
}

async function testDatabaseSchema() {
  console.log('\nTesting database schema...');
  
  try {
    // Check if tables exist
    const tables = ['pluto_latest', 'hpd_violations', 'dob_complaints', 'hpd_registrations', 'marshal_evictions'];
    
    for (const table of tables) {
      const result = await pool.query(`
        SELECT EXISTS (
          SELECT FROM information_schema.tables 
          WHERE table_schema = 'public' 
          AND table_name = $1
        )
      `, [table]);
      
      if (result.rows[0].exists) {
        console.log(`✅ Table '${table}' exists`);
      } else {
        console.log(`❌ Table '${table}' does not exist`);
      }
    }
    
    return true;
  } catch (error) {
    console.error('❌ Database schema test failed:', error.message);
    return false;
  }
}

async function testSampleData() {
  console.log('\nTesting sample data...');
  
  try {
    // Check if sample data exists in each table
    const tables = ['pluto_latest', 'hpd_violations', 'dob_complaints', 'hpd_registrations', 'marshal_evictions'];
    
    for (const table of tables) {
      const result = await pool.query(`SELECT COUNT(*) FROM ${table}`);
      const count = parseInt(result.rows[0].count, 10);
      
      if (count > 0) {
        console.log(`✅ Table '${table}' has ${count} records`);
      } else {
        console.log(`❌ Table '${table}' has no records`);
      }
    }
    
    return true;
  } catch (error) {
    console.error('❌ Sample data test failed:', error.message);
    return false;
  }
}

async function testSearchQuery() {
  console.log('\nTesting search query...');
  
  try {
    // Test a search query on pluto_latest
    const result = await pool.query(`
      SELECT * FROM pluto_latest 
      WHERE borough ILIKE $1
      LIMIT 5
    `, ['%MANHATTAN%']);
    
    if (result.rows.length > 0) {
      console.log(`✅ Search query returned ${result.rows.length} results`);
      console.log('Sample result:', result.rows[0]);
    } else {
      console.log('❌ Search query returned no results');
    }
    
    return true;
  } catch (error) {
    console.error('❌ Search query test failed:', error.message);
    return false;
  }
}

async function runTests() {
  console.log('=== NYCDB Web App Database Tests ===\n');
  
  try {
    // Run all tests
    const connectionSuccess = await testDatabaseConnection();
    if (!connectionSuccess) {
      console.error('Database connection failed. Aborting remaining tests.');
      return;
    }
    
    await testDatabaseSchema();
    await testSampleData();
    await testSearchQuery();
    
    console.log('\n=== Test Summary ===');
    console.log('Database connection and functionality tests completed.');
    
  } catch (error) {
    console.error('Test execution failed:', error);
  } finally {
    // End pool
    await pool.end();
  }
}

// Run the tests
runTests();
