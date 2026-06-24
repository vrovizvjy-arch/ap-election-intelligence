import { useEffect, useState, useMemo } from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const DISTRICT_COORDS = {
  'Srikakulam': [18.3, 83.9], 'Vizianagaram': [18.12, 83.42],
  'Visakhapatnam': [17.73, 83.31], 'East Godavari': [16.99, 82.25],
  'West Godavari': [16.99, 81.78], 'Krishna': [16.21, 81.14],
  'Guntur': [16.31, 80.45], 'Prakasam': [15.51, 80.05],
  'Nellore': [14.46, 79.99], 'Chittoor': [13.21, 79.10],
  'Kadapa': [14.47, 78.82], 'Anantapur': [14.69, 77.60],
  'Kurnool': [15.83, 78.04]
};

function DistrictMarkers({ predictions, partyColors }) {
  const grouped = useMemo(() => {
    const g = {};
    for (const p of (predictions || [])) {
      const d = p.district;
      if (!g[d]) g[d] = { district: d, wards: [], wins: {} };
      g[d].wards.push(p);
      g[d].wins[p.prediction] = (g[d].wins[p.prediction] || 0) + 1;
    }
    return Object.values(g);
  }, [predictions]);

  return grouped.map((g) => {
    const coord = DISTRICT_COORDS[g.district] || [15.9, 79.5];
    const sorted = Object.entries(g.wins).sort((a, b) => b[1] - a[1]);
    const topParty = sorted[0];
    const color = partyColors[topParty?.[0]] || '#666';
    const totalWards = g.wards.length;

    return (
      <CircleMarker
        key={g.district}
        center={coord}
        radius={Math.max(6, Math.min(18, totalWards * 0.8))}
        pathOptions={{ color: '#fff', weight: 1.5, fillColor: color, fillOpacity: 0.8 }}
      >
        <Popup>
          <div style={{ fontFamily: 'sans-serif', minWidth: 200 }}>
            <strong style={{ fontSize: 14 }}>{g.district} District</strong>
            <hr style={{ margin: '4px 0' }} />
            <div>Total Wards: <strong>{totalWards}</strong></div>
            <div>Leading: <strong style={{ color }}>{topParty?.[0] || 'N/A'}</strong> ({topParty?.[1] || 0})</div>
            <hr style={{ margin: '4px 0' }} />
            {sorted.map(([p, c]) => (
              <div key={p} style={{ display: 'flex', justifyContent: 'space-between', gap: 12 }}>
                <span>
                  <span style={{ display: 'inline-block', width: 10, height: 10, background: partyColors[p] || '#666', borderRadius: '50%', marginRight: 4 }} />
                  {p}
                </span>
                <strong>{c}</strong>
              </div>
            ))}
          </div>
        </Popup>
      </CircleMarker>
    );
  });
}

export default function MapView({ predictions, partyColors }) {
  return (
    <div style={{ width: '100%', height: '100%', position: 'relative' }}>
      <MapContainer center={[15.9, 79.5]} zoom={7} style={{ width: '100%', height: '100%' }} zoomControl={false}>
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, &copy; <a href="https://carto.com/">CARTO</a>'
        />
        <DistrictMarkers predictions={predictions} partyColors={partyColors} />
      </MapContainer>
      <div style={{
        position: 'absolute', top: 12, left: 12, zIndex: 1000,
        background: '#1e293b', padding: '10px 14px', borderRadius: 8,
        fontSize: 12, border: '1px solid #334155', boxShadow: '0 2px 8px rgba(0,0,0,0.3)'
      }}>
        <strong style={{ fontSize: 13 }}>Legend</strong>
        {Object.entries(partyColors).map(([p, c]) => (
          <div key={p} style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 4 }}>
            <span style={{ width: 10, height: 10, background: c, borderRadius: '50%', display: 'inline-block' }} />
            <span>{p}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
