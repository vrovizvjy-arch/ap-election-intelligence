import { useMemo } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

export default function WelfareChart({ predictions, partyColors }) {
  const data = useMemo(() => {
    if (!predictions || predictions.length === 0) return [];
    const grouped = {};
    for (const p of predictions) {
      const d = p.district;
      if (!grouped[d]) grouped[d] = { district: d, total: 0, count: 0 };
      grouped[d].total += (p.confidence || 0);
      grouped[d].count += 1;
    }
    return Object.values(grouped)
      .map(g => ({ district: g.district, avgConfidence: +(g.total / g.count * 100).toFixed(1) }))
      .sort((a, b) => b.avgConfidence - a.avgConfidence)
      .slice(0, 10);
  }, [predictions]);

  if (data.length === 0) return (
    <div style={{ padding: 16, flex: 1 }}>
      <h3 style={{ margin: '0 0 8px', fontSize: 14, fontWeight: 600 }}>District Confidence</h3>
      <div style={{ color: '#64748b', fontSize: 13 }}>No data</div>
    </div>
  );

  return (
    <div style={{ padding: '12px 16px', flex: 1, minHeight: 220 }}>
      <h3 style={{ margin: '0 0 8px', fontSize: 14, fontWeight: 600 }}>
        Prediction Confidence by District
      </h3>
      <ResponsiveContainer width="100%" height={180}>
        <BarChart data={data} layout="vertical" margin={{ top: 4, right: 8, left: 4, bottom: 4 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis type="number" domain={[0, 100]} tick={{ fontSize: 10, fill: '#94a3b8' }} />
          <YAxis dataKey="district" type="category" width={80} tick={{ fontSize: 9, fill: '#94a3b8' }} />
          <Tooltip
            contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 6, fontSize: 12 }}
            formatter={(v) => [`${v}%`, 'Confidence']}
          />
          <Bar dataKey="avgConfidence" radius={[0, 4, 4, 0]} barSize={10}>
            {data.map((entry, idx) => (
              <Cell key={idx} fill={entry.avgConfidence > 60 ? '#22c55e' : entry.avgConfidence > 40 ? '#eab308' : '#ef4444'} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
