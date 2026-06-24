"""
AP Election Intelligence - Government Data Ingestion Pipeline
Fetches real data from government sources: Census 2011, AP SEC, data.gov.in
"""
import json
import os
import urllib.request
import urllib.error
import ssl

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

CENSUS_API = "https://api.data.gov.in/resource/04cbe4b1-2f2b-4b8d-bc0b-8e8b6c5c0b5b?api-key=579b464db66ec23bdd000001cd58c3e14a6e440f5e2b1e3a1d8c2b5f4a6b7c8d&format=json&limit=20&filters[state_name]=Andhra+Pradesh"
SEC_URL = "https://sec.ap.gov.in"

def fetch_census_data():
    print("[CENSUS] Fetching data from data.gov.in...")
    try:
        req = urllib.request.Request(CENSUS_API, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
            data = json.loads(resp.read())
            with open(os.path.join(DATA_DIR, "census_data.json"), "w") as f:
                json.dump(data, f, indent=2)
            print(f"[CENSUS] Saved {len(data.get('records', []))} records")
            return data
    except Exception as e:
        print(f"[CENSUS] API unavailable ({e}), using seed data")
        return None

def build_census_fallback():
    districts = [
        {"district": "Srikakulam", "population": 2703118, "male": 1348692, "female": 1354426, "literacy": 62.3, "sex_ratio": 1004, "density": 340, "households": 702110},
        {"district": "Vizianagaram", "population": 2344474, "male": 1168517, "female": 1175957, "literacy": 59.5, "sex_ratio": 1006, "density": 340, "households": 609604},
        {"district": "Visakhapatnam", "population": 4290589, "male": 2145128, "female": 2145461, "literacy": 68.0, "sex_ratio": 1000, "density": 340, "households": 1115561},
        {"district": "East Godavari", "population": 5154296, "male": 2578072, "female": 2576224, "literacy": 71.4, "sex_ratio": 999, "density": 470, "households": 1340065},
        {"district": "West Godavari", "population": 3934966, "male": 1970704, "female": 1964262, "literacy": 73.1, "sex_ratio": 997, "density": 430, "households": 1022791},
        {"district": "Krishna", "population": 4535278, "male": 2274615, "female": 2260663, "literacy": 74.5, "sex_ratio": 994, "density": 520, "households": 1179041},
        {"district": "Guntur", "population": 4887813, "male": 2446017, "female": 2441796, "literacy": 67.4, "sex_ratio": 998, "density": 430, "households": 1270418},
        {"district": "Prakasam", "population": 3397764, "male": 1711073, "female": 1686691, "literacy": 63.5, "sex_ratio": 986, "density": 230, "households": 883235},
        {"district": "Nellore", "population": 2966557, "male": 1490716, "female": 1475841, "literacy": 69.2, "sex_ratio": 990, "density": 290, "households": 771244},
        {"district": "Kadapa", "population": 2934456, "male": 1478793, "female": 1455663, "literacy": 67.9, "sex_ratio": 984, "density": 230, "households": 762957},
        {"district": "Chittoor", "population": 4174064, "male": 2099869, "female": 2074195, "literacy": 72.2, "sex_ratio": 988, "density": 280, "households": 1085086},
        {"district": "Anantapur", "population": 4081148, "male": 2067564, "female": 2013584, "literacy": 64.3, "sex_ratio": 974, "density": 220, "housesholds": 1061032},
        {"district": "Kurnool", "population": 4056842, "male": 2047190, "female": 2009652, "literacy": 61.1, "sex_ratio": 982, "density": 290, "households": 1054697}
    ]
    with open(os.path.join(DATA_DIR, "census_data.json"), "w") as f:
        json.dump({"records": districts, "source": "census_2011_seed"}, f, indent=2)
    print(f"[CENSUS] Built fallback data for {len(districts)} districts")
    return districts

def try_fetch_sec_data():
    print("[SEC] Attempting to fetch AP SEC election data...")
    try:
        req = urllib.request.Request(SEC_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as resp:
            html = resp.read().decode("utf-8")[:500]
            print(f"[SEC] Connected. HTML length: {len(html)} chars")
            with open(os.path.join(DATA_DIR, "sec_portal.html"), "w") as f:
                f.write(html)
            return True
    except Exception as e:
        print(f"[SEC] Cannot reach AP SEC portal ({e})")
        return False

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    print("=" * 50)
    print("AP GOVERNMENT DATA INGESTION PIPELINE")
    print("=" * 50)

    census = fetch_census_data()
    if not census:
        census = build_census_fallback()

    sec = try_fetch_sec_data()

    print("-" * 50)
    print("Ingestion complete. Files in:", DATA_DIR)
    for f in os.listdir(DATA_DIR):
        size = os.path.getsize(os.path.join(DATA_DIR, f))
        print(f"  {f}: {size/1024:.1f} KB")
