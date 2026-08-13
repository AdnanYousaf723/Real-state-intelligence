import React from 'react';

export default function DataQualityPage() {
  return (
    <div className="space-y-6 max-w-4xl">
      <header>
        <h1 className="text-3xl font-light text-white tracking-tight">Data Quality</h1>
        <p className="text-slate-400 mt-2 text-sm">Monitor pipeline data hygiene and rejection metrics.</p>
      </header>

      <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
        <div className="flex items-center justify-between mb-8 pb-6 border-b border-slate-800">
          <div>
            <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest">Overall Score</h2>
            <p className="text-4xl font-light text-white mt-2">94%</p>
          </div>
        </div>
        
        <div className="space-y-4">
          <div className="flex justify-between text-sm">
            <span className="text-slate-400">Completeness</span>
            <span className="text-emerald-400">96%</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-400">Validity</span>
            <span className="text-emerald-400">97%</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-400">Uniqueness</span>
            <span className="text-amber-400">91%</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-400">Consistency</span>
            <span className="text-emerald-400">95%</span>
          </div>
        </div>

        <div className="mt-8 pt-6 border-t border-slate-800">
          <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4">Latest Issues</h3>
          <ul className="space-y-2 text-sm text-slate-400">
            <li>• 379 rejected records</li>
            <li>• 82 missing ZIP codes</li>
            <li>• 42 invalid years</li>
            <li>• 64 invalid values</li>
          </ul>
        </div>
      </div>
    </div>
  );
}
