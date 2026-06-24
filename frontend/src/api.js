const API_BASE = 'http://localhost:8100/api';

export async function fetchDistricts() {
  const r = await fetch(`${API_BASE}/districts`);
  return r.json();
}

export async function fetchWards(params = {}) {
  const q = new URLSearchParams(params).toString();
  const r = await fetch(`${API_BASE}/wards?${q}`);
  return r.json();
}

export async function fetchPredictions(params = {}) {
  const q = new URLSearchParams(params).toString();
  const r = await fetch(`${API_BASE}/predict/all?${q}`);
  return r.json();
}

export async function fetchRisks(params = {}) {
  const q = new URLSearchParams(params).toString();
  const r = await fetch(`${API_BASE}/risks?${q}`);
  return r.json();
}

export async function fetchSummary(params = {}) {
  const q = new URLSearchParams(params).toString();
  const r = await fetch(`${API_BASE}/summary?${q}`);
  return r.json();
}

export async function simulateTurnout(turnoutShift, segment = '', district = '') {
  const params = { turnout_shift: turnoutShift };
  if (segment) params.segment = segment;
  if (district) params.district = district;
  const q = new URLSearchParams(params).toString();
  const r = await fetch(`${API_BASE}/simulate?${q}`);
  return r.json();
}
