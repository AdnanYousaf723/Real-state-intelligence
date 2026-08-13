const API_BASE = '/api/v1';

export const fetchDashboardData = async () => {
  try {
    const res = await fetch(`${API_BASE}/pipeline/runs`);
    if (!res.ok) throw new Error('API not available');
    const runs = await res.json();
    return runs;
  } catch (err) {
    // Return mock data for UI demonstration
    return [
      {
        id: 1, started_at: "2026-08-14T01:00:00Z", finished_at: "2026-08-14T01:02:31Z",
        status: "SUCCESS", source: "ATTOM", records_received: 10000, records_valid: 9621,
        records_rejected: 379, duplicates_found: 612, records_enriched: 9109,
        signals_generated: 15420, leads_generated: 3218, error_count: 0, duration_seconds: 151
      }
    ];
  }
};

export const fetchLeads = async () => {
  try {
    const res = await fetch(`${API_BASE}/leads`);
    if (!res.ok) throw new Error('API not available');
    return await res.json();
  } catch (err) {
    return [
      { id: 1, score: 94, priority: 'VERY_HIGH', property: { address_line_1: '123 Main St', city: 'Denver', state: 'CO' }, reasons: '• Absentee (+15)\n• Vacant (+25)' },
      { id: 2, score: 88, priority: 'VERY_HIGH', property: { address_line_1: '72 Oak Ave', city: 'Denver', state: 'CO' }, reasons: '• Ownership > 20 yrs (+25)' },
      { id: 3, score: 81, priority: 'HIGH', property: { address_line_1: '91 Pine Road', city: 'Aurora', state: 'CO' }, reasons: '• Tax signal (+20)' },
    ];
  }
};
