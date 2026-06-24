import random
import json
import numpy as np
from config import DISTRICTS, MANDALS, CASTE_GROUPS, PARTIES, WELFARE_SCHEMES

random.seed(42)
np.random.seed(42)

wards = []
ward_id = 0

for dist in DISTRICTS:
    for mandal in MANDALS.get(dist, []):
        for gp_idx in range(random.randint(3, 8)):
            ward_id += 1
            total_voters = random.randint(800, 3500)
            caste_breakup = {}
            remaining = 1.0
            cg_items = list(CASTE_GROUPS.items())
            random.shuffle(cg_items)
            for i, (key, val) in enumerate(cg_items):
                lo, hi = val["pct_range"]
                if i == len(cg_items) - 1:
                    pct = remaining
                else:
                    pct = round(random.uniform(lo / 100, min(hi / 100, remaining - 0.02)), 4)
                remaining -= pct
                caste_breakup[key] = round(pct, 4)

            hh_count = random.randint(200, 900)
            welfare_scores = {}
            for scheme in WELFARE_SCHEMES:
                welfare_scores[scheme] = round(random.uniform(0.3, 0.98), 2)

            ward_type = random.choice(["GP", "MPTC", "ZPTC", "Municipal"])
            reservation = random.choice(["General", "SC", "ST", "BC", "BC-Women", "SC-Women", "ST-Women", "General-Women"])

            booth_results_2024 = {}
            for party in ["YSRCP", "TDP", "JSP", "BJP"]:
                booth_results_2024[party] = random.randint(40, 1000)

            winner_2024 = max(booth_results_2024, key=booth_results_2024.get)

            field_intel = {
                "cadre_density": {
                    "YSRCP": random.randint(5, 60),
                    "TDP": random.randint(5, 50),
                    "JSP": random.randint(0, 20),
                    "BJP": random.randint(0, 10)
                },
                "dissident_index": round(random.uniform(0, 0.45), 2),
                "independent_threat": round(random.uniform(0, 0.35), 2),
                "undecided_voter_pct": round(random.uniform(0.15, 0.45), 2),
                "candidate_popularity": {
                    "YSRCP": round(random.uniform(0.2, 0.9), 2),
                    "TDP": round(random.uniform(0.2, 0.9), 2),
                    "JSP": round(random.uniform(0.1, 0.6), 2),
                    "BJP": round(random.uniform(0.05, 0.4), 2)
                }
            }

            recent_news = []
            news_templates = [
                f"Local protests over water supply in {mandal} mandal",
                f"{caste_breakup['kapu']*100:.0f}% Kapu voters leaning towards opposition in {mandal}",
                f"Welfare scheme delays reported in {mandal} area",
                f"Strong independent candidate emerges in {mandal} panchayat",
                f"Internal party rift widens in {mandal} mandal",
                f"Women voters mobilize for local candidate in {mandal}",
                f"Road infrastructure complaints dominate {mandal} village meeting",
                f"New voter registrations surge in {mandal} ahead of polls",
                f"Community elders endorse independent panel in {mandal}",
                f"Pension distribution irregularities flagged in {mandal}"
            ]
            for _ in range(random.randint(1, 4)):
                recent_news.append({
                    "headline": random.choice(news_templates),
                    "sentiment": random.choice(["positive", "negative", "neutral"]),
                    "source": random.choice(["Sakshi", "Eenadu", "Andhra Jyothy", "Local", "Social Media"])
                })

            ward = {
                "ward_id": ward_id,
                "district": dist,
                "mandal": mandal,
                "ward_name": f"{mandal} GP No.{gp_idx+1}",
                "ward_type": ward_type,
                "reservation": reservation,
                "total_voters": total_voters,
                "female_voters_pct": round(random.uniform(0.48, 0.54), 2),
                "new_voters_18_22_pct": round(random.uniform(0.08, 0.18), 2),
                "caste_breakup": caste_breakup,
                "households": hh_count,
                "welfare_delivery": welfare_scores,
                "booth_result_2024": booth_results_2024,
                "winner_2024": winner_2024,
                "field_intel": field_intel,
                "recent_news": recent_news,
                "is_unanimous": random.random() < 0.12
            }
            wards.append(ward)

with open("data/wards.json", "w") as f:
    json.dump(wards, f, indent=2)

print(f"Generated {len(wards)} wards across {len(DISTRICTS)} districts")
