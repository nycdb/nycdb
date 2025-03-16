'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useSearchParams, useRouter } from 'next/navigation';
import Layout from '../../../../components/Layout';

interface FilterOption {
  field: string;
  label: string;
  type: 'select' | 'date' | 'text' | 'checkbox';
  options?: { value: string; label: string }[];
}

export default function SearchFiltersPage() {
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const datasetId = params.datasetId as string;
  const query = searchParams.get('query') || '';
  const field = searchParams.get('field') || '';
  const page = parseInt(searchParams.get('page') || '1', 10);
  
  const [filters, setFilters] = useState<Record<string, any>>({});
  const [availableFilters, setAvailableFilters] = useState<FilterOption[]>([]);
  const [loading, setLoading] = useState(false);
  const [datasetName, setDatasetName] = useState('');
  
  // Define available filters based on dataset
  useEffect(() => {
    async function fetchDatasetInfo() {
      try {
        const response = await fetch(`/api/datasets/${datasetId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch dataset info');
        }
        const data = await response.json();
        setDatasetName(data.name);
        
        // Create filter options based on dataset fields
        const filterOptions: FilterOption[] = [];
        
        if (datasetId === 'pluto') {
          filterOptions.push(
            {
              field: 'borough',
              label: 'Borough',
              type: 'select',
              options: [
                { value: '', label: 'All Boroughs' },
                { value: 'MANHATTAN', label: 'Manhattan' },
                { value: 'BRONX', label: 'Bronx' },
                { value: 'BROOKLYN', label: 'Brooklyn' },
                { value: 'QUEENS', label: 'Queens' },
                { value: 'STATEN ISLAND', label: 'Staten Island' }
              ]
            },
            {
              field: 'yearbuilt_min',
              label: 'Year Built (Min)',
              type: 'text'
            },
            {
              field: 'yearbuilt_max',
              label: 'Year Built (Max)',
              type: 'text'
            },
            {
              field: 'unitsres_min',
              label: 'Residential Units (Min)',
              type: 'text'
            }
          );
        } else if (datasetId === 'hpd_violations') {
          filterOptions.push(
            {
              field: 'class',
              label: 'Violation Class',
              type: 'select',
              options: [
                { value: '', label: 'All Classes' },
                { value: 'A', label: 'Class A (Non-Hazardous)' },
                { value: 'B', label: 'Class B (Hazardous)' },
                { value: 'C', label: 'Class C (Immediately Hazardous)' }
              ]
            },
            {
              field: 'status',
              label: 'Status',
              type: 'select',
              options: [
                { value: '', label: 'All Statuses' },
                { value: 'OPEN', label: 'Open' },
                { value: 'CLOSED', label: 'Closed' }
              ]
            },
            {
              field: 'novissuedate_min',
              label: 'Issue Date (From)',
              type: 'date'
            },
            {
              field: 'novissuedate_max',
              label: 'Issue Date (To)',
              type: 'date'
            }
          );
        } else if (datasetId === 'dob_complaints') {
          filterOptions.push(
            {
              field: 'status',
              label: 'Status',
              type: 'select',
              options: [
                { value: '', label: 'All Statuses' },
                { value: 'ACTIVE', label: 'Active' },
                { value: 'CLOSED', label: 'Closed' }
              ]
            },
            {
              field: 'dateentered_min',
              label: 'Date Entered (From)',
              type: 'date'
            },
            {
              field: 'dateentered_max',
              label: 'Date Entered (To)',
              type: 'date'
            }
          );
        } else if (datasetId === 'evictions') {
          filterOptions.push(
            {
              field: 'executeddate_min',
              label: 'Executed Date (From)',
              type: 'date'
            },
            {
              field: 'executeddate_max',
              label: 'Executed Date (To)',
              type: 'date'
            },
            {
              field: 'residentialcommercialind',
              label: 'Type',
              type: 'select',
              options: [
                { value: '', label: 'All Types' },
                { value: 'RESIDENTIAL', label: 'Residential' },
                { value: 'COMMERCIAL', label: 'Commercial' }
              ]
            }
          );
        }
        
        // Add borough filter to all datasets except pluto (which already has it)
        if (datasetId !== 'pluto') {
          filterOptions.unshift({
            field: 'borough',
            label: 'Borough',
            type: 'select',
            options: [
              { value: '', label: 'All Boroughs' },
              { value: 'MANHATTAN', label: 'Manhattan' },
              { value: 'BRONX', label: 'Bronx' },
              { value: 'BROOKLYN', label: 'Brooklyn' },
              { value: 'QUEENS', label: 'Queens' },
              { value: 'STATEN ISLAND', label: 'Staten Island' }
            ]
          });
        }
        
        setAvailableFilters(filterOptions);
        
        // Initialize filters from URL params
        const initialFilters: Record<string, any> = {};
        filterOptions.forEach(filter => {
          const paramValue = searchParams.get(filter.field);
          if (paramValue) {
            initialFilters[filter.field] = paramValue;
          }
        });
        
        setFilters(initialFilters);
      } catch (err) {
        console.error('Error fetching dataset info:', err);
      }
    }
    
    if (datasetId) {
      fetchDatasetInfo();
    }
  }, [datasetId, searchParams]);
  
  const handleFilterChange = (field: string, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };
  
  const applyFilters = () => {
    setLoading(true);
    
    // Build URL with all search params and filters
    const urlParams = new URLSearchParams();
    urlParams.set('query', query);
    if (field) urlParams.set('field', field);
    urlParams.set('page', '1'); // Reset to page 1 when applying filters
    
    // Add all active filters to URL
    Object.entries(filters).forEach(([key, value]) => {
      if (value) {
        urlParams.set(key, String(value));
      }
    });
    
    router.push(`/search/${datasetId}?${urlParams.toString()}`);
  };
  
  const clearFilters = () => {
    setFilters({});
    
    // Build URL with only search params, no filters
    const urlParams = new URLSearchParams();
    urlParams.set('query', query);
    if (field) urlParams.set('field', field);
    urlParams.set('page', '1');
    
    router.push(`/search/${datasetId}?${urlParams.toString()}`);
  };
  
  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <button 
            onClick={() => router.back()} 
            className="text-blue-600 hover:underline flex items-center"
          >
            &larr; Back to Search Results
          </button>
        </div>
        
        <h1 className="text-2xl font-bold mb-6">
          Filter Results: "{query}" in {datasetName || datasetId}
        </h1>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {availableFilters.map(filter => (
              <div key={filter.field} className="space-y-2">
                <label htmlFor={filter.field} className="block text-sm font-medium text-gray-700">
                  {filter.label}
                </label>
                
                {filter.type === 'select' && (
                  <select
                    id={filter.field}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={filters[filter.field] || ''}
                    onChange={(e) => handleFilterChange(filter.field, e.target.value)}
                  >
                    {filter.options?.map(option => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                )}
                
                {filter.type === 'date' && (
                  <input
                    id={filter.field}
                    type="date"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={filters[filter.field] || ''}
                    onChange={(e) => handleFilterChange(filter.field, e.target.value)}
                  />
                )}
                
                {filter.type === 'text' && (
                  <input
                    id={filter.field}
                    type="text"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    value={filters[filter.field] || ''}
                    onChange={(e) => handleFilterChange(filter.field, e.target.value)}
                    placeholder={`Enter ${filter.label.toLowerCase()}`}
                  />
                )}
                
                {filter.type === 'checkbox' && (
                  <div className="flex items-center">
                    <input
                      id={filter.field}
                      type="checkbox"
                      className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      checked={!!filters[filter.field]}
                      onChange={(e) => handleFilterChange(filter.field, e.target.checked)}
                    />
                    <label htmlFor={filter.field} className="ml-2 block text-sm text-gray-900">
                      {filter.label}
                    </label>
                  </div>
                )}
              </div>
            ))}
          </div>
          
          <div className="mt-8 flex justify-between">
            <button
              type="button"
              onClick={clearFilters}
              className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Clear Filters
            </button>
            
            <button
              type="button"
              onClick={applyFilters}
              className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              disabled={loading}
            >
              {loading ? 'Applying...' : 'Apply Filters'}
            </button>
          </div>
        </div>
      </div>
    </Layout>
  );
}
