'use client';

import React, { useState, useEffect } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Layout from '../../components/Layout';

interface Dataset {
  id: string;
  name: string;
  description: string;
  category: string;
}

export default function SearchPage() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const initialQuery = searchParams.get('query') || '';
  
  const [query, setQuery] = useState(initialQuery);
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDataset, setSelectedDataset] = useState<string>('');
  const [loading, setLoading] = useState(false);
  
  useEffect(() => {
    async function fetchDatasets() {
      try {
        const response = await fetch('/api/datasets');
        if (!response.ok) {
          throw new Error('Failed to fetch datasets');
        }
        const data = await response.json();
        setDatasets(data);
        
        // Set default dataset if none selected
        if (data.length > 0 && !selectedDataset) {
          setSelectedDataset(data[0].id);
        }
      } catch (err) {
        console.error('Error fetching datasets:', err);
      }
    }
    
    fetchDatasets();
  }, [selectedDataset]);
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim() && selectedDataset) {
      setLoading(true);
      router.push(`/search/${selectedDataset}?query=${encodeURIComponent(query)}`);
    }
  };
  
  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">Search NYC Housing Data</h1>
        
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <form onSubmit={handleSearch} className="space-y-6">
            <div>
              <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-1">
                Search Term
              </label>
              <input
                id="query"
                type="text"
                placeholder="Enter address, BBL, or other search terms..."
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                required
              />
            </div>
            
            <div>
              <label htmlFor="dataset" className="block text-sm font-medium text-gray-700 mb-1">
                Select Dataset
              </label>
              <select
                id="dataset"
                className="w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={selectedDataset}
                onChange={(e) => setSelectedDataset(e.target.value)}
                required
              >
                <option value="" disabled>Select a dataset</option>
                {datasets.map(dataset => (
                  <option key={dataset.id} value={dataset.id}>
                    {dataset.name} - {dataset.description}
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <button
                type="submit"
                className="w-full bg-blue-600 text-white px-6 py-3 rounded hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 flex justify-center items-center"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white mr-2"></div>
                    Searching...
                  </>
                ) : (
                  'Search'
                )}
              </button>
            </div>
          </form>
        </div>
        
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-3">Search Tips</h2>
          <ul className="list-disc pl-5 space-y-2">
            <li>Use a BBL (Borough-Block-Lot) for precise property lookup</li>
            <li>Search by address to find property information</li>
            <li>For violations or complaints, try searching by description keywords</li>
            <li>Select the appropriate dataset for more targeted results</li>
            <li>Use filters on the results page to narrow down your search</li>
          </ul>
        </div>
      </div>
    </Layout>
  );
}
