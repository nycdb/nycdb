// Layout component for NYCDB web application
'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

interface LayoutProps {
  children: React.ReactNode;
}

export default function Layout({ children }: LayoutProps) {
  const pathname = usePathname();
  
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-blue-700 text-white shadow-md">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center">
            <Link href="/" className="text-xl font-bold">
              NYCDB Web App
            </Link>
          </div>
          <nav className="flex space-x-4">
            <Link 
              href="/datasets" 
              className={`hover:text-blue-200 ${pathname.startsWith('/datasets') ? 'font-bold underline' : ''}`}
            >
              Datasets
            </Link>
            <Link 
              href="/about" 
              className={`hover:text-blue-200 ${pathname === '/about' ? 'font-bold underline' : ''}`}
            >
              About
            </Link>
            <Link 
              href="/help" 
              className={`hover:text-blue-200 ${pathname === '/help' ? 'font-bold underline' : ''}`}
            >
              Help
            </Link>
          </nav>
        </div>
      </header>
      
      {/* Main content */}
      <main className="flex-grow container mx-auto px-4 py-8">
        {children}
      </main>
      
      {/* Footer */}
      <footer className="bg-gray-100 border-t border-gray-200">
        <div className="container mx-auto px-4 py-6">
          <div className="text-center text-gray-600 text-sm">
            <p>Data provided by NYCDB | <a href="https://www.housingdatanyc.org/" className="text-blue-600 hover:underline" target="_blank" rel="noopener noreferrer">Housing Data Coalition</a></p>
            <p className="mt-2">This application is for educational and research purposes only.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
