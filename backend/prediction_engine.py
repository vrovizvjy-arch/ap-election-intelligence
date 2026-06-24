import numpy as np
from config import PARTIES

class ElectionPredictionEngine:
    def __init__(self):
        self.parties = list(PARTIES.keys())
        # District-level base leanings (historical pattern)
        self.district_bias = {
            "Srikakulam": {"YSRCP": 0.40, "TDP": 0.35, "JSP": 0.12, "BJP": 0.08, "IND": 0.05},
            "Vizianagaram": {"YSRCP": 0.42, "TDP": 0.34, "JSP": 0.11, "BJP": 0.07, "IND": 0.06},
            "Visakhapatnam": {"YSRCP": 0.35, "TDP": 0.38, "JSP": 0.14, "BJP": 0.08, "IND": 0.05},
            "East Godavari": {"YSRCP": 0.33, "TDP": 0.40, "JSP": 0.13, "BJP": 0.09, "IND": 0.05},
            "West Godavari": {"YSRCP": 0.34, "TDP": 0.39, "JSP": 0.13, "BJP": 0.09, "IND": 0.05},
            "Krishna": {"YSRCP": 0.36, "TDP": 0.37, "JSP": 0.13, "BJP": 0.09, "IND": 0.05},
            "Guntur": {"YSRCP": 0.41, "TDP": 0.33, "JSP": 0.12, "BJP": 0.08, "IND": 0.06},
            "Prakasam": {"YSRCP": 0.44, "TDP": 0.31, "JSP": 0.11, "BJP": 0.07, "IND": 0.07},
            "Nellore": {"YSRCP": 0.43, "TDP": 0.32, "JSP": 0.11, "BJP": 0.08, "IND": 0.06},
            "Chittoor": {"YSRCP": 0.38, "TDP": 0.36, "JSP": 0.10, "BJP": 0.10, "IND": 0.06},
            "Kadapa": {"YSRCP": 0.50, "TDP": 0.24, "JSP": 0.10, "BJP": 0.07, "IND": 0.09},
            "Anantapur": {"YSRCP": 0.45, "TDP": 0.28, "JSP": 0.11, "BJP": 0.08, "IND": 0.08},
            "Kurnool": {"YSRCP": 0.46, "TDP": 0.27, "JSP": 0.10, "BJP": 0.08, "IND": 0.09}
        }

    def _compute_score(self, ward):
        dist = ward["district"]
        cb = ward["caste_breakup"]
        fi = ward["field_intel"]
        wd = ward["welfare_delivery"]
        br = ward["booth_result_2024"]

        base = dict(self.district_bias.get(dist, self.district_bias["Guntur"]))
        total_votes_2024 = sum(br.values()) or 1

        # Caste factor: certain castes lean specific parties
        caste_lean = {
            "kamma": {"TDP": 0.15, "JSP": 0.05},
            "kapu": {"TDP": 0.10, "YSRCP": 0.05},
            "reddy": {"YSRCP": 0.12, "TDP": -0.05},
            "bc_boya": {"YSRCP": 0.08},
            "sc_madiga": {"YSRCP": 0.06, "TDP": 0.02},
            "sc_mala": {"TDP": 0.06, "YSRCP": 0.02},
            "minorities": {"YSRCP": 0.08, "TDP": -0.03}
        }

        for caste, leans in caste_lean.items():
            pct = cb.get(caste, 0)
            for party, delta in leans.items():
                if party in base:
                    base[party] += pct * delta

        # Booth 2024 momentum
        incumbent_2024 = max(br, key=br.get)
        base[incumbent_2024] = base.get(incumbent_2024, 0.3) + 0.08

        # Welfare delivery boosts YSRCP (they heavily pushed welfare)
        welfare_avg = np.mean(list(wd.values()))
        base["YSRCP"] += (welfare_avg - 0.5) * 0.15

        # Cadre density
        cadre_total = sum(fi["cadre_density"].values()) or 1
        for party in ["YSRCP", "TDP", "JSP", "BJP"]:
            base[party] += (fi["cadre_density"].get(party, 0) / cadre_total) * 0.1

        # Candidate popularity
        for party in ["YSRCP", "TDP", "JSP", "BJP"]:
            base[party] += (fi["candidate_popularity"].get(party, 0.5) - 0.5) * 0.12

        # Dissident & independent penalty
        base["YSRCP"] -= fi["dissident_index"] * 0.15
        base["TDP"] -= fi["dissident_index"] * 0.10
        base["IND"] += fi["independent_threat"] * 0.20

        # Undecided voters dilute confidence but not bias
        # New voters tend to favor TDP/JSP slightly
        new_voter_effect = ward["new_voters_18_22_pct"] * 0.1
        base["TDP"] += new_voter_effect
        base["JSP"] += new_voter_effect * 0.5

        return base

    def predict(self, ward):
        if ward.get("is_unanimous"):
            return {
                "prediction": "Unanimous",
                "probabilities": {p: 0 for p in self.parties},
                "confidence": 1.0,
                "seat_status": "Uncontested"
            }

        scores = self._compute_score(ward)
        # Add noise for variety
        rng = np.random.RandomState(ward["ward_id"])
        noise = {p: rng.normal(0, 0.04) for p in self.parties}
        adjusted = {p: max(0, scores[p] + noise[p]) for p in self.parties}
        total = sum(adjusted.values()) or 1
        probs = {p: adjusted[p] / total for p in self.parties}

        predicted_party = max(probs, key=probs.get)
        confidence = probs[predicted_party]

        seat_status = "Safe" if confidence > 0.55 else "Leaning" if confidence > 0.45 else "Battleground"

        return {
            "prediction": predicted_party,
            "probabilities": {p: round(probs[p], 4) for p in self.parties},
            "confidence": round(confidence, 4),
            "seat_status": seat_status
        }

    def predict_batch(self, wards):
        results = []
        for ward in wards:
            pred = self.predict(ward)
            results.append({
                "ward_id": ward["ward_id"],
                "ward_name": ward["ward_name"],
                "district": ward["district"],
                "mandal": ward["mandal"],
                "reservation": ward["reservation"],
                "ward_type": ward["ward_type"],
                **pred
            })
        return results

    def simulate_turnout(self, wards, turnout_shift_pct, segment=None):
        adjusted = []
        for ward in wards:
            w = dict(ward)
            fi = w["field_intel"]
            fi["undecided_voter_pct"] = max(0, fi["undecided_voter_pct"] + turnout_shift_pct / 100)
            if segment == "women":
                w["female_voters_pct"] = min(0.6, w["female_voters_pct"] + 0.02 * turnout_shift_pct / 5)
            elif segment == "youth":
                w["new_voters_18_22_pct"] = min(0.25, w["new_voters_18_22_pct"] + 0.015 * turnout_shift_pct / 5)
            adjusted.append(w)
        return self.predict_batch(adjusted)

    def get_risk_analysis(self, wards):
        risks = []
        base_preds = self.predict_batch(wards)
        for pred, ward in zip(base_preds, wards):
            risk_score = 0
            factors = []
            fi = ward["field_intel"]
            if fi["dissident_index"] > 0.25:
                risk_score += 0.3
                factors.append(f"High dissidency ({fi['dissident_index']:.0%})")
            if fi["independent_threat"] > 0.2:
                risk_score += 0.25
                factors.append(f"Strong independent ({fi['independent_threat']:.0%})")
            welfare_avg = np.mean(list(ward["welfare_delivery"].values()))
            if welfare_avg < 0.5:
                risk_score += 0.2
                factors.append(f"Poor welfare delivery ({welfare_avg:.0%})")
            if pred["seat_status"] == "Battleground":
                risk_score += 0.15
                factors.append("Battleground seat")
            if ward["district"] in ["Kurnool", "Anantapur", "Kadapa"]:
                risk_score += 0.1
                factors.append("High volatilty district")
            if pred["confidence"] < 0.40:
                risk_score += 0.1
                factors.append(f"Low confidence ({pred['confidence']:.0%})")

            risks.append({
                "ward_id": ward["ward_id"],
                "ward_name": ward["ward_name"],
                "district": ward["district"],
                "mandal": ward["mandal"],
                "risk_score": round(min(risk_score, 1.0), 3),
                "risk_level": "Critical" if risk_score > 0.6 else "High" if risk_score > 0.4 else "Medium" if risk_score > 0.2 else "Low",
                "factors": factors,
                "predicted_winner": pred["prediction"],
                "confidence": pred["confidence"]
            })
        return sorted(risks, key=lambda r: r["risk_score"], reverse=True)
