from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
import os
import numpy as np

from config import DISTRICTS, PARTIES
from prediction_engine import ElectionPredictionEngine
from sentiment_analyzer import compute_narrative_vector

app = FastAPI(title="AP Election Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "wards.json")
engine = ElectionPredictionEngine()

def load_wards():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH) as f:
            return json.load(f)
    return []

@app.on_event("startup")
def startup():
    global engine
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "data")):
        os.makedirs(os.path.join(os.path.dirname(__file__), "data"))
    wards = load_wards()
    if not wards:
        from seed_data import wards as seed_wards
        with open(DATA_PATH, "w") as f:
            json.dump(seed_wards, f, indent=2)

@app.get("/api/districts")
def get_districts():
    return DISTRICTS

@app.get("/api/wards")
def get_wards(
    district: str = None,
    mandal: str = None,
    ward_type: str = None,
    reservation: str = None,
    limit: int = 500
):
    wards = load_wards()
    filtered = wards
    if district:
        filtered = [w for w in filtered if w["district"] == district]
    if mandal:
        filtered = [w for w in filtered if w["mandal"] == mandal]
    if ward_type:
        filtered = [w for w in filtered if w["ward_type"] == ward_type]
    if reservation:
        filtered = [w for w in filtered if w["reservation"] == reservation]
    return filtered[:limit]

@app.get("/api/predict/all")
def predict_all(district: str = None, mandal: str = None):
    wards = load_wards()
    if district:
        wards = [w for w in wards if w["district"] == district]
    if mandal:
        wards = [w for w in wards if w["mandal"] == mandal]
    results = engine.predict_batch(wards)
    return {
        "total_wards": len(results),
        "predictions": results,
        "summary": generate_summary(results)
    }

@app.get("/api/predict/{ward_id}")
def predict_ward(ward_id: int):
    wards = load_wards()
    ward = next((w for w in wards if w["ward_id"] == ward_id), None)
    if not ward:
        return {"error": "Ward not found"}
    pred = engine.predict(ward)
    narrative = compute_narrative_vector([ward])
    return {
        "ward": ward,
        "prediction": pred,
        "narrative": narrative.get(ward_id, {})
    }

@app.get("/api/simulate")
def simulate(
    turnout_shift: float = Query(0, description="Turnout shift % (-10 to 10)"),
    segment: str = Query(None, description="Voter segment: women, youth, or null"),
    district: str = None
):
    wards = load_wards()
    if district:
        wards = [w for w in wards if w["district"] == district]
    results = engine.simulate_turnout(wards, turnout_shift, segment)
    return {
        "simulation_params": {"turnout_shift": turnout_shift, "segment": segment},
        "total_wards": len(results),
        "predictions": results,
        "summary": generate_summary(results)
    }

@app.get("/api/risks")
def get_risks(district: str = None, min_risk: float = 0):
    wards = load_wards()
    if district:
        wards = [w for w in wards if w["district"] == district]
    risks = engine.get_risk_analysis(wards)
    if min_risk > 0:
        risks = [r for r in risks if r["risk_score"] >= min_risk]
    return {"total_risks": len(risks), "risks": risks[:100]}

@app.get("/api/summary")
def get_summary(district: str = None):
    wards = load_wards()
    if district:
        wards = [w for w in wards if w["district"] == district]
    preds = engine.predict_batch(wards)
    summary = generate_summary(preds)

    # Build district-level breakdown
    dist_wards = {}
    for w, p in zip(wards, preds):
        d = w["district"]
        dist_wards.setdefault(d, []).append(p)
    district_details = []
    for dw, dpreds in dist_wards.items():
        dist_party = {}
        for p in dpreds:
            party = p["prediction"]
            if party != "Unanimous":
                dist_party[party] = dist_party.get(party, 0) + 1
        ranked = sorted(dist_party.items(), key=lambda x: -x[1])
        district_details.append({
            "district": dw,
            "parties": [{"name": k, "seats": v} for k, v in ranked],
            "total": len(dpreds)
        })
    summary["district_details"] = district_details
    return summary

@app.get("/api/intel/stream")
def get_intel_stream():
    wards = load_wards()
    events = []
    rng = np.random.RandomState(42)
    templates = [
        ("district_update", "Intelligence report: {district} cluster showing {delta:+.1f}% shift in {demo} demographic sentiment following recent policy announcement.", "DISTRICT_UPDT", "tertiary"),
        ("field_alert", "High-level influencer alignment confirmed in {district}. Adjusted win probability to {pct}% (+{delta}%).", "FIELD_ALERT", "secondary"),
        ("risk_detection", "Social media volatility spike in {district} (Zone-{zone}). Narrative shift detected. Response strategy required.", "RISK_DETECTION", "error"),
        ("sys_log", "Electoral roll audit for {district} complete. No significant anomalies found.", "SYS_LOG", "muted"),
        ("positive_vibe", "New investments boost confidence among youth in {mandal} mandal. Positive sentiment trending.", "POSITIVE_VIBE", "green"),
        ("cadre_report", "Cadre mobilization confirmed in {district}. Door-to-door campaign initiated across {n} booths.", "CADRE_MOBI", "tertiary"),
    ]
    for i in range(8):
        ward = wards[rng.randint(0, len(wards)-1)]
        tmpl = templates[rng.randint(0, len(templates)-1)]
        now = __import__("datetime").datetime.now()
        time_str = (now - __import__("datetime").timedelta(minutes=i*4 + rng.randint(1, 3))).strftime("%H:%M:%S")
        delta = round(rng.uniform(-5, 8), 1)
        pct = min(95, max(40, 65 + delta))
        zone = chr(ord('A') + rng.randint(0, 4))
        n = rng.randint(5, 30)
        text = tmpl[1].format(district=ward["district"], mandal=ward["mandal"], delta=delta, pct=pct, zone=zone, n=n, demo=rng.choice(["youth", "women", "rural", "urban"]))
        events.append({
            "id": i+1,
            "time": time_str,
            "label": tmpl[2],
            "color": tmpl[3],
            "text": text,
            "timestamp": (now - __import__("datetime").timedelta(minutes=i*4 + rng.randint(1, 3))).isoformat()
        })
    return {"events": events}

@app.get("/api/intel/sentiment")
def get_sentiment():
    wards = load_wards()
    preds = engine.predict_batch(wards)
    narratives = compute_narrative_vector(wards)
    sentiment_values = [n["sentiment_score"] for n in narratives.values()]
    avg_sentiment = np.mean(sentiment_values) if sentiment_values else 0.5
    return {
        "overall_sentiment": round(float(avg_sentiment), 4),
        "narrative_confidence": round(float(np.std(sentiment_values)) if len(sentiment_values) > 1 else 0.1, 4),
        "total_wards_analyzed": len(narratives),
        "positive_ratio": round(float(sum(1 for s in sentiment_values if s > 0.5) / max(len(sentiment_values), 1)), 4)
    }

CENSUS_PATH = os.path.join(os.path.dirname(__file__), "data", "census_data.json")
GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "data", "ap_districts.geojson")

@app.get("/api/census")
def get_census():
    if os.path.exists(CENSUS_PATH):
        with open(CENSUS_PATH) as f:
            return json.load(f)
    return {"error": "Census data not available"}

@app.get("/api/geojson")
def get_geojson():
    if os.path.exists(GEOJSON_PATH):
        with open(GEOJSON_PATH) as f:
            return json.load(f)
    return {"error": "GeoJSON not available"}

@app.get("/api/district/{name}")
def get_district_detail(name: str):
    wards = load_wards()
    dist_wards = [w for w in wards if w["district"].lower() == name.lower()]
    if not dist_wards:
        return {"error": "District not found"}
    preds = engine.predict_batch(dist_wards)
    summary = generate_summary(preds)
    census = {}
    if os.path.exists(CENSUS_PATH):
        with open(CENSUS_PATH) as f:
            cdata = json.load(f)
            for r in cdata.get("records", []):
                if r["district"].lower() == name.lower():
                    census = r
    return {
        "district": name,
        "total_wards": len(dist_wards),
        "summary": summary,
        "predictions": preds[:10],
        "census": census
    }

@app.get("/api/intel/favorability")
def get_favorability():
    wards = load_wards()
    rng = np.random.RandomState(42)
    total_wards = len(wards)
    return {
        "leaders": [
            {
                "name": "LEADER_ALFA",
                "favorability": round(65 + rng.uniform(-5, 15), 1),
                "trend": "+2.3%",
                "status": "stable"
            },
            {
                "name": "LEADER_OMEGA",
                "favorability": round(30 + rng.uniform(-5, 10), 1),
                "trend": "-1.8%",
                "status": "declining"
            },
            {
                "name": "LEADER_BETA",
                "favorability": round(50 + rng.uniform(-8, 8), 1),
                "trend": "+0.5%",
                "status": "stable"
            }
        ],
        "aggregate_confidence": round(rng.uniform(0.82, 0.94), 3)
    }

@app.get("/api/simulate/advanced")
def simulate_advanced(
    women_pct: float = Query(74, ge=0, le=100),
    youth_pct: float = Query(62, ge=0, le=100),
    caste_pct: float = Query(58, ge=0, le=100),
    swing_pct: float = Query(12, ge=0, le=100),
    district: str = None
):
    wards = load_wards()
    if district:
        wards = [w for w in wards if w["district"] == district]
    turnout_shift = (women_pct + youth_pct + caste_pct) / 3 - 65
    results = engine.simulate_turnout(wards, turnout_shift, None)
    summary = generate_summary(results)
    total_seats = summary["total_wards"]
    top_party = max(summary["party_projection"].items(), key=lambda x: x[1]) if summary["party_projection"] else ("N/A", 0)
    return {
        "simulated_seats": top_party[1],
        "total_seats": total_seats,
        "top_party": top_party[0],
        "turnout_shift": round(turnout_shift, 2),
        "summary": summary,
        "parameters": {"women_pct": women_pct, "youth_pct": youth_pct, "caste_pct": caste_pct, "swing_pct": swing_pct}
    }

def generate_summary(predictions):
    total = len(predictions)
    if total == 0:
        return {"total": 0}
    party_counts = {}
    status_counts = {}
    unanimous = 0
    for p in predictions:
        if p["prediction"] == "Unanimous":
            unanimous += 1
            status_counts["Uncontested"] = status_counts.get("Uncontested", 0) + 1
        else:
            party = p["prediction"]
            party_counts[party] = party_counts.get(party, 0) + 1
            status_counts[p.get("seat_status", "Unknown")] = status_counts.get(p.get("seat_status", "Unknown"), 0) + 1
    return {
        "total_wards": total,
        "party_projection": party_counts,
        "seat_status_breakdown": status_counts,
        "unanimous_wards": unanimous
    }
