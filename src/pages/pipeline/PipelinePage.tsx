import React, { useEffect, useState } from 'react';
import { fetchDashboardData } from '../../lib/api';

export default function PipelinePage() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetchDashboardData().then(res => setData(res[0]));
  }, []);

  if (!data) return null;

  return (
    <div className="space-y-6 max-w-4xl">
      <header>
        <h1 className="text-3xl font-light text-white tracking-tight">Pipeline Control</h1>
        <p className="text-slate-400 mt-2 text-sm">Monitor and trigger ingestion and scoring pipelines.</p>
      </header>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4 border-b border-slate-800 pb-2">Status</h2>
          <div className="space-y-2 mt-4">
            <p className="text-sm text-slate-400">Current Status: <span className="text-white font-medium">IDLE</span></p>
            <p className="text-sm text-slate-400">Last Run: <span className="text-white font-medium">{new Date(data.started_at).toLocaleString()}</span></p>
          </div>
          
          <div className="mt-8 space-y-3">
            <button className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium rounded transition-colors">
              RUN PIPELINE
            </button>
            <div className="grid grid-cols-2 gap-3">
              <button className="py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium border border-slate-700 rounded transition-colors">
                VALIDATE ONLY
              </button>
              <button className="py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium border border-slate-700 rounded transition-colors">
                EXPORT RESULTS
              </button>
            </div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4 border-b border-slate-800 pb-2">Last Run Metrics</h2>
          
          <div className="space-y-3 text-sm text-slate-400 font-mono mt-4">
            <div className="flex justify-between">
              <span>Records received:</span>
              <span className="text-white">{data.records_received.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span>Valid:</span>
              <span className="text-emerald-400">{data.records_valid.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span>Rejected:</span>
              <span className="text-rose-400">{data.records_rejected.toLocaleString()}</span>
            </div>
            <div className="flex justify-between pt-2 border-t border-slate-800">
              <span>Duplicates:</span>
              <span className="text-amber-400">{data.duplicates_found.toLocaleString()}</span>
            </div>
            <div className="flex justify-between">
              <span>Enriched:</span>
              <span className="text-white">{data.records_enriched.toLocaleString()}</span>
            </div>
            <div className="flex justify-between pt-2 border-t border-slate-800">
              <span>Leads generated:</span>
              <span className="text-white font-bold">{data.leads_generated.toLocaleString()}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
