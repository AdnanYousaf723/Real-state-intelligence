import React, { useEffect, useState } from 'react';
import { fetchLeads } from '../../lib/api';

export default function LeadsPage() {
  const [leads, setLeads] = useState<any[]>([]);

  useEffect(() => {
    fetchLeads().then(setLeads);
  }, []);

  return (
    <div className="space-y-6 max-w-6xl">
      <header className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-light text-white tracking-tight">Leads</h1>
          <p className="text-slate-400 mt-2 text-sm">Prioritized intelligence based on observable signals.</p>
        </div>
      </header>

      <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden">
        <table className="w-full text-left text-sm">
          <thead className="bg-slate-900/50 text-slate-400 text-xs uppercase tracking-widest border-b border-slate-800">
            <tr>
              <th className="p-4 font-semibold">Property</th>
              <th className="p-4 font-semibold">Location</th>
              <th className="p-4 font-semibold">Score</th>
              <th className="p-4 font-semibold">Priority</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/50 text-slate-300">
            {leads.map((lead) => (
              <tr key={lead.id} className="hover:bg-slate-800/20 transition-colors">
                <td className="p-4 font-medium text-white">{lead.property.address_line_1}</td>
                <td className="p-4">{lead.property.city}, {lead.property.state}</td>
                <td className="p-4">
                  <span className="inline-flex items-center justify-center w-8 h-8 rounded bg-slate-800 border border-slate-700 text-sm font-medium">
                    {lead.score}
                  </span>
                </td>
                <td className="p-4">
                  <span className={`inline-flex px-2 py-1 rounded text-xs font-semibold tracking-wider ${
                    lead.priority === 'VERY_HIGH' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' :
                    lead.priority === 'HIGH' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20' :
                    'bg-slate-800 text-slate-400 border border-slate-700'
                  }`}>
                    {lead.priority.replace('_', ' ')}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
