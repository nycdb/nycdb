// Home page component for NYCDB web application
'use client';

import React from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import Layout from '../../components/Layout';

export default function HomePage() {
  const router = useRouter();
  const [searchQuery, setSearchQuery] = React.useState('');
  
  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      router.push(`/search?query=${encodeURIComponent(searchQuery)}`);
    }
  };
  
  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-3xl font-bold mb-4">Welcome to NYCDB Web Application</h1>
          <p className="text-xl text-gray-600">
            Explore NYC housing data from multiple sources
          </p>
        </div>
        
        {/* Quick Search */}
        <div className="mb-12">
          <form onSubmit={handleSearch} className="flex">
            <input
              type="text"
              placeholder="Enter address, BBL, or building info"
              className="flex-grow px-4 py-2 border border-gray-300 rounded-l focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button
              type="submit"
              className="bg-blue-600 text-white px-6 py-2 rounded-r hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Search
            </button>
          </form>
        </div>
        
        {/* Dataset Categories */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          {/* Property Data */}
          <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <h2 className="text-xl font-semibold mb-3">Property Data</h2>
            <ul className="space-y-2">
              <li>
                <Link href="/datasets/pluto" className="text-blue-600 hover:underline">
                  PLUTO
                </Link>
                <p className="text-sm text-gray-600">Property and tax lot information</p>
              </li>
              <li>
                <Link href="/datasets/hpd_registrations" className="text-blue-600 hover:underline">
                  HPD Registrations
                </Link>
                <p className="text-sm text-gray-600">Building registrations with HPD</p>
              </li>
            </ul>
          </div>
          
          {/* Violations */}
          <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <h2 className="text-xl font-semibold mb-3">Violations</h2>
            <ul className="space-y-2">
              <li>
                <Link href="/datasets/hpd_violations" className="text-blue-600 hover:underline">
                  HPD Violations
                </Link>
                <p className="text-sm text-gray-600">Housing code violations</p>
              </li>
              <li>
                <Link href="/datasets/dob_violations" className="text-blue-600 hover:underline">
                  DOB Violations
                </Link>
                <p className="text-sm text-gray-600">Building code violations</p>
              </li>
            </ul>
          </div>
          
          {/* Complaints */}
          <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <h2 className="text-xl font-semibold mb-3">Complaints</h2>
            <ul className="space-y-2">
              <li>
                <Link href="/datasets/dob_complaints" className="text-blue-600 hover:underline">
                  DOB Complaints
                </Link>
                <p className="text-sm text-gray-600">Building complaints</p>
              </li>
              <li>
                <Link href="/datasets/hpd_complaints" className="text-blue-600 hover:underline">
                  HPD Complaints
                </Link>
                <p className="text-sm text-gray-600">Housing complaints</p>
              </li>
            </ul>
          </div>
          
          {/* Evictions */}
          <div className="border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
            <h2 className="text-xl font-semibold mb-3">Evictions</h2>
            <ul className="space-y-2">
              <li>
                <Link href="/datasets/evictions" className="text-blue-600 hover:underline">
                  Marshal Evictions
                </Link>
                <p className="text-sm text-gray-600">Eviction data from NYC marshals</p>
              </li>
            </ul>
          </div>
        </div>
        
        {/* About Section */}
        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl font-semibold mb-3">About NYCDB</h2>
          <p className="mb-4">
            NYCDB is a database of NYC housing data, compiled from various public sources. 
            This web application provides an easy-to-use interface for accessing and searching this data.
          </p>
          <p>
            <Link href="/about" className="text-blue-600 hover:underline">
              Learn more about NYCDB
            </Link>
          </p>
        </div>
      </div>
    </Layout>
  );
}
