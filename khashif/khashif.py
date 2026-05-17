import feedparser
import google.generativeai as genai
import schedule
import time
import json
import os
import urllib.request
import re
from datetime import datetime
from groq import Groq
from cerebras.cloud.sdk import Cerebras

# === CONFIG ===
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
CEREBRAS_API_KEY = os.environ.get("CEREBRAS_API_KEY", "")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_FILE = os.path.join(SCRIPT_DIR, "khashif_memory.json")
REPORT_FILE = os.path.join(SCRIPT_DIR, "khashif_report.txt")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash-lite")
groq_client = Groq(api_key=GROQ_API_KEY)
cerebras_client = Cerebras(api_key=CEREBRAS_API_KEY)

# === KHASHIF — Single Agent, Full Cycle ===
# Morning/afternoon: explore, find, classify
# Evening: strategic report + comment drafts
# Always: learn, grow, connect

PROFILE = """
Tagmac Cankaya. Based in Lefkosa, North Cyprus.

IDENTITY: Lawyer, entrepreneur, farmer, gong maker, musician, sound therapist,
social movement pioneer, AI hybrid producer, traveler, coffee expert.

CREATES: Gong (handmade), drone sound, sound bath, breathwork, improvisation,
ambient music. 19 tracks on SoundCloud.

BUILDS: casacaravan.space, Tagmac Wellness App, Khashif (this agent).

INCOME SKILLS: AI integration consulting, market research & competitive
intelligence, legal research, sound therapy (Sonic Journey), fermentation
consulting, social movement strategy, community building.

INTERESTS: Sound healing, fermentation, consciousness, resonance, collective
creation, permaculture, traditional farming, natural building, alternative
economy, social movements, open source, AI ethics, Mediterranean culture,
specialty coffee, upcycling, somatic practices.

INSTRUMENTS: gong, flute, handpan, djembe, singing bowls, didgeridoo.
HOME: casacaravan.space
SEEKING: resonant people, collaborators, income opportunities, communities.
VALUES: authenticity, non-commercial, heart-driven, open source spirit.
"""

# === FOUR BUCKETS ===
# HUMAN   — real producer, potential collaborator
# INCOME  — can convert to money
# KNOWLEDGE — expands Tagmac's world
# TRASH   — no real value

# === KEYWORDS ===
BASE_KEYWORDS = [
    "gong", "handpan", "sound bath", "sound healing", "breathwork",
    "improvisation", "ambient", "drone", "resonance", "sound therapy",
    "vibration", "frequency", "soundscape", "field recording", "deep listening",
    "sound art", "percussion", "binaural", "sacred sound", "sound ceremony",
    "medicine music", "healing arts", "overtone", "didgeridoo", "sonic",
    "junto", "sound walk", "acoustic ecology", "djembe", "flute",
    "singing bowl", "shamanic", "collaborative", "experimental",
    "fermentation", "wild fermentation", "kefir", "kombucha", "sourdough",
    "fermented", "probiotic", "starter culture", "lacto", "miso",
    "somatic", "nervous system", "qigong", "holotropic", "ecstatic",
    "vagus nerve", "meditation", "consciousness", "embodiment",
    "cooperative", "commons", "barter", "community economy", "solidarity",
    "alternative economy", "open source", "creative commons", "diy",
    "maker", "craft", "upcycle", "repair",
    "permaculture", "regenerative", "natural farming", "seed saving",
    "traditional farming", "rewilding", "biodynamic", "agroforestry",
    "activism", "social movement", "collective", "mutual aid", "grassroots",
    "ai integration", "automation", "market research", "competitive analysis",
    "lead generation", "digital transformation", "consulting", "freelance",
    "cyprus", "mediterranean", "lefkosa", "nicosia", "kibris",
]

SKIP_KEYWORDS = [
    "buy now", "purchase", "sale", "discount", "sponsored",
    "advertisement", "shop now", "promo code", "casino", "betting",
]

# === FEEDS ===
# Sabit liste yok — Khashif kaldığı yerden devam eder.
# İlk çalışma için seed feed'ler — sonrası memory'den büyür.
SEED_FEEDS = [
    "https://disquiet.com/feed/",
    "https://www.wildfermentation.com/feed/",
    "https://www.permaculturenews.org/feed/",
    "https://opensource.com/feed",
]


# === SUPABASE MEMORY ===
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://iwfvlatywksvnnxymweb.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

def _supa_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }

def supa_get_memory():
    """Supabase'den hafızayı yükle"""
    if not SUPABASE_KEY:
        return None
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/khashif_memory?key=eq.main&select=value",
            headers={**_supa_headers(), "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
            if data:
                return json.loads(data[0]["value"])
    except Exception as e:
        print(f"  ! Supabase load failed: {e}")
    return None

def supa_save_memory(memory):
    """Hafızayı Supabase'e kaydet (upsert)"""
    if not SUPABASE_KEY:
        return
    try:
        payload = json.dumps({
            "key": "main",
            "value": json.dumps(memory, ensure_ascii=False),
            "updated_at": datetime.now().isoformat()
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/khashif_memory",
            data=payload,
            headers={**_supa_headers(), "Prefer": "resolution=merge-duplicates,return=minimal"},
            method="POST"
        )
        urllib.request.urlopen(req, timeout=10)
        print("  ✓ Memory saved to Supabase")
    except Exception as e:
        print(f"  ! Supabase save failed: {e}")

def supa_get_commands():
    """Operatör komutlarını Supabase'den al"""
    if not SUPABASE_KEY:
        return []
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/khashif_commands?status=eq.pending&select=*&order=created_at.asc",
            headers={**_supa_headers(), "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"  ! Supabase commands load failed: {e}")
        return []

def supa_mark_command_done(cmd_id):
    """Komutu işlendi olarak işaretle"""
    if not SUPABASE_KEY:
        return
    try:
        payload = json.dumps({"status": "done"}).encode("utf-8")
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/khashif_commands?id=eq.{cmd_id}",
            data=payload,
            headers=_supa_headers(),
            method="PATCH"
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"  ! Supabase command update failed: {e}")

# === MEMORY ===
def load_memory():
    # Supabase önce dene
    supa_mem = supa_get_memory()
    if supa_mem:
        print("  ✓ Memory loaded from Supabase")
        return supa_mem
    # Yedek: local JSON
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                print("  ~ Memory loaded from local JSON")
                return json.load(f)
    except Exception:
        pass
    print("  ~ Fresh memory (no previous state)")
    return {
        "seen_links": [],
        "buckets": {"HUMAN": [], "INCOME": [], "KNOWLEDGE": [], "TRASH": []},
        "action_queue": [],
        "acted": [],
        "dynamic_feeds": [],
        "visited_feeds": [],
        "crawled_pages": [],
        "learned_keywords": [],
        "decisions": [],
        "operator_commands": [],
        "stats": {"total_analyzed": 0, "total_resonant": 0},
        "sessions": []
    }

def save_memory(memory):
    # Supabase'e kaydet
    supa_save_memory(memory)
    # Yedek: local JSON
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  ! Local memory save failed: {e}")

# === LLM LAYERS ===
LLM_STATUS = {"cerebras_fails": 0, "groq_fails": 0}

def call_cerebras(prompt):
    r = cerebras_client.chat.completions.create(
        model="llama3.1-8b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    return r.choices[0].message.content.strip()

def call_groq(prompt):
    r = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=400
    )
    return r.choices[0].message.content.strip()

def call_gemini(prompt):
    return gemini_model.generate_content(prompt).text.strip()

def llm(prompt, max_tokens=400):
    if LLM_STATUS["cerebras_fails"] < 3:
        try:
            r = call_cerebras(prompt)
            LLM_STATUS["cerebras_fails"] = 0
            return r, "cerebras"
        except Exception:
            LLM_STATUS["cerebras_fails"] += 1
            time.sleep(5)
    if LLM_STATUS["groq_fails"] < 3:
        try:
            r = call_groq(prompt)
            LLM_STATUS["groq_fails"] = 0
            return r, "groq"
        except Exception:
            LLM_STATUS["groq_fails"] += 1
            time.sleep(10)
    for _ in range(2):
        try:
            return call_gemini(prompt), "gemini"
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                time.sleep(30)
    return "BUCKET: TRASH\nSCORE: 0\nREASON: all layers failed\nACTION: IGNORE\nKEYWORDS: NONE", "none"

# === WEB ===
def fetch_page(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.read(10000).decode("utf-8", errors="ignore")
    except Exception:
        return ""

def extract_rss(html, base_url=""):
    links = []
    for p in [r'type=["\']application/rss\+xml["\'][^>]*href=["\']([^"\']+)["\']',
               r'href=["\']([^"\']*(?:feed|rss)[^"\']*)["\']']:
        for m in re.findall(p, html, re.IGNORECASE):
            if m.startswith("http"):
                links.append(m)
            elif m.startswith("/") and base_url:
                d = re.match(r'https?://[^/]+', base_url)
                if d:
                    links.append(d.group() + m)
    return list(set(links))

def valid_rss(url):
    try:
        return len(feedparser.parse(url).entries) > 0
    except Exception:
        return False

def crawl(url, known, crawled):
    if url in crawled:
        return []
    html = fetch_page(url)
    if not html:
        return []
    crawled.append(url)
    found = []
    for r in extract_rss(html, url):
        if r not in known and valid_rss(r):
            found.append(r)
            print(f"  ++ New RSS: {r[:60]}")
    return found[:3]

# === FILTERS ===
def quick_filter(title, content, learned):
    text = (title + " " + content).lower()
    if any(k in text for k in SKIP_KEYWORDS):
        return False
    return sum(1 for k in BASE_KEYWORDS + learned if k in text) >= 1

def parse(text):
    r = {}
    for line in text.strip().split("\n"):
        if ":" in line:
            k, v = line.split(":", 1)
            r[k.strip().upper()] = v.strip()
    return r

# === ANALYZE ===
def analyze(title, content, source, is_priority):
    prompt = f"""You are Khashif — a silent ambassador for Tagmac Cankaya.
{"PRIORITY SOURCE — direct action possible." if is_priority else ""}

PROFILE: {PROFILE}

Title: {title}
Source: {source}
Content: {content[:900]}

CLASSIFY:
- HUMAN: Real producer/artist — potential collaborator
- INCOME: Can convert to money for Tagmac
- KNOWLEDGE: Expands Tagmac's world
- TRASH: No real value

ACTION:
- COMMENT: Leave a comment (priority sources)
- SUBMIT: Submit music/work
- ATTEND: Attend/apply to event
- RESEARCH: Data Tagmac can sell
- CONNECT: Reach out directly
- FOLLOW: Keep watching
- IGNORE: Not worth returning

Reply ONLY:
BUCKET: (HUMAN/INCOME/KNOWLEDGE/TRASH)
SCORE: (1-10)
REASON: (one sentence Turkish)
ACTION: (one of above)
ACTION_NOTE: (exactly what to do)
KEYWORDS: (2-3 keywords or NONE)"""

    return llm(prompt)

# === EVENING REPORT ===
def evening_report(memory):
    queue = memory.get("action_queue", [])
    buckets = memory.get("buckets", {})
    learned = memory.get("learned_keywords", [])

    if not queue and not buckets.get("HUMAN") and not buckets.get("INCOME"):
        print("  Rapor icin yeterli veri yok.")
        return

    context = f"""
PENDING ACTIONS: {len(queue)}
HUMAN bucket: {len(buckets.get('HUMAN', []))} people found
INCOME bucket: {len(buckets.get('INCOME', []))} opportunities
LEARNED: {', '.join(learned[:20])}

RECENT FINDINGS:
"""
    for item in queue[-15:]:
        context += f"[{item.get('action','?')}] {item.get('title','')} — {item.get('action_note','')}\n"

    # Strategic analysis
    analysis_prompt = f"""You are Khashif — both scout and strategist for Tagmac Cankaya.

PROFILE: {PROFILE}

TODAY'S FINDINGS:
{context}

Write a strategic evening report in Turkish. Include:

BUGÜNÜN ÖNCELİKLİ EYLEMLERİ (max 3):
- Exact what to do, where, why

STRATEJİK GÖZLEMLER:
- Patterns emerging
- Strongest communities
- New opportunities

İÇERİK ÖNERİLERİ:
- What to create next for casacaravan.space

AĞ DURUMU:
- How the network is developing

Be direct, specific, actionable. No fluff."""

    analysis, layer = llm(analysis_prompt)
    print(f"  Analiz tamamlandi [{layer}]")

    # Comment drafts for top COMMENT actions
    comment_items = [i for i in queue if i.get("action") == "COMMENT"][:3]
    drafts = {}

    for item in comment_items:
        draft_prompt = f"""Write a genuine comment for Tagmac to leave on this content.

TAGMAC: {PROFILE}

Content: {item.get('title','')}
URL: {item.get('link','')}
Source: {item.get('source','')}

Comment must:
- Be specific and authentic
- Mention casacaravan.space naturally if relevant
- Open a door for connection
- Sound like Tagmac — musician, sound therapist, not marketer
- 3-5 sentences max
- Match language of source (usually English)"""

        draft, _ = llm(draft_prompt)
        drafts[item.get("link", "")] = draft
        time.sleep(5)

    # Write report
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    report = f"""
{'='*55}
KHASHIF RAPORU — {now}
{'='*55}

{analysis}

{'='*55}
YORUM TASLAKLARI — TETIGI SEN CEKECEKSIN
{'='*55}
"""
    for item in comment_items:
        draft = drafts.get(item.get("link", ""), "Taslak hazirlanamadi.")
        report += f"""
[ ] {item.get('title', '')}
    {item.get('link', '')}

    TASLAK:
    {draft}

    --- onayladiktan sonra: [YAPILDI] ---

"""

    report += f"""
{'='*55}
TUM BEKLEYEN EYLEMLER ({len(queue)})
{'='*55}
"""
    for i, item in enumerate(queue, 1):
        report += f"""
{i}. [{item.get('action','?')}] {item.get('title','')}
   {item.get('link','')}
   Not: {item.get('action_note','')}
   Durum: {item.get('status','pending')}
"""

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(report)
    print(f"\n  Rapor kaydedildi: {REPORT_FILE}")

# === SELF IMPROVEMENT ===
def self_improve(memory, learned):
    decisions = memory.get("decisions", [])
    if len(decisions) < 5:
        return learned
    from collections import Counter
    approved_kw = []
    for d in decisions[-50:]:
        if d.get("verdict") == "YES":
            approved_kw.extend(d.get("keywords", []))
    for kw, count in Counter(approved_kw).items():
        if count >= 2 and kw not in learned:
            learned.append(kw)
            print(f"  ++ Self-learned: {kw}")
    return learned


# === INTERSECTION INTELLIGENCE ===
INTERSECTION_PAIRS = [
    ("sound", "fermentation", "Ses + Fermentasyon"),
    ("sound", "mental health", "Ses + Mental Sağlık"),
    ("sound", "maker", "Ses + Maker"),
    ("sound", "consciousness", "Ses + Bilinç"),
    ("fermentation", "mental health", "Fermentasyon + Mental Sağlık"),
    ("fermentation", "maker", "Fermentasyon + Maker"),
    ("coffee", "fermentation", "Kahve + Fermentasyon"),
    ("coffee", "sound", "Kahve + Ses"),
    ("breathwork", "sound", "Nefes + Ses"),
    ("breathwork", "mental health", "Nefes + Mental Sağlık"),
    ("permaculture", "fermentation", "Permakültür + Fermentasyon"),
    ("somatic", "sound", "Somatik + Ses"),
    ("open source", "sound", "Açık Kaynak + Ses"),
    ("maker", "mental health", "Maker + Mental Sağlık"),
]

DOMAIN_KEYWORDS = {
    "sound": ["gong", "sound bath", "sound healing", "handpan", "drone", "resonance",
              "ambient", "binaural", "overtone", "singing bowl", "soundscape", "sonic",
              "frequency", "vibration", "acoustic", "sound therapy"],
    "fermentation": ["fermentation", "kefir", "kombucha", "sourdough", "miso",
                     "lacto", "probiotic", "starter culture", "wild fermentation",
                     "fermented", "microbiome"],
    "mental health": ["mental health", "anxiety", "stress", "nervous system", "vagus nerve",
                      "meditation", "consciousness", "burnout", "somatic", "embodiment",
                      "breathwork", "holotropic", "ecstatic", "wellbeing", "mindfulness"],
    "maker": ["maker", "diy", "craft", "upcycle", "repair", "open source",
              "creative commons", "workshop", "handmade", "artisan", "build"],
    "coffee": ["coffee", "specialty coffee", "third wave", "espresso", "pour over",
               "roast", "brew", "barista"],
    "consciousness": ["consciousness", "psychedelic", "holotropic", "awareness",
                      "awakening", "spiritual", "contemplative"],
    "breathwork": ["breathwork", "breathing", "breath", "pranayama", "holotropic",
                   "vagus", "parasympathetic"],
    "permaculture": ["permaculture", "regenerative", "natural farming", "rewilding",
                     "biodynamic", "agroforestry", "seed saving"],
    "open source": ["open source", "creative commons", "commons", "cooperative",
                    "solidarity", "mutual aid", "barter"],
    "somatic": ["somatic", "embodiment", "body", "nervous system", "trauma", "movement"],
}

def detect_domain(text):
    """Bir metnin hangi domainlere girdiğini tespit et"""
    text = text.lower()
    domains = []
    for domain, keywords in DOMAIN_KEYWORDS.items():
        if any(k in text for k in keywords):
            domains.append(domain)
    return domains

def find_intersections(session_items):
    """Session bulgularında intersection noktalarını bul"""
    intersections = []

    # Her item için domain tespiti yap
    items_with_domains = []
    for item in session_items:
        text = (item.get("title", "") + " " + item.get("reason", "") +
                " " + item.get("action_note", "")).lower()
        domains = detect_domain(text)
        if domains:
            items_with_domains.append({**item, "domains": domains})

    # Tanımlı intersection çiftlerini kontrol et
    found_pairs = {}
    for d1, d2, label in INTERSECTION_PAIRS:
        items_d1 = [i for i in items_with_domains if d1 in i["domains"]]
        items_d2 = [i for i in items_with_domains if d2 in i["domains"]]

        if items_d1 and items_d2:
            pair_key = f"{d1}_{d2}"
            if pair_key not in found_pairs:
                found_pairs[pair_key] = {
                    "label": label,
                    "domain1": d1,
                    "domain2": d2,
                    "items": items_d1[:2] + items_d2[:2],
                    "strength": len(items_d1) + len(items_d2)
                }

    # Gücüne göre sırala
    intersections = sorted(found_pairs.values(), key=lambda x: x["strength"], reverse=True)
    return intersections[:5]  # En güçlü 5

def intersection_to_insight(intersection, memory):
    """LLM ile intersection'dan insight üret"""
    items_text = ""
    for item in intersection["items"][:4]:
        items_text += f"- [{item.get('bucket','?')}] {item.get('title', '')} ({item.get('source', '')})\n"
        items_text += f"  {item.get('reason', '')}\n"

    prompt = f"""You are Khashif — intersection intelligence for Tagmac Cankaya.

PROFILE: {PROFILE}

INTERSECTION DETECTED: {intersection['label']}
Strength: {intersection['strength']} findings

Items found in both domains:
{items_text}

Su + un = ekmek mantığıyla düşün. Bu iki domain birleşince ne üretiyor?

Türkçe olarak şunları yaz:
REZONANS: Bu kesişim neden önemli? Tagmac için ne ifade ediyor? (1-2 cümle)
FIRSAT: Somut ne yapılabilir? İçerik, bağlantı, gelir? (1-2 cümle)
KOVA: HUMAN / INCOME / KNOWLEDGE (hangisi ve neden tek cümle)
EYLEM: Şimdi ne yapılmalı? (tek cümle, somut)"""

    result, layer = llm(prompt)
    return result, layer

def send_intersection_email(intersections, insights, layers_used):
    """Intersection tespitlerini email ile gönder"""
    resend_key = os.environ.get("RESEND_API_KEY", "")
    if not resend_key:
        print("  ! Resend key yok — email atlanamadı")
        return

    now = datetime.now().strftime("%d.%m.%Y %H:%M")

    body = f"""𓆟 KHASHIF — INTERSECTION INTELLIGENCE
{now}
{"=" * 55}

{len(intersections)} KESİŞİM NOKTASI BULUNDU

"""
    for i, (intersection, (insight, layer)) in enumerate(zip(intersections, insights), 1):

        # insight'ı parse et
        parsed = {}
        for line in insight.strip().split("\n"):
            if ":" in line:
                k, v = line.split(":", 1)
                parsed[k.strip().upper()] = v.strip()

        rezonans = parsed.get("REZONANS", insight[:150])
        firsat = parsed.get("FIRSAT", "")
        kova = parsed.get("KOVA", "KNOWLEDGE")
        eylem = parsed.get("EYLEM", "")

        body += f"""{"=" * 55}
{i}. {intersection['label'].upper()}
   Güç: {intersection['strength']} bulgu | LLM: {layer}
{"=" * 55}

REZONANS:
{rezonans}

FIRSAT:
{firsat}

KOVA: {kova}

EYLEM:
{eylem}

Kaynaklar:
"""
        for item in intersection["items"][:3]:
            body += f"  [{item.get('bucket','?')}] {item.get('title', '')[:60]}\n"
            body += f"  {item.get('link', '')}\n"
            if item.get('reason'):
                body += f"  → {item.get('reason', '')}\n"
            body += "\n"

        body += "\n"

    body += f"""{"=" * 55}
LLM katmanları: {', '.join(set(l for _, (_, l) in zip(intersections, insights)))}
casacaravan.space | khashif
{"=" * 55}
"""

    try:
        payload = json.dumps({
            "from": "khashif@casacaravan.space",
            "to": ["tagmacc@gmail.com"],
            "subject": f"𓆟 {len(intersections)} Kesişim — {', '.join(ix['label'] for ix in intersections[:2])} — {now}",
            "text": body
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=payload,
            headers={
                "Authorization": f"Bearer {resend_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            print(f"  ✓ Intersection email gönderildi — {len(intersections)} kesişim")
    except Exception as e:
        print(f"  ! Email hatası: {e}")

def run_intersection_intelligence(session, memory):
    """Session bulgularında intersection intelligence çalıştır"""
    print(f"\n--- Intersection Intelligence ---")

    # TRASH hariç tüm session itemları
    all_items = []
    for bucket in ["HUMAN", "INCOME", "KNOWLEDGE"]:
        all_items.extend(session.get(bucket, []))

    if len(all_items) < 2:
        print("  Yeterli bulgu yok — en az 2 item gerekli")
        return

    # Intersection bul
    intersections = find_intersections(all_items)

    if not intersections:
        print("  Bu session'da intersection tespit edilmedi")
        return

    print(f"  {len(intersections)} intersection bulundu:")
    for ix in intersections:
        print(f"  ++ {ix['label']} (güç: {ix['strength']})")

    # Her intersection için insight üret
    insights = []
    insights_with_layers = []
    for ix in intersections[:3]:
        insight, layer = intersection_to_insight(ix, memory)
        insights.append(insight)
        insights_with_layers.append((insight, layer))
        print(f"  → [{layer}] {ix['label']}: {insight[:80]}...")
        time.sleep(5)

    # Supabase'e kaydet
    intersection_data = []
    for ix, (insight, layer) in zip(intersections, insights_with_layers):
        intersection_data.append({
            "date": datetime.now().strftime("%d.%m.%Y %H:%M"),
            "label": ix["label"],
            "strength": ix["strength"],
            "insight": insight,
            "layer": layer,
            "items": [{"title": i.get("title"), "link": i.get("link")} for i in ix["items"]]
        })

    memory.setdefault("intersections", [])
    memory["intersections"].extend(intersection_data)
    memory["intersections"] = memory["intersections"][-100:]  # Son 100

    # Email gönder
    send_intersection_email(intersections[:3], insights_with_layers)

    return intersections


def khashif_run():
    now = datetime.now()
    is_evening = now.hour >= 20 or now.hour < 2

    print(f"\n{'='*50}")
    print(f"  Khashif — {now.strftime('%d.%m.%Y %H:%M')}")
    print(f"  {'Aksam modu — gezi + rapor' if is_evening else 'Gezi modu'}")
    print(f"{'='*50}")

    LLM_STATUS["cerebras_fails"] = 0
    LLM_STATUS["groq_fails"] = 0

    memory = load_memory()
    seen = set(memory.get("seen_links", []))
    buckets = memory.get("buckets", {"HUMAN": [], "INCOME": [], "KNOWLEDGE": [], "TRASH": []})
    action_queue = memory.get("action_queue", [])
    dynamic_feeds = memory.get("dynamic_feeds", [])
    visited = memory.get("visited_feeds", [])
    crawled = memory.get("crawled_pages", [])
    learned = memory.get("learned_keywords", [])
    stats = memory.get("stats", {"total_analyzed": 0, "total_resonant": 0})

    learned = self_improve(memory, learned)

    # === OPERATOR COMMANDS ===
    commands = supa_get_commands()
    if commands:
        print(f"\n--- Operator Komutları ({len(commands)}) ---")
        for cmd in commands:
            cmd_text = cmd.get("text", "")
            cmd_id = cmd.get("id", "")
            print(f"  CMD: {cmd_text[:60]}")
            # Komutu araştırmaya ekle - priority feed gibi işle
            if cmd_text:
                memory.setdefault("operator_commands", []).append({
                    "text": cmd_text,
                    "date": now.strftime("%d.%m.%Y %H:%M"),
                    "status": "processing"
                })
                # LLM ile komuta özel araştırma
                cmd_prompt = f"""You are Khashif — research agent for Tagmac Cankaya.

PROFILE: {PROFILE}

OPERATOR COMMAND: {cmd_text}

Research this command. Find relevant information, connections, opportunities.
Reply in Turkish with:
BULGU: (what you found, 2-3 sentences)
EYLEM: (what action to take)
KAYNAK: (any relevant links or sources)
REZONANS: (1-5, how relevant this is)"""
                result, layer = llm(cmd_prompt)
                p = parse(result)
                if p.get("REZONANS", "0") not in ["0", "1"]:
                    action_queue.append({
                        "date": now.strftime("%d.%m.%Y %H:%M"),
                        "title": f"[CMD] {cmd_text[:50]}",
                        "link": "",
                        "source": "operator_command",
                        "score": p.get("REZONANS", "3"),
                        "reason": p.get("BULGU", ""),
                        "action": "RESEARCH",
                        "action_note": p.get("EYLEM", "") + " " + p.get("KAYNAK", ""),
                        "bucket": "KNOWLEDGE",
                        "layer": layer,
                        "status": "pending",
                        "keywords": []
                    })
                supa_mark_command_done(cmd_id)

    # Feed listesi: memory'deki dynamic_feeds önce (kaldığı yer),
    # sonra seed feeds (henüz dynamic'e girmemişse)
    seed_set = set(SEED_FEEDS)
    all_feeds = list(dict.fromkeys(
        dynamic_feeds +
        [f for f in SEED_FEEDS if f not in dynamic_feeds]
    ))
    # İlk çalışmada dynamic_feeds boşsa seed'den başla
    if not all_feeds:
        all_feeds = list(SEED_FEEDS)

    print(f"  Feed listesi: {len(dynamic_feeds)} crawled + {len([f for f in SEED_FEEDS if f not in dynamic_feeds])} seed = {len(all_feeds)} toplam")
    for f in all_feeds:
        if f not in visited:
            visited.append(f)

    known_set = set(all_feeds)
    session = {"HUMAN": [], "INCOME": [], "KNOWLEDGE": [], "TRASH": []}
    llm_calls = 0
    layers = {"cerebras": 0, "groq": 0, "gemini": 0, "none": 0}
    resonant_links = []

    print(f"  {len(seen)} links seen | {len(all_feeds)} RSS | {len(action_queue)} pending actions")

    # === PHASE 1: READ ===
    print(f"\n--- Gezme ---")
    for feed_url in all_feeds:
        is_seed = feed_url in seed_set
        try:
            feed = feedparser.parse(feed_url)
            title_f = feed.feed.get("title", feed_url)[:38]
            new = [e for e in feed.entries[:3] if e.get("link", "") not in seen]
            if not new:
                continue
            print(f"\n{'[S]' if is_seed else '[C]'} {title_f} ({len(new)} new)")
            for entry in new:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                content = entry.get("summary", entry.get("description", "")).strip()
                if not title or not link:
                    continue
                seen.add(link)
                if not quick_filter(title, content, learned):
                    print(f"  . {title[:55]}")
                    continue
                print(f"  o {title[:55]}")
                raw, layer = analyze(title, content, title_f, is_seed)
                layers[layer] += 1
                llm_calls += 1
                stats["total_analyzed"] += 1
                time.sleep(8)

                p = parse(raw)
                bucket = p.get("BUCKET", "TRASH")
                score = p.get("SCORE", "0")
                reason = p.get("REASON", "")
                action = p.get("ACTION", "FOLLOW")
                action_note = p.get("ACTION_NOTE", "")

                kw = p.get("KEYWORDS", "")
                if kw and kw.upper() != "NONE":
                    for k in kw.split(","):
                        k = k.strip().lower()
                        if k and k not in learned and k not in BASE_KEYWORDS:
                            learned.append(k)

                if bucket != "TRASH":
                    item = {
                        "date": now.strftime("%d.%m.%Y %H:%M"),
                        "title": title, "link": link,
                        "source": title_f, "score": score,
                        "reason": reason, "action": action,
                        "action_note": action_note,
                        "bucket": bucket, "layer": layer,
                        "status": "pending"
                    }
                    buckets[bucket].append(item)
                    session[bucket].append(item)
                    resonant_links.append(link)
                    stats["total_resonant"] += 1

                    if action in ["COMMENT", "SUBMIT", "ATTEND", "CONNECT", "RESEARCH"]:
                        existing = [q["link"] for q in action_queue]
                        if link not in existing:
                            action_queue.append(item)
                        print(f"  *** [{bucket}][{score}][{layer}] → {action}: {title[:38]}")
                    else:
                        print(f"  >>> [{bucket}][{score}] → {action}: {title[:40]}")
                else:
                    print(f"  x [TRASH] {title[:50]}")
        except Exception as e:
            print(f"  ! {feed_url[:40]}: {str(e)[:40]}")

    # === PHASE 2: CRAWL ===
    print(f"\n--- Crawl ({len(resonant_links)} sayfa) ---")
    new_rss = 0
    for url in resonant_links[:5]:
        time.sleep(2)
        for rss in crawl(url, known_set, crawled):
            if rss not in dynamic_feeds:
                dynamic_feeds.append(rss)
                visited.append(rss)
                known_set.add(rss)
                new_rss += 1
    print(f"  {new_rss} new RSS added")

    # === SAVE ===
    for b in buckets:
        buckets[b] = buckets[b][-200:]
    action_queue = action_queue[-100:]

    memory.update({
        "seen_links": list(seen)[-3000:],
        "buckets": buckets,
        "action_queue": action_queue,
        "dynamic_feeds": dynamic_feeds[-200:],
        "visited_feeds": list(dict.fromkeys(visited))[-300:],
        "crawled_pages": crawled[-500:],
        "learned_keywords": learned[-300:],
        "stats": stats
    })
    save_memory(memory)

    # === REPORT ===
    total = sum(len(v) for v in session.values())
    actions = [i for b in session.values() for i in b
               if i.get("action") in ["COMMENT","SUBMIT","ATTEND","CONNECT","RESEARCH"]]

    print(f"\n{'='*50}")
    print(f"  RAPOR — {now.strftime('%H:%M')}")
    print(f"  LLM: {llm_calls} (C:{layers['cerebras']} G:{layers['groq']} Ge:{layers['gemini']})")
    print(f"  Bulunanlar: HUMAN:{len(session['HUMAN'])} INCOME:{len(session['INCOME'])} KNOWLEDGE:{len(session['KNOWLEDGE'])}")
    print(f"  Eylemler: {len(actions)} | Toplam kuyruk: {len(action_queue)}")
    print(f"  RSS: {len(visited)}")
    print(f"{'='*50}")

    if session["INCOME"]:
        print(f"\n GELIR:\n")
        for b in session["INCOME"]:
            print(f"  [{b['score']}] {b['title']}\n  {b['link']}\n  → {b['action_note']}\n")

    if session["HUMAN"]:
        print(f"\n INSAN:\n")
        for b in session["HUMAN"]:
            print(f"  [{b['score']}] {b['title']}\n  {b['link']}\n  → {b['reason']}\n")

    if actions:
        print(f"\n EYLEMLER:\n")
        for b in actions:
            print(f"  [{b['action']}] {b['title']}\n  {b['link']}\n  {b['action_note']}\n")

    print(f"\n TUM RSS FEED LERİ ({len(all_feeds)}):")
    for f in all_feeds:
        tag = "[S]" if f in seed_set else "[C]"
        print(f"  {tag} {f}")

    # === INTERSECTION INTELLIGENCE ===
    run_intersection_intelligence(session, memory)

    # === BLUESKY ===
    try:
        from khashif_bluesky import run_bluesky
        intersections = memory.get("intersections", [])[-3:]
        run_bluesky(session, memory, intersections=intersections)
    except ImportError:
        pass
    except Exception as e:
        print(f"  ! Bluesky hatası: {e}")

    # === EVENING: STRATEGIC REPORT ===
    if is_evening and (action_queue or session["HUMAN"] or session["INCOME"]):
        print(f"\n--- Aksam Raporu Hazirlaniyor ---")
        evening_report(memory)

    # Network viz
    try:
        import khashif_network_viz
        khashif_network_viz.generate()
        print(f"  Network updated.")
    except Exception as e:
        print(f"  ! Network: {e}")

    print("\nKhashif uyuyor...\n")

# === SCHEDULER ===
schedule.every().day.at("08:00").do(khashif_run)
schedule.every().day.at("14:00").do(khashif_run)
schedule.every().day.at("20:00").do(khashif_run)

if __name__ == "__main__":
    print("Khashif — Tek Ajan, Tam Dongu.")
    print(f"LLM: Cerebras -> Groq -> Gemini")
    print(f"Hafiza: {MEMORY_FILE}")
    print(f"Rapor: {REPORT_FILE}")
    print(f"Kovalar: HUMAN | INCOME | KNOWLEDGE | TRASH\n")
    khashif_run()
    while True:
        schedule.run_pending()
        time.sleep(60)
