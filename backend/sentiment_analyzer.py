import re
import json

POSITIVE_WORDS_TE = [
    "ābhiVR̥ddhi", "ākarṣaṇīya", "āśīrvāda", "unnati", "aḍugu", "aṅgīkāraṁ",
    "pragati", "sēva", "ādarśaṁ", "rājī", "ātmīya", "sahāyaṁ",
    "bāhuḷyaṁ", "sāphalyamu", "cakkagā", "cālā", "navanirmāṇaṁ",
    "daya", "dōr̥kaka", "dhr̥ḍhatvaṁ", "gauravamu", "jayin̄cāḍu",
    "kāpāḍu", "kāvalē", "kr̥taṁ", "kūḍā", "mātraṁ", "māṭlāḍāḍaṁ",
    "nāyakatvaṁ", "nāśaṁ", "nirmāṇaṁ", "pāṭin̄cāḍu", "paryāyālu",
    "prabhutvaṁ", "pramāṇaṁ", "pūrṇaṁ", "rājyāṅgaṁ", "sādhakaṁ",
    "sādhanaṁ", "samājaṁ", "samagraṁ", "samarthana", "sampradāyaṁ",
    "santr̥pti", "sāphalyamu", "sāṭi", "sēva", "siddhāntaṁ",
    "sōdarulu", "sphūrti", "śrēṣṭha", "sthiraṁ", "sukhaṁ",
    "sūtrin̄cina", "svāgatamu", "tanakē", "unnataṁ", "unnaṭlu",
    "upayōgaṁ", "ūpiṁci", "vāgḍaṁbaṁ", "vaijayanti", "varana",
    "vinōdaṁ", "viplavaṁ", "viśālaṁ", "viṣayaṁ", "viśvāsamu",
    "yōgya", "అభివృద్ధి", "గెలుపు", "విజయం", "మంచి", "అభినందన",
    "స్వాగతం", "అభిమానం", "సహాయం", "సేవ", "ప్రగతి", "అంగీకారం",
    "నాయకత్వం", "ప్రజాసేవ", "ప్రతిజ్ఞ", "సంకల్పం", "ఆశీర్వాదం",
    "కృషి", "నిర్మాణం", "ఆదర్శం", "సమర్థత", "ప్రామాణికం",
    "ప్రభుత్వం", "ఆధునికం", "వికాసం", "సంక్షేమం", "అవకాశం",
    "భరోసా", "సంతృప్తి", "సదుపాయం", "పౌరసేవ", "సమగ్రత",
    "ప్రోత్సాహం", "జాగరూకత", "సంరక్షణ", "పరిష్కారం", "ఐక్యత",
    "సమర్ధవంతమైన", "సు-స్థిర", "న్యాయం", "శాంతి", "అహర్నిశలు",
    "సౌలభ్యం", "సాఫల్యం", "సమానత్వం", "సద్భావన", "ఆప్యాయత",
    "ఆత్మీయత", "సత్కార్యం", "శ్రేయస్సు", "ఆదాయం", "సుపరిపాలన",
    "పారదర్శకత", "సమర్థుడు", "నిజాయితీ", "క్రమశిక్షణ", "సహృదయం",
    # English sentiment words matching seed data headlines
    "mobilize", "support", "progress", "development", "welfare", "improve",
    "benefit", "growth", "positive", "stable", "secure", "strengthen",
    "advantage", "confidence", "invest", "employment", "opportunity",
    "service", "delivery", "satisfaction", "transparent", "efficient",
]

NEGATIVE_WORDS_TE = [
    "apahāraṁ", "apamānaṁ", "aśānta", "aṭaṅka", "baṅkti", "bāyulu",
    "bhr̥ṣṭācāraṁ", "cāṭu", "cētalu", "dādrā", "dōṣaṁ", "durōr̥kalu",
    "ekamataṁ", "gaddi", "ghātakaṁ", "gōlmal", "hatyā", "īrṣya",
    "jāgratha", "kapaṭaṁ", "kastūri", "kōpamu", "kṣatī", "kutra",
    "lagāḍaṁ", "lōbhi", "lōpala", "mōḍi", "mōsagaṭaṁ", "mudda",
    "nāśaṁ", "nikr̥ṣṭa", "nirlakṣya", "nirmaryāda", "nirvr̥tti",
    "nōkōli", "pāpamu", "parābhavaṁ", "pārparaṁ", "phōr",
    "pōḍupāṭu", "prajā-drōhaṁ", "pramādāla", "pratipāda",
    "prēranā", "rājī", "rākṣasika", "sakhāt", "samasyalu",
    "saṁghātaka", "sarpaṇa", "sastōka", "śatrutvaṁ", "sid'dhāntaṁ",
    "sthānaṁ", "tappu", "tirugu", "ughāḍaṁ", "vādaṁ", "vairaṁ",
    "vāñchita", "varadhi", "vēdanai", "viplavaṁ", "viṣamaṁ",
    "vyājaṁ", "అవినీతి", "అవినీతి", "అవకతవక", "సమస్య", "భ్రష్టాచారం",
    "దుర్భరం", "కుంభకోణం", "దుర్భరం", "అసహాయం", "అసమర్థత",
    "నిర్లక్ష్యం", "నిరుత్సాహం", "అసంతృప్తి", "దురాశ", "లోపం",
    "విఫలం", "అన్యాయం", "దారిద్య్రం", "కష్టం", "బాధ",
    "కోపం", "ద్వేషం", "అసూయ", "కలహం", "గొడవ", "తగాదా",
    "ద్రోహం", "మోసం", "పోరు", "సంక్షోభం", "అస్థిరత",
    "నిరాశ", "పరాజయం", "అపజయం", "వెట్టి", "వ్యాజ్యం",
    "బంద్", "ఆందోళన", "నిరసన", "దాడి", "హాని", "అభద్రత",
    "కొరత", "అవసరం", "లేమి", "అల్లరి", "అరాచకం",
    "దౌర్జన్యం", "అణచివేత", "భయం", "ఆందోళన", "నష్టం",
    # English sentiment words matching seed data headlines
    "protest", "violation", "irregularities", "rift", "crisis", "decline",
    "corruption", "delay", "failure", "negative", "unrest", "instability",
    "conflict", "dispute", "fraud", "mismanagement", "inefficiency",
    "grievance", "complaint", "shortage", "lack", "poor", "critical",
    "warning", "threat", "damage", "loss", "problem", "issue", "anger",
]

def analyze_text_sentiment(headlines, body_text=None):
    scores = []
    for item in headlines:
        text = item.get("headline", "") + " " + (body_text or "")
        text_lower = text.lower()
        pos_count = sum(1 for w in POSITIVE_WORDS_TE if w.lower() in text_lower)
        neg_count = sum(1 for w in NEGATIVE_WORDS_TE if w.lower() in text_lower)
        total = pos_count + neg_count
        if total == 0:
            score = 0.5
        else:
            score = pos_count / total
        scores.append(score)

    if not scores:
        return 0.5
    return sum(scores) / len(scores)


def compute_narrative_vector(wards):
    results = {}
    for ward in wards:
        news = ward.get("recent_news", [])
        sentiment = analyze_text_sentiment(news)

        fi = ward["field_intel"]
        cadre_ratio = 0
        total_cadre = sum(fi["cadre_density"].values())
        if total_cadre > 0:
            cadre_ratio = fi["cadre_density"].get("YSRCP", 0) / total_cadre

        nv = (sentiment * 0.5) + (cadre_ratio * 0.3) + (fi["candidate_popularity"].get("YSRCP", 0.5) * 0.2)
        results[ward["ward_id"]] = {
            "narrative_vector": round(nv, 4),
            "sentiment_score": round(sentiment, 4),
            "cadre_ratio": round(cadre_ratio, 4)
        }
    return results
