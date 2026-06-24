import { useState, useEffect, useCallback, useRef } from 'react';
import { fetchDistricts, fetchPredictions, fetchRisks, fetchSummary, simulateTurnout } from './api';
import MapView from './components/MapView';
import RiskTracker from './components/RiskTracker';
import TurnoutSimulator from './components/TurnoutSimulator';
import WelfareChart from './components/WelfareChart';
import Sidebar from './components/Sidebar';

const PARTY_COLORS = { YSRCP: '#FF0000', TDP: '#FFFF00', JSP: '#0000FF', BJP: '#FF9933', IND: '#808080' };

export default function Dashboard() {
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState('');
  const [predictions, setPredictions] = useState([]);
  const [risks, setRisks] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [simResult, setSimResult] = useState(null);
  const initialized = useRef(false);

  useEffect(() => {
    fetchDistricts().then(setDistricts);
  }, []);

  const loadData = useCallback(async (district) => {
    setLoading(true);
    const params = district ? { district } : {};
    const [pred, risk, summ] = await Promise.all([
      fetchPredictions(params),
      fetchRisks(params),
      fetchSummary(params)
    ]);
    setPredictions(pred.predictions || []);
    setRisks(risk.risks || []);
    setSummary(summ);
    setLoading(false);
  }, []);

  useEffect(() => {
    if (!initialized.current) {
      initialized.current = true;
      loadData('');
    }
  }, [loadData]);

  const handleDistrictChange = (d) => {
    setSelectedDistrict(d);
    loadData(d);
  };

  const handleSimulate = async (turnoutShift, segment) => {
    const result = await simulateTurnout(turnoutShift, segment, selectedDistrict);
    setSimResult(result);
    setPredictions(result.predictions || []);
    setSummary(result.summary);
  };

  const handleReset = () => {
    setSimResult(null);
    loadData(selectedDistrict);
  };

  const partyProjection = summary?.party_projection || {};
  const total = summary?.total_wards || 0;
  const topParty = Object.entries(partyProjection).sort((a, b) => b[1] - a[1]);

  return (
    <div style={{ display: 'flex', height: '100vh', fontFamily: 'Inter, sans-serif', background: '#0f172a', color: '#e2e8f0' }}>
      <Sidebar
        districts={districts}
        selectedDistrict={selectedDistrict}
        onDistrictChange={handleDistrictChange}
        summary={summary}
        partyColors={PARTY_COLORS}
        onReset={handleReset}
        isSimulated={!!simResult}
      />
      <main style={{ flex: 1, display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
        <header style={{ padding: '16px 24px', borderBottom: '1px solid #1e293b', background: '#1e293b' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            <h1 style={{ margin: 0, fontSize: 20, fontWeight: 600 }}>
              AP Local Body Election Intelligence
            </h1>
            {simResult && (
              <span style={{ background: '#f59e0b', color: '#000', padding: '4px 12px', borderRadius: 12, fontSize: 12, fontWeight: 600 }}>
                SIMULATION ACTIVE
              </span>
            )}
          </div>
        </header>

        {loading ? (
          <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <div style={{ fontSize: 18 }}>Loading intelligence data...</div>
          </div>
        ) : (
          <div style={{ flex: 1, display: 'grid', gridTemplateColumns: '1fr 380px', gap: 0, overflow: 'hidden' }}>
            <div style={{ display: 'flex', flexDirection: 'column', overflow: 'hidden' }}>
              <div style={{ flex: 1, position: 'relative' }}>
                <MapView predictions={predictions} partyColors={PARTY_COLORS} />
              </div>
              <TurnoutSimulator onSimulate={handleSimulate} />
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', borderLeft: '1px solid #1e293b', overflow: 'auto' }}>
              <RiskTracker risks={risks} />
              <WelfareChart predictions={predictions} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
