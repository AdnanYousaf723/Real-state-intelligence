import React from 'react';

export default function PropertiesPage() {
  return (
    <div className="space-y-6 max-w-6xl">
      <header>
        <h1 className="text-3xl font-light text-white tracking-tight">Properties</h1>
        <p className="text-slate-400 mt-2 text-sm">Canonical property records ingested from all sources.</p>
      </header>

      <div className="bg-slate-900 border border-slate-800 rounded-lg p-8 text-center">
        <p className="text-slate-500">Property table functionality and details will be mounted here.</p>
      </div>
    </div>
  );
}
