// Enhanced search functionality for the search results page
'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import Layout from '../../../../components/Layout';

interface SearchResult {
  [key: string]: any;
}

interface Pagination {
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export default function SearchResultsPage() {
  const params = useParams();
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const datasetId = params.datasetId as string;
  const query = searchParams.get('query') || '';
  const field = searchParams.get('field') || '';
  const page = parseInt(searchParams.get('page') || '1', 10);
  
  const [results, setResults] = useState<SearchResult[]>([]);
  const [pagination, setPagination] = useState<Pagination>({
    total: 0,
    page: 1,
    limit: 20,
    pages: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [datasetName, setDatasetName] = useState('');
  const [activeFilters, setActiveFilters] = useState<string[]>([]);
  const [sortField, setSortField] = useState('');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');
  
  // Get all search params except pagination
  const getFilterParams = () => {
    const filters: Record<string, string> = {};
    searchParams.forEach((value, key) => {
      if (key !== 'page' && key !== 'query' && key !== 'field') {
        filters[key] = value;
      }
    });
    return filters;
  };
  
  useEffect(() => {
    async function fetchDatasetInfo() {
      try {
        const response = await fetch(`/api/datasets/${datasetId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch dataset info');
        }
        const data = await response.json();
        setDatasetName(data.name);
        
        // Set default sort field based on dataset
        if (!sortField) {
          if (datasetId === 'pluto') {
            setSortField('bbl');
          } else if (datasetId === 'hpd_violations') {
            setSortField('novissuedate');
          } else if (datasetId === 'dob_complaints') {
            setSortField('dateentered');
          } else if (datasetId === 'evictions') {
            setSortField('executeddate');
          } else {
            setSortField('id');
          }
        }
      } catch (err) {
        console.error('Error fetching dataset info:', err);
      }
    }
    
    fetchDatasetInfo();
  }, [datasetId, sortField]);
  
  useEffect(() => {
    // Get active filters from URL
    const filters = getFilterParams();
    const filterLabels = Object.entries(filters).map(([key, value]) => {
      // Format the filter label for display
      const formattedKey = key.replace(/_/g, ' ').replace(/min|max/g, '');
      return `${formattedKey}: ${value}`;
    });
    setActiveFilters(filterLabels);
    
    async function fetchSearchResults() {
      setLoading(true);
      try {
        // Build URL with all search params and filters
        const urlParams = new URLSearchParams();
        urlParams.set('query', query);
        if (field) urlParams.set('field', field);
        urlParams.set('page', page.toString());
        urlParams.set('limit', '20');
        
        // Add sort parameters
        if (sortField) {
          urlParams.set('sort', sortField);
          urlParams.set('direction', sortDirection);
        }
        
        // Add all filters from URL
        Object.entries(filters).forEach(([key, value]) => {
          urlParams.set(key, value);
        });
        
        const response = await fetch(
          `/api/search/${datasetId}?${urlParams.toString()}`
        );
        
        if (!response.ok) {
          throw new Error('Failed to fetch search results');
        }
        
        const data = await response.json();
        setResults(data.results || []);
        setPagination({
          total: data.pagination?.total || 0,
          page: data.pagination?.page || 1,
          limit: data.pagination?.limit || 20,
          pages: data.pagination?.pages || 0
        });
      } catch (err) {
        setError('Error loading search results. Please try again later.');
        console.error('Error fetching search results:', err);
      } finally {
        setLoading(false);
      }
    }
    
    if (datasetId && query) {
      fetchSearchResults();
    }
  }, [datasetId, query, field, page, sortField, sortDirection, searchParams]);
  
  const handlePageChange = (newPage: number) => {
    // Preserve all existing params, just update the page
    const urlParams = new URLSearchParams(searchParams.toString());
    urlParams.set('page', newPage.toString());
    router.push(`/search/${datasetId}?${urlParams.toString()}`);
  };
  
  const handleSortChange = (field: string) => {
    // If clicking the same field, toggle direction
    if (field === sortField) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      // New field, default to descending
      setSortField(field);
      setSortDirection('desc');
    }
  };
  
  const handleFilterClick = () => {
    // Navigate to filters page, preserving all current params
    router.push(`/search/${datasetId}/filters?${searchParams.toString()}`);
  };
  
  const removeFilter = (filterIndex: number) => {
    // Get the filter key to remove
    const filterKey = Object.keys(getFilterParams())[filterIndex];
    if (!filterKey) return;
    
    // Create new URL params without this filter
    const urlParams = new URLSearchParams(searchParams.toString());
    urlParams.delete(filterKey);
    urlParams.set('page', '1'); // Reset to page 1 when removing filters
    
    router.push(`/search/${datasetId}?${urlParams.toString()}`);
  };
  
  const getDisplayableFields = (result: SearchResult) => {
    // Exclude internal fields and show the most important fields first
    const priorityFields = ['bbl', 'address', 'borough', 'violationid', 'complaintnumber', 'eviction_id'];
    const excludeFields = ['id'];
    
    const allFields = Object.keys(result).filter(key => !excludeFields.includes(key));
    
    // Sort fields to show priority fields first
    return allFields.sort((a, b) => {
      const aIndex = priorityFields.indexOf(a);
      const bIndex = priorityFields.indexOf(b);
      
      if (aIndex >= 0 && bIndex >= 0) return aIndex - bIndex;
      if (aIndex >= 0) return -1;
      if (bIndex >= 0) return 1;
      return a.localeCompare(b);
    });
  };
  
  const getSortableFields = (result: SearchResult) => {
    // Return fields that make sense to sort by
    const fields = Object.keys(result);
    const sortableTypes = ['string', 'number'];
    
    return fields.filter(field => {
      const value = result[field];
      return value !== null && sortableTypes.includes(typeof value);
    });
  };
  
  const exportResults = () => {
    // In a real implementation, this would generate and download a CSV
    alert('In a production environment, this would download a CSV of the current results.');
  };
  
  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <button 
            onClick={() => router.back()} 
            className="text-blue-600 hover:underline flex items-center"
          >
            &larr; Back to {datasetName || 'Dataset'}
          </button>
        </div>
        
        <h1 className="text-2xl font-bold mb-2">
          Search Results: "{query}" in {datasetName || datasetId}
        </h1>
        
        <div className="mb-6">
          <p className="text-gray-600">
            {pagination.total} results found
            {field && ` for field "${field}"`}
          </p>
          
          <div className="mt-4 flex flex-wrap items-center gap-2">
            {field && (
              <span className="inline-block bg-blue-100 text-blue-800 text-sm px-2 py-1 rounded">
                Field: {field}
              </span>
            )}
            
            {activeFilters.map((filter, index) => (
              <span 
                key={index} 
                className="inline-flex items-center bg-gray-100 text-gray-800 text-sm px-2 py-1 rounded"
              >
                {filter}
                <button 
                  onClick={() => removeFilter(index)}
                  className="ml-1 text-gray-500 hover:text-gray-700"
                >
                  &times;
                </button>
              </span>
            ))}
            
            <button
              onClick={handleFilterClick}
              className="inline-flex items-center bg-white border border-gray-300 text-gray-700 text-sm px-3 py-1 rounded hover:bg-gray-50"
            >
              <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
              </svg>
              {activeFilters.length > 0 ? 'Modify Filters' : 'Add Filters'}
            </button>
          </div>
        </div>
        
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        ) : results.length > 0 ? (
          <>
            <div className="overflow-x-auto bg-white rounded-lg shadow mb-6">
              <table className="min-w-full">
                <thead>
                  <tr className="bg-gray-100 border-b">
                    {results.length > 0 && getDisplayableFields(results[0]).map(field => (
                      <th 
                        key={field} 
                        className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                      >
                        <button 
                          className="flex items-center focus:outline-none"
                          onClick={() => handleSortChange(field)}
                        >
                          {field}
                          {sortField === field && (
                            <span className="ml-1">
                              {sortDirection === 'asc' ? '↑' : '↓'}
                            </span>
                          )}
                        </button>
                      </th>
                    ))}
                    <th className="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {results.map((result, index) => (
                    <tr key={index} className="border-b hover:bg-gray-50">
                      {getDisplayableFields(result).map(field => (
                        <td key={field} className="py-3 px-4 whitespace-nowrap">
                          {result[field] !== null ? String(result[field]) : ''}
                        </td>
                      ))}
                      <td className="py-3 px-4 whitespace-nowrap">
                        {result.bbl && (
                          <a 
                            href={`/property/${result.bbl}`}
                            className="text-blue-600 hover:underline"
                          >
                            View Property
                          </a>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            
            {/* Pagination */}
            {pagination.pages > 1 && (
              <div className="flex justify-between items-center mb-6">
                <button
                  onClick={() => handlePageChange(pagination.page - 1)}
                  disabled={pagination.page === 1}
                  className={`px-4 py-2 border rounded ${
                    pagination.page === 1 
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                      : 'bg-white text-blue-600 hover:bg-blue-50'
                  }`}
                >
                  &larr; Previous
                </button>
                
                <span className="text-gray-600">
                  Page {pagination.page} of {pagination.pages}
                </span>
                
                <button
                  onClick={() => handlePageChange(pagination.page + 1)}
                  disabled={pagination.page === pagination.pages}
                  className={`px-4 py-2 border rounded ${
                    pagination.page === pagination.pages 
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                      : 'bg-white text-blue-600 hover:bg-blue-50'
                  }`}
                >
                  Next &rarr;
                </button>
              </div>
            )}
            
            {/* Export Button */}
            <div className="text-right">
              <button
                className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
                onClick={exportResults}
              >
                Export CSV
              </button>
            </div>
          </>
        ) : (
          <div className="bg-yellow-50 border border-yellow-200 text-yellow-800 px-4 py-8 rounded text-center">
            <h3 className="text-lg font-medium mb-2">No results found</h3>
            <p>Try adjusting your search query or removing some filters.</p>
          </div>
        )}
      </div>
    </Layout>
  );
}
