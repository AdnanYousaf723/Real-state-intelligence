import React, { useEffect, useState } from 'react';
import { fetchDashboardData } from '../lib/api';

export default function DashboardOverview() {
  const [data, setData] = useState<any>(null);

  useEffect(() => {
    fetchDashboardData().then(res => setData(res[0]));
  }, []);

  if (!data) return <div className="text-slate-400">Loading dashboard...</div>;

  return (
    <div className="space-y-6 max-w-6xl">
      <header>
        <h1 className="text-3xl font-light text-white tracking-tight">Real Estate Lead Intelligence</h1>
        <p className="text-slate-400 mt-2 text-sm">Overview of current pipeline status and property metrics.</p>
      </header>

      <div className="grid grid-cols-3 gap-6">
        <MetricCard label="Properties Processed" value={data.records_received.toLocaleString()} />
        <MetricCard label="Leads Generated" value={data.leads_generated.toLocaleString()} />
        <MetricCard label="Pipeline Success Rate" value="100%" />
      </div>

      <div className="grid grid-cols-2 gap-6">
        <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4">Pipeline Status</h2>
          <div className="space-y-3 text-sm text-slate-400">
            <div className="flex justify-between pb-3 border-b border-slate-800/50">
              <span>Status</span>
              <span className="text-emerald-400 flex items-center gap-2">✓ {data.status}</span>
            </div>
            <div className="flex justify-between pb-3 border-b border-slate-800/50">
              <span>Started</span>
              <span className="text-slate-300">{new Date(data.started_at).toLocaleString()}</span>
            </div>
            <div className="flex justify-between pb-3 border-b border-slate-800/50">
              <span>Duration</span>
              <span className="text-slate-300">{data.duration_seconds}s</span>
            </div>
          </div>
        </div>

        <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-widest mb-4">Lead Distribution</h2>
          <div className="space-y-4">
            <ProgressBar label="VERY HIGH" percentage={15} color="bg-rose-500" />
            <ProgressBar label="HIGH" percentage={30} color="bg-amber-500" />
            <ProgressBar label="MEDIUM" percentage={40} color="bg-blue-500" />
            <ProgressBar label="LOW" percentage={15} color="bg-slate-600" />
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ label, value }: { label: string, value: string | number }) {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-lg p-6">
      <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-widest">{label}</h3>
      <p className="text-3xl font-light text-white mt-2">{value}</p>
    </div>
  );
}

function ProgressBar({ label, percentage, color }: { label: string, percentage: number, color: string }) {
  return (
    <div>
      <div className="flex justify-between text-xs mb-1.5">
        <span className="text-slate-400 font-medium">{label}</span>
      </div>
      <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
        <div className={`h-full ${color}`} style={{ width: `${percentage}%` }}></div>
      </div>
    </div>
  );
}
