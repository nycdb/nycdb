'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Layout from '../../../components/Layout';

interface PropertyData {
  bbl: string;
  property: any;
  datasets: {
    pluto: { found: boolean; data: any };
    hpdViolations: { found: boolean; count: { total: number; open: number }; recent: any[] };
    dobComplaints: { found: boolean; count: { total: number; open: number }; recent: any[] };
    hpdRegistrations: { found: boolean; data: any };
    evictions: { found: boolean; count: number; recent: any[] };
  };
}

export default function PropertyDetailPage() {
  const params = useParams();
  const router = useRouter();
  const bbl = params.bbl as string;
  
  const [propertyData, setPropertyData] = useState<PropertyData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('overview');
  
  useEffect(() => {
    async function fetchPropertyData() {
      setLoading(true);
      try {
        const response = await fetch(`/api/property/${bbl}`);
        
        if (!response.ok) {
          throw new Error('Failed to fetch property data');
        }
        
        const data = await response.json();
        setPropertyData(data);
      } catch (err) {
        setError('Error loading property information. Please try again later.');
        console.error('Error fetching property data:', err);
      } finally {
        setLoading(false);
      }
    }
    
    if (bbl) {
      fetchPropertyData();
    }
  }, [bbl]);
  
  const formatDate = (dateString: string) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  };
  
  const getViolationClass = (violationClass: string) => {
    switch (violationClass) {
      case 'A':
        return 'bg-yellow-100 text-yellow-800';
      case 'B':
        return 'bg-orange-100 text-orange-800';
      case 'C':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };
  
  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        <div className="mb-6">
          <button 
            onClick={() => router.back()} 
            className="text-blue-600 hover:underline flex items-center"
          >
            &larr; Back to Search Results
          </button>
        </div>
        
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
          </div>
        ) : error ? (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        ) : propertyData ? (
          <>
            <h1 className="text-3xl font-bold mb-2">
              {propertyData.property?.address || 'Property'} 
              <span className="text-gray-500 ml-2 text-xl">(BBL: {bbl})</span>
            </h1>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {/* Property Info Card */}
              <div className="bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold mb-4">Property Info</h2>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">Borough:</span>
                    <span className="font-medium">{propertyData.property?.borough || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Block:</span>
                    <span className="font-medium">{propertyData.property?.block || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Lot:</span>
                    <span className="font-medium">{propertyData.property?.lot || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Zip Code:</span>
                    <span className="font-medium">{propertyData.property?.zipcode || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Year Built:</span>
                    <span className="font-medium">{propertyData.property?.yearbuilt || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Building Class:</span>
                    <span className="font-medium">{propertyData.property?.buildingclass || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Land Use:</span>
                    <span className="font-medium">{propertyData.property?.landuse || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Residential Units:</span>
                    <span className="font-medium">{propertyData.property?.unitsres || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Total Units:</span>
                    <span className="font-medium">{propertyData.property?.unitstotal || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">Owner:</span>
                    <span className="font-medium">{propertyData.property?.ownername || 'N/A'}</span>
                  </div>
                </div>
              </div>
              
              {/* Building Map Placeholder */}
              <div className="md:col-span-2 bg-white rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold mb-4">Building Map</h2>
                <div className="bg-gray-100 h-64 flex items-center justify-center rounded">
                  <p className="text-gray-500">Map would be displayed here</p>
                </div>
              </div>
            </div>
            
            {/* Tabs */}
            <div className="mb-6">
              <div className="border-b border-gray-200">
                <nav className="flex -mb-px">
                  <button
                    onClick={() => setActiveTab('overview')}
                    className={`py-4 px-6 font-medium text-sm ${
                      activeTab === 'overview'
                        ? 'border-b-2 border-blue-500 text-blue-600'
                        : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Overview
                  </button>
                  <button
                    onClick={() => setActiveTab('violations')}
                    className={`py-4 px-6 font-medium text-sm ${
                      activeTab === 'violations'
                        ? 'border-b-2 border-blue-500 text-blue-600'
                        : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Violations
                  </button>
                  <button
                    onClick={() => setActiveTab('complaints')}
                    className={`py-4 px-6 font-medium text-sm ${
                      activeTab === 'complaints'
                        ? 'border-b-2 border-blue-500 text-blue-600'
                        : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Complaints
                  </button>
                  <button
                    onClick={() => setActiveTab('evictions')}
                    className={`py-4 px-6 font-medium text-sm ${
                      activeTab === 'evictions'
                        ? 'border-b-2 border-blue-500 text-blue-600'
                        : 'text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    Evictions
                  </button>
                </nav>
              </div>
            </div>
            
            {/* Tab Content */}
            <div className="bg-white rounded-lg shadow p-6">
              {activeTab === 'overview' && (
                <div>
                  <h2 className="text-xl font-semibold mb-4">Property Overview</h2>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {/* HPD Violations Summary */}
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h3 className="text-lg font-medium mb-2">HPD Violations</h3>
                      <div className="flex justify-between mb-2">
                        <span>Open violations:</span>
                        <span className="font-bold text-red-600">
                          {propertyData.datasets.hpdViolations.count.open}
                        </span>
                      </div>
                      <div className="flex justify-between mb-4">
                        <span>Total violations:</span>
                        <span className="font-bold">
                          {propertyData.datasets.hpdViolations.count.total}
                        </span>
                      </div>
                      <button
                        onClick={() => setActiveTab('violations')}
                        className="text-blue-600 hover:underline text-sm"
                      >
                        View all violations
                      </button>
                    </div>
                    
                    {/* DOB Complaints Summary */}
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h3 className="text-lg font-medium mb-2">DOB Complaints</h3>
                      <div className="flex justify-between mb-2">
                        <span>Open complaints:</span>
                        <span className="font-bold text-red-600">
                          {propertyData.datasets.dobComplaints.count.open}
                        </span>
                      </div>
                      <div className="flex justify-between mb-4">
                        <span>Total complaints:</span>
                        <span className="font-bold">
                          {propertyData.datasets.dobComplaints.count.total}
                        </span>
                      </div>
                      <button
                        onClick={() => setActiveTab('complaints')}
                        className="text-blue-600 hover:underline text-sm"
                      >
                        View all complaints
                      </button>
                    </div>
                    
                    {/* HPD Registration */}
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h3 className="text-lg font-medium mb-2">HPD Registration</h3>
                      {propertyData.datasets.hpdRegistrations.found ? (
                        <>
                          <div className="flex justify-between mb-2">
                            <span>Registration ID:</span>
                            <span className="font-medium">
                              {propertyData.datasets.hpdRegistrations.data?.registrationid || 'N/A'}
                            </span>
                          </div>
                          <div className="flex justify-between mb-2">
                            <span>Owner:</span>
                            <span className="font-medium">
                              {propertyData.datasets.hpdRegistrations.data?.ownername || 'N/A'}
                            </span>
                          </div>
                          <div className="flex justify-between mb-2">
                            <span>Business:</span>
                            <span className="font-medium">
                              {propertyData.datasets.hpdRegistrations.data?.ownerbusinessname || 'N/A'}
                            </span>
                          </div>
                          <div className="flex justify-between">
                            <span>Expires:</span>
                            <span className="font-medium">
                              {formatDate(propertyData.datasets.hpdRegistrations.data?.registrationenddate)}
                            </span>
                          </div>
                        </>
                      ) : (
                        <p className="text-gray-500">No registration found</p>
                      )}
                    </div>
                    
                    {/* Evictions Summary */}
                    <div className="border border-gray-200 rounded-lg p-4">
                      <h3 className="text-lg font-medium mb-2">Evictions</h3>
                      <div className="flex justify-between mb-4">
                        <span>Total evictions:</span>
                        <span className="font-bold">
                          {propertyData.datasets.evictions.count}
                        </span>
                      </div>
                      {propertyData.datasets.evictions.found ? (
                        <button
                          onClick={() => setActiveTab('evictions')}
                          className="text-blue-600 hover:underline text-sm"
                        >
                          View all evictions
                        </button>
                      ) : (
                        <p className="text-gray-500">No evictions found</p>
                      )}
                    </div>
                  </div>
                </div>
              )}
              
              {activeTab === 'violations' && (
                <div>
                  <h2 className="text-xl font-semibold mb-4">HPD Violations</h2>
                  
                  {propertyData.datasets.hpdViolations.found ? (
                    <>
                      <div className="mb-4">
                        <div className="flex items-center space-x-4">
                          <div className="flex items-center">
                            <div className="w-3 h-3 rounded-full bg-yellow-500 mr-2"></div>
                            <span>Class A: Non-hazardous</span>
                          </div>
                          <div className="flex items-center">
                            <div className="w-3 h-3 rounded-full bg-orange-500 mr-2"></div>
                            <span>Class B: Hazardous</span>
                          </div>
                          <div className="flex items-center">
                            <div className="w-3 h-3 rounded-full bg-red-500 mr-2"></div>
                            <span>Class C: Immediately Hazardous</span>
                          </div>
                        </div>
                      </div>
                      
                      <div className="overflow-x-auto">
                        <table className="min-w-full">
                          <thead>
                            <tr className="bg-gray-100 border-b">
                              <th className="py-3 px-4 text-left">Violation ID</th>
                              <th className="py-3 px-4 text-left">Apartment</th>
                              <th className="py-3 px-4 text-left">Issue Date</th>
                              <th className="py-3 px-4 text-left">Class</th>
                              <th classNa<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>