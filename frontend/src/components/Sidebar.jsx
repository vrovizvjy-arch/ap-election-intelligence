const PARTY_COLORS = { YSRCP: '#FF0000', TDP: '#FFFF00', JSP: '#0000FF', BJP: '#FF9932', IND: '#808080' };

export default function Sidebar({ districts, selectedDistrict, onDistrictChange, summary, onReset, isSimulated }) {
  const partyProjection = summary?.party_projection || {};
  const total = summary?.total_wards || 0;
  const sorted = Object.entries(partyProjection).sort((a, b) => b[1] - a[1]);
  const statusBreakdown = summary?.seat_status_breakdown || {};

  return (
    <aside style={{
      width: 260, background: '#1e293b', borderRight: '1px solid #0f172a',
      display: 'flex', flexDirection: 'column', overflow: 'auto'
    }}>
      <div style={{ padding: '16px 16px 12px', borderBottom: '1px solid #334155' }}>
        <h2 style={{ margin: 0, fontSize: 16, fontWeight: 600 }}>Filters</h2>
      </div>

      <div style={{ padding: '12px 16px', borderBottom: '1px solid #334155' }}>
        <label style={{ fontSize: 11, color: '#94a3b8', display: 'block', marginBottom: 4 }}>DISTRICT</label>
        <select
          value={selectedDistrict}
          onChange={e => onDistrictChange(e.target.value)}
          style={{
            width: '100%', background: '#0f172a', color: '#e2e8f0', border: '1px solid #334155',
            padding: '6px 8px', borderRadius: 6, fontSize: 13, cursor: 'pointer'
          }}
        >
          <option value="">All Districts</option>
          {districts.map(d => <option key={d} value={d}>{d}</option>)}
        </select>
      </div>

      <div style={{ padding: '16px', borderBottom: '1px solid #334155' }}>
        <h3 style={{ margin: '0 0 8px', fontSize: 13, fontWeight: 600, color: '#94a3b8' }}>
          SEAT PROJECTION
        </h3>
        {total > 0 ? (
          <>
            <div style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>
              {total} <span style={{ fontSize: 14, fontWeight: 400, color: '#94a3b8' }}>wards</span>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
              {sorted.map(([party, count]) => {
                const pct = total > 0 ? (count / total * 100).toFixed(1) : 0;
                return (
                  <div key={party}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 2 }}>
                      <span>
                        <span style={{ display: 'inline-block', width: 8, height: 8, background: PARTY_COLORS[party] || '#666', borderRadius: '50%', marginRight: 4 }} />
                        {party}
                      </span>
                      <strong>{count} ({pct}%)</strong>
                    </div>
                    <div style={{ height: 4, background: '#0f172a', borderRadius: 2, overflow: 'hidden' }}>
                      <div style={{ width: `${pct}%`, height: '100%', background: PARTY_COLORS[party] || '#666', borderRadius: 2, transition: 'width 0.3s' }} />
                    </div>
                  </div>
                );
              })}
            </div>
          </>
        ) : (
          <div style={{ color: '#64748b', fontSize: 13 }}>No data</div>
        )}
      </div>

      <div style={{ padding: '16px', borderBottom: '1px solid #334155' }}>
        <h3 style={{ margin: '0 0 6px', fontSize: 13, fontWeight: 600, color: '#94a3b8' }}>
          SEAT STATUS
        </h3>
        {Object.entries(statusBreakdown).filter(([k]) => k !== 'Uncontested').map(([status, count]) => {
          const color = status === 'Safe' ? '#22c55e' : status === 'Leaning' ? '#eab308' : status === 'Battleground' ? '#ef4444' : '#64748b';
          return (
            <div key={status} style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginBottom: 3 }}>
              <span style={{ color }}>● {status}</span>
              <strong>{count}</strong>
            </div>
          );
        })}
        {summary?.unanimous_wards > 0 && (
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 12, marginTop: 4, paddingTop: 4, borderTop: '1px solid #334155' }}>
            <span style={{ color: '#64748b' }}>Uncontested</span>
            <strong>{summary.unanimous_wards}</strong>
          </div>
        )}
      </div>

      <div style={{ padding: '12px 16px', marginTop: 'auto' }}>
        {isSimulated && (
          <button
            onClick={onReset}
            style={{
              width: '100%', background: '#334155', color: '#e2e8f0', border: 'none',
              padding: '8px', borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: 'pointer',
              transition: 'background 0.2s'
            }}
            onMouseOver={e => e.target.style.background = '#475569'}
            onMouseOut={e => e.target.style.background = '#334155'}
          >
            Reset to Baseline
          </button>
        )}
        <div style={{ fontSize: 10, color: '#475569', textAlign: 'center', marginTop: 8 }}>
          AP Local Body Election Intelligence
        </div>
      </div>
    </aside>
  );
}
