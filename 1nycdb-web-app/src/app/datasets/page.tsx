// Datasets page component for NYCDB web application
'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import Layout from '../../components/Layout';

interface Dataset {
  id: string;
  name: string;
  description: string;
  category: string;
}

export default function DatasetsPage() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  useEffect(() => {
    async function fetchDatasets() {
      try {
        const response = await fetch('/api/datasets');
        if (!response.ok) {
          throw new Error('Failed to fetch datasets');
        }
        const data = await response.json();
        setDatasets(data);
      } catch (err) {
        setError('Error loading datasets. Please try again later.');
        console.error('Error fetching datasets:', err);
      } finally {
        setLoading(false);
      }
    }
    
    fetchDatasets();
  }, []);
  
  // Group datasets by category
  const datasetsByCategory: Record<string, Dataset[]> = {};
  datasets.forEach(dataset => {
    if (!datasetsByCategory[dataset.category]) {
      datasetsByCategory[dataset.category] = [];
    }
    datasetsByCategory[dataset.category].push(dataset);
  });
  
  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-6">NYC Housing Datasets</h1>
        
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        ) : (
          <div className="space-y-8">
            {Object.entries(datasetsByCategory).map(([category, categoryDatasets]) => (
              <div key={category} className="border border-gray-200 rounded-lg p-6">
                <h2 className="text-xl font-semibold mb-4 text-blue-700">{category}</h2>
                <div className="space-y-4">
                  {categoryDatasets.map(dataset => (
                    <div key={dataset.id} className="border-b border-gray-100 pb-4 last:border-b-0 last:pb-0">
                      <Link href={`/datasets/${dataset.id}`} className="text-lg font-medium text-blue-600 hover:underline">
                        {dataset.name}
                      </Link>
                      <p className="text-gray-600 mt-1">{dataset.description}</p>
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        )}
        
        <div className="mt-8 bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-3">About These Datasets</h2>
          <p className="mb-4">
            These datasets are sourced from various NYC government agencies and compiled by NYCDB.
            They provide information about properties, violations, complaints, and other housing-related data.
          </p>
          <p>
            <a 
              href="https://github.com/nycdb/nycdb" 
              className="text-blue-600 hover:underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              Learn more about NYCDB on GitHub
            </a>
          </p>
        </div>
      </div>
    </Layout>
  );
}
