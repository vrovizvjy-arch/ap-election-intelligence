import { useState } from 'react';

export default function TurnoutSimulator({ onSimulate }) {
  const [turnoutShift, setTurnoutShift] = useState(0);
  const [segment, setSegment] = useState('');

  const handleSimulate = () => {
    onSimulate(turnoutShift, segment);
  };

  return (
    <div style={{ borderTop: '1px solid #1e293b', background: '#1e293b', padding: '12px 20px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16, flexWrap: 'wrap' }}>
        <div style={{ fontWeight: 600, fontSize: 13, whiteSpace: 'nowrap' }}>
          <span style={{ marginRight: 4 }}>Turnout Simulator</span>
          <span style={{ fontSize: 11, color: '#94a3b8', fontWeight: 400 }}>
            (What-If Scenario)
          </span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 11, color: '#94a3b8' }}>-5%</span>
          <input
            type="range"
            min="-5"
            max="5"
            step="0.5"
            value={turnoutShift}
            onChange={e => setTurnoutShift(parseFloat(e.target.value))}
            style={{ width: 140, accentColor: '#3b82f6' }}
          />
          <span style={{ fontSize: 11, color: '#94a3b8' }}>+5%</span>
          <span style={{
            background: turnoutShift > 0 ? '#22c55e' : turnoutShift < 0 ? '#ef4444' : '#64748b',
            color: '#fff', padding: '1px 8px', borderRadius: 8, fontSize: 12, fontWeight: 600, minWidth: 36, textAlign: 'center'
          }}>
            {turnoutShift > 0 ? '+' : ''}{turnoutShift}%
          </span>
        </div>

        <select
          value={segment}
          onChange={e => setSegment(e.target.value)}
          style={{
            background: '#0f172a', color: '#e2e8f0', border: '1px solid #334155',
            padding: '4px 8px', borderRadius: 6, fontSize: 12, cursor: 'pointer'
          }}
        >
          <option value="">All voters</option>
          <option value="women">Women voters</option>
          <option value="youth">Youth (18-22) voters</option>
        </select>

        <button
          onClick={handleSimulate}
          style={{
            background: '#3b82f6', color: '#fff', border: 'none', padding: '5px 16px',
            borderRadius: 6, fontSize: 12, fontWeight: 600, cursor: 'pointer',
            transition: 'background 0.2s'
          }}
          onMouseOver={e => e.target.style.background = '#2563eb'}
          onMouseOut={e => e.target.style.background = '#3b82f6'}
        >
          Run Simulation
        </button>
      </div>
    </div>
  );
}
