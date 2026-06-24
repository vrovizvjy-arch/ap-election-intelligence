const RISK_COLORS = { Critical: '#ef4444', High: '#f97316', Medium: '#eab308', Low: '#22c55e' };

export default function RiskTracker({ risks }) {
  if (!risks || risks.length === 0) return (
    <div style={{ padding: 16, flex: 1 }}>
      <h3 style={{ margin: '0 0 8px', fontSize: 14, fontWeight: 600 }}>Risk & Rebel Tracker</h3>
      <div style={{ color: '#64748b', fontSize: 13 }}>No risks detected</div>
    </div>
  );

  const topRisks = risks.slice(0, 8);

  return (
    <div style={{ padding: '12px 16px', borderBottom: '1px solid #1e293b' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <h3 style={{ margin: 0, fontSize: 14, fontWeight: 600 }}>Risk & Rebel Tracker</h3>
        <span style={{ fontSize: 11, color: '#94a3b8', background: '#0f172a', padding: '2px 8px', borderRadius: 8 }}>
          {risks.length} flagged
        </span>
      </div>
      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
        {topRisks.map(r => (
          <div key={r.ward_id} style={{
            background: '#0f172a', borderRadius: 6, padding: '8px 10px',
            borderLeft: `3px solid ${RISK_COLORS[r.risk_level] || '#666'}`
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontSize: 12, fontWeight: 600 }}>{r.ward_name}</div>
                <div style={{ fontSize: 10, color: '#94a3b8' }}>{r.district} / {r.mandal}</div>
              </div>
              <div style={{ textAlign: 'right' }}>
                <div style={{
                  fontSize: 10, fontWeight: 700, padding: '1px 6px', borderRadius: 8,
                  background: RISK_COLORS[r.risk_level], color: '#000'
                }}>
                  {r.risk_level}
                </div>
                <div style={{ fontSize: 10, color: '#94a3b8', marginTop: 2 }}>
                  {r.predicted_winner}
                </div>
              </div>
            </div>
            {r.factors?.length > 0 && (
              <div style={{ marginTop: 4, display: 'flex', flexWrap: 'wrap', gap: 3 }}>
                {r.factors.slice(0, 2).map((f, i) => (
                  <span key={i} style={{ fontSize: 9, background: '#334155', padding: '1px 6px', borderRadius: 4, color: '#cbd5e1' }}>
                    {f}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
