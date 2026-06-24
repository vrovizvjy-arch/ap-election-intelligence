DISTRICTS = [
    "Srikakulam", "Vizianagaram", "Visakhapatnam", "East Godavari",
    "West Godavari", "Krishna", "Guntur", "Prakasam",
    "Nellore", "Chittoor", "Kadapa", "Anantapur",
    "Kurnool"
]

MANDALS = {
    "Guntur": ["Guntur", "Tenali", "Mangalagiri", "Ponnur", "Repalle", "Bapatla", "Chilakaluripet", "Narasaraopet"],
    "Krishna": ["Machilipatnam", "Vijayawada", "Nuzvid", "Gudivada", "Pedana", "Avanigadda", "Mylavaram", "Tiruvuru"],
    "Visakhapatnam": ["Visakhapatnam", "Anakapalli", "Bheemunipatnam", "Pendurthi", "Chodavaram", "Narsipatnam", "Yelamanchili", "Madugula"],
    "East Godavari": ["Kakinada", "Rajahmundry", "Amalapuram", "Kothapeta", "Razole", "Pithapuram", "Samalkota", "Tuni"],
    "West Godavari": ["Eluru", "Bhimavaram", "Tadepalligudem", "Nidadavolu", "Kovvur", "Palakollu", "Tanuku", "Jangareddygudem"],
    "Chittoor": ["Chittoor", "Tirupati", "Madanapalle", "Palamaner", "Srikalahasti", "Puttur", "Nagari", "Punganur"],
    "Kurnool": ["Kurnool", "Nandyal", "Adoni", "Yemmiganur", "Banaganapalle", "Dhone", "Pattikonda", "Allagadda"],
    "Anantapur": ["Anantapur", "Hindupur", "Dharmavaram", "Guntakal", "Tadipatri", "Penukonda", "Rayadurg", "Kalyandurg"],
    "Nellore": ["Nellore", "Gudur", "Kavali", "Venkatagiri", "Sullurpeta", "Naidupeta", "Rapur", "Atmakur"],
    "Prakasam": ["Ongole", "Markapur", "Chirala", "Kandukur", "Addanki", "Darsi", "Podili", "Kotha"],
    "Kadapa": ["Kadapa", "Proddatur", "Badvel", "Jammalamadugu", "Pulivendula", "Rayachoti", "Mydukur", "Kamalapuram"],
    "Srikakulam": ["Srikakulam", "Palasa", "Tekkali", "Ichapuram", "Amadalavalasa", "Narasannapeta", "Pathapatnam", "Kotabommali"],
    "Vizianagaram": ["Vizianagaram", "Parvathipuram", "Bobbili", "Saluru", "Cheepurupalli", "Gajapathinagaram", "Nellimarla", "Kurupam"]
}

CASTE_GROUPS = {
    "kapu": {"pct_range": (10, 28), "label": "Kapu"},
    "kamma": {"pct_range": (3, 12), "label": "Kamma"},
    "reddy": {"pct_range": (8, 22), "label": "Reddy"},
    "bc_boya": {"pct_range": (5, 18), "label": "BC-Boya"},
    "bc_yadava": {"pct_range": (3, 10), "label": "BC-Yadava"},
    "bc_padmashali": {"pct_range": (2, 8), "label": "BC-Padmashali"},
    "bc_others": {"pct_range": (8, 20), "label": "BC-Others"},
    "sc_madiga": {"pct_range": (3, 10), "label": "SC-Madiga"},
    "sc_mala": {"pct_range": (3, 8), "label": "SC-Mala"},
    "st": {"pct_range": (1, 5), "label": "ST"},
    "minorities": {"pct_range": (2, 8), "label": "Minorities"}
}

WELFARE_SCHEMES = ["Amma Vodi", "YSR Cheyutha", "Pension Kanuka", "Rythu Bharosa", "Navaratnalu"]

PARTIES = {
    "YSRCP": {"color": "#FF0000", "label": "YSR Congress Party"},
    "TDP": {"color": "#FFFF00", "label": "Telugu Desam Party"},
    "JSP": {"color": "#0000FF", "label": "Jana Sena Party"},
    "BJP": {"color": "#FF9933", "label": "Bharatiya Janata Party"},
    "IND": {"color": "#808080", "label": "Independent"}
}
