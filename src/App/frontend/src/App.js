import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import Scanner from './components/Scanner';
import Encyclopedia from './components/Encyclopedia';
import Report from './components/Report';
import Settings from './components/Settings';
import { Toaster } from './components/ui/sonner';
import './App.css';

export default function App() {
  const [currentPage, setCurrentPage] = useState('scanner');

  const renderPage = () => {
    switch (currentPage) {
      case 'scanner':
        return <Scanner />;
      case 'encyclopedia':
        return <Encyclopedia />;
      case 'report':
        return <Report />;
      case 'settings':
        return <Settings />;
      default:
        return <Scanner />;
    }
  };

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <main className="flex-1 overflow-y-auto">
        {renderPage()}
      </main>
      <Toaster />
    </div>
  );
}