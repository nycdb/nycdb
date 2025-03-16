// Dataset detail page component for NYCDB web application
'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Layout from '../../../components/Layout';

interface Field {
  name: string;
  type: string;
  description: string;
  searchable?: boolean;
  filterable?: boolean;
  displayInResults?: boolean;
}

interface Dataset {
  id: string;
  name: string;
  description: string;
  tableName: string;
  category: string;
  fields: Field[];
  sampleQuery?: string;
}

export default function DatasetDetailPage() {
  const params = useParams();
  const router = useRouter();
  const datasetId = params.id as string;
  
  const [dataset, setDataset] = useState<Dataset | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const [searchQuery, setSearchQuery] = useState('');
  const [searchField, setSearchField] = useState('');
  
  useEffect(() => {
    async function fetchDataset() {
      try {
        const response = await fetch(`/api/datasets/${datasetId}`);
        if (!response.ok) {
          throw new Error('Failed to fetch dataset');
        }
        const data = await response.json();
        setDataset(data);
        
        // Set default search field to first searchable field
        if (data.fields && data.fields.length > 0) {
          const searchableField = data.fields.find(f => f.searchable) || data.fields[0];
          setSearchField(searchableField.name);
        }
      } catch (err) {
        setError('Error loading dataset. Please try again later.');
        console.error('Error fetching dataset:', err);
      } finally {
        setLoading(false);
      }
    }
    
    if (datasetId) {
      fetchDataset();
    }
  }, [datasetId]);
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search/${datasetId}?query=${encodeURIComponent(searchQuery)}&field=${encodeURIComponent(searchField)}`);
    }
  };
  
  const searchableFields = dataset?.fields.filter(field => field.searchable) || [];
  const filterableFields = dataset?.fields.filter(field => field.filterable) || [];
  
  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        ) : dataset ? (
          <>
            <div className="mb-6">
              <button 
                onClick={() => router.back()} 
                className="text-blue-600 hover:underline flex items-center"
              >
                &larr; Back to Datasets
              </button>
            </div>
            
            <h1 className="text-3xl font-bold mb-2">{dataset.name}</h1>
            <p className="text-xl text-gray-600 mb-8">{dataset.description}</p>
            
            {/* Search Form */}
            <div className="bg-gray-50 p-6 rounded-lg mb-8">
              <h2 className="text-xl font-semibold mb-4">Search {dataset.name}</h2>
              <form onSubmit={handleSearch} className="space-y-4">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-grow">
                    <label htmlFor="searchQuery" className="block text-sm font-medium text-gray-700 mb-1">
                      Search Term
                    </label>
                    <input
                      id="searchQuery"
                      type="text"
                      placeholder={`Enter search term...`}
                      className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                  </div>
                  
                  <div className="md:w-1/3">
                    <label htmlFor="searchField" className="block text-sm font-medium text-gray-700 mb-1">
                      Search Field
                    </label>
                    <select
                      id="searchField"
                      className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                      value={searchField}
                      onChange={(e) => setSearchField(e.target.value)}
                    >
                      {searchableFields.map(field => (
                        <option key={field.name} value={field.name}>
                          {field.name}
                        </option>
                      ))}
                    </select>
                  </div>
                  
                  <div className="md:self-end">
                    <button
                      type="submit"
                      className="w-full md:w-auto bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      Search
                    </button>
                  </div>
                </div>
              </form>
            </div>
            
            {/* Dataset Fields */}
            <div className="mb-8">
              <h2 className="text-xl font-semibold mb-4">Available Fields</h2>
              <div className="overflow-x-auto">
                <table className="min-w-full bg-white border border-gray-200">
                  <thead>
                    <tr className="bg-gray-100">
                      <th className="py-2 px-4 border-b text-left">Field Name</th>
                      <th className="py-2 px-4 border-b text-left">Type</th>
                      <th className="py-2 px-4 border-b text-left">Description</th>
                      <th className="py-2 px-4 border-b text-left">Searchable</th>
                      <th className="py-2 px-4 border-b text-left">Filterable</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dataset.fields.map(field => (
                      <tr key={field.name} className="hover:bg-gray-50">
                        <td className="py-2 px-4 border-b font-medium">{field.name}</td>
                        <td className="py-2 px-4 border-b">{field.type}</td>
                        <td className="py-2 px-4 border-b">{field.description}</td>
                        <td className="py-2 px-4 border-b">
                          {field.searchable ? '✓' : ''}
                        </td>
                        <td className="py-2 px-4 border-b">
                          {field.filterable ? '✓' : ''}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
            
            {/* Sample Query */}
            {dataset.sampleQuery && (
              <div className="mb-8">
                <h2 className="text-xl font-semibold mb-4">Sample Query</h2>
                <div className="bg-gray-800 text-white p-4 rounded overflow-x-auto">
                  <pre>{dataset.sampleQuery}</pre>
                </div>
              </div>
            )}
          </>
        ) : (
          <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
            Dataset not found
          </div>
        )}
      </div>
    </Layout>
  );
}
