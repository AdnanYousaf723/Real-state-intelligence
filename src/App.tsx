/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import { LayoutDashboard, Users, Home, Activity, CheckCircle, Database, Settings } from 'lucide-react';
import DashboardOverview from './pages/DashboardOverview';
import LeadsPage from './pages/leads/LeadsPage';
import PropertiesPage from './pages/properties/PropertiesPage';
import PipelinePage from './pages/pipeline/PipelinePage';
import DataQualityPage from './pages/quality/DataQualityPage';

const Sidebar = () => {
  const location = useLocation();
  const navItems = [
    { name: 'Dashboard', path: '/', icon: LayoutDashboard },
    { name: 'Leads', path: '/leads', icon: Users },
    { name: 'Properties', path: '/properties', icon: Home },
    { name: 'Pipeline', path: '/pipeline', icon: Activity },
    { name: 'Data Quality', path: '/quality', icon: CheckCircle },
    { name: 'Sources', path: '/sources', icon: Database },
    { name: 'Settings', path: '/settings', icon: Settings },
  ];

  return (
    <div className="w-64 bg-slate-900 text-slate-300 flex flex-col h-screen border-r border-slate-800">
      <div className="p-6 border-b border-slate-800">
        <h1 className="text-xl font-bold text-white tracking-wider">RELI</h1>
        <p className="text-xs text-slate-500 uppercase mt-1 tracking-widest">Lead Intelligence</p>
      </div>
      <nav className="flex-1 py-4">
        <ul className="space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;
            return (
              <li key={item.name}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-6 py-3 text-sm font-medium transition-colors ${
                    isActive ? 'text-white bg-slate-800 border-r-2 border-blue-500' : 'hover:text-white hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {item.name}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </div>
  );
};

export default function App() {
  return (
    <Router>
      <div className="flex h-screen bg-slate-950 text-slate-200 font-sans overflow-hidden">
        <Sidebar />
        <main className="flex-1 overflow-y-auto bg-slate-950 p-8">
          <Routes>
            <Route path="/" element={<DashboardOverview />} />
            <Route path="/leads" element={<LeadsPage />} />
            <Route path="/properties" element={<PropertiesPage />} />
            <Route path="/pipeline" element={<PipelinePage />} />
            <Route path="/quality" element={<DataQualityPage />} />
            <Route path="*" element={<div className="p-4 bg-slate-900 rounded-lg border border-slate-800 text-slate-400">Page under construction</div>} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}
