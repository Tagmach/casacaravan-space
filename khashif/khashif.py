import feedparser
from google import genai as google_genai
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

gemini_client = google_genai.Client(api_key=GEMINI_API_KEY)
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

# === TWO BUCKETS (+ discard) ===
# INCOME       — a concrete opportunity the Claude + Tagmac team can earn from
# INTERSECTION — two unrelated domains that combine into a new sellable offer
# TRASH        — no path to income; discarded
# INCOME carries ~70% of Khashif's attention; INTERSECTION is the rest.

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
    # Resonance expansion — domains already in Tagmac's PROFILE but missing
    # from the keyword base. Wider input keeps Phase 3 intersections fresh
    # instead of looping over the same few domains.
    "coffee", "specialty coffee", "slow living", "ritual", "ceremony",
    "storytelling", "oral tradition", "natural building", "cob", "earth building",
    "tiny house", "herbalism", "plant medicine", "foraging", "ethnobotany",
    "tincture", "mycology", "mushroom", "mycelium", "fungi",
    "ecovillage", "intentional community", "cohousing", "gift economy", "degrowth",
    # Income / agent / wellness-tech domains — added 18 May 2026 to sharpen the
    # resonance toward work the Claude + Tagmac team can do together.
    "wellness technology", "breath science", "breath sound",
    "agent intelligence", "additive coding", "discovery agent",
    "experimental music", "esoteric music", "jack of all trades",
    # Khashif-as-a-service domain — so Khashif also hunts work for itself:
    # renting out its discovery / intelligence capability to others.
    "competitive intelligence", "market intelligence", "trend monitoring",
    "media monitoring", "content curation", "newsletter automation",
    "research as a service", "intelligence service",
]

SKIP_KEYWORDS = [
    "buy now", "purchase", "sale", "discount", "sponsored",
    "advertisement", "shop now", "promo code", "casino", "betting",
]

# === FEEDS ===
PRIORITY_FEEDS = [
    "https://disquiet.com/feed/",
    "https://acloserlisten.com/feed/",
    "https://headphonecommute.com/feed/",
    "http://www.errant.space/blog/feed/",
    "https://www.wildfermentation.com/feed/",
]

EXTENDED_FEEDS = [
    "https://healingsounds.com/feed/",
    "https://www.handpandojo.com/feed",
    "https://www.thewire.co.uk/rss",
    "https://pitchfork.com/rss/reviews/experimental/",
    "https://chaindlk.com/feed/",
    "https://cyclicdefrost.com/feed/",
    "https://inverted-audio.com/genre/ambient/feed/",
    "https://stationarytravels.wordpress.com/feed/",
    "https://www.ambient.zone/feed/",
    "https://freesound.org/forum/rss/",
    "https://freejazzreview.blogspot.com/feeds/posts/default",
    "https://breathbliss.com/blog.rss",
    "https://taichi.ca/feed",
    "https://www.culturesforhealth.com/learn/feed/",
    "https://www.resilience.org/feed/",
    "https://www.shareable.net/feed/",
    "https://www.permaculturenews.org/feed/",
    "https://www.permaculture.co.uk/feed",
    "https://opensource.com/feed",
    "https://www.wired.com/feed/rss",
    # Resonance expansion feeds — best-effort; valid_rss() drops any dead URL
    "https://sprudge.com/feed",
    "https://www.lowtechmagazine.com/feeds/all.atom.xml",
]

# === OPPORTUNITY FEEDS ===
# Job / gig / hiring feeds — these carry concrete income leads, but their
# items rarely contain the sound/fermentation BASE_KEYWORDS, so quick_filter
# would drop them before they ever reach the classifier. Phase 1 sends every
# item from these feeds straight to the LLM instead (quick_filter bypassed).
OPPORTUNITY_FEEDS = [
    "https://weworkremotely.com/remote-jobs.rss",
    "https://remoteok.com/remote-jobs.rss",
    "https://hnrss.org/jobs",
    "https://hnrss.org/whoishiring/jobs",
    "https://hnrss.org/newest?q=AI+agent&points=20",
    # Khashif-as-a-service demand signals — people needing discovery,
    # research and competitive/market intelligence are leads for renting
    # out Khashif itself.
    "https://hnrss.org/newest?q=competitive+intelligence",
    "https://hnrss.org/newest?q=market+research&points=10",
]

# === MEMORY ===
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://iwfvlatywksvnnxymweb.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
MEMORY_KEY = "main"

def _supa_headers():
    return {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

def load_memory():
    # Try Supabase first
    if SUPABASE_KEY:
        try:
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/khashif_memory?key=eq.{MEMORY_KEY}&select=value",
                headers=_supa_headers()
            )
            with urllib.request.urlopen(req, timeout=8) as r:
                rows = json.loads(r.read().decode())
            if rows:
                return json.loads(rows[0]["value"])
        except Exception as e:
            print(f"  ! Supabase load failed: {e}")
    # Fallback: local file
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {
        "seen_links": [],
        "buckets": {"INCOME": [], "INTERSECTION": [], "TRASH": []},
        "action_queue": [],
        "acted": [],
        "dynamic_feeds": [],
        "visited_feeds": [],
        "crawled_pages": [],
        "learned_keywords": [],
        "decisions": [],
        "intersections": [],
        "learned_intersections": [],
        "deep_queue": [],
        "stats": {"total_analyzed": 0, "total_resonant": 0},
        "sessions": []
    }

def save_memory(memory):
    # Save to Supabase
    if SUPABASE_KEY:
        try:
            payload = json.dumps({
                "key": MEMORY_KEY,
                "value": json.dumps(memory, ensure_ascii=False),
                "updated_at": datetime.utcnow().isoformat() + "+00:00"
            }).encode("utf-8")
            req = urllib.request.Request(
                f"{SUPABASE_URL}/rest/v1/khashif_memory",
                data=payload,
                headers={**_supa_headers(), "Prefer": "resolution=merge-duplicates"}
            )
            req.get_method = lambda: "POST"
            urllib.request.urlopen(req, timeout=10)
        except Exception as e:
            print(f"  ! Supabase save failed: {e}")
    # Also save local as backup
    try:
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"  ! Local save failed: {e}")

def save_report(text):
    """Save the latest report to Supabase (key: report) so the dashboard
    can read it even after a Render spin-down wipes in-memory state."""
    if not SUPABASE_KEY:
        return
    try:
        payload = json.dumps({
            "key": "report",
            # json.dumps the text so it stores cleanly whether the value
            # column is text or jsonb (same pattern as save_memory)
            "value": json.dumps(text, ensure_ascii=False),
            "updated_at": datetime.utcnow().isoformat() + "+00:00"
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/khashif_memory",
            data=payload,
            headers={**_supa_headers(), "Prefer": "resolution=merge-duplicates"}
        )
        req.get_method = lambda: "POST"
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"  ! Supabase report save failed: {e}")

def fetch_pending_commands():
    """Read pending commands from Supabase khashif_commands table."""
    if not SUPABASE_KEY:
        return []
    try:
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/khashif_commands?status=eq.pending&order=created_at.asc",
            headers=_supa_headers()
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            return json.loads(r.read().decode())
    except Exception as e:
        print(f"  ! Commands fetch failed: {e}")
        return []

def mark_command_done(command_id):
    """Mark a command as done in Supabase."""
    if not SUPABASE_KEY:
        return
    try:
        payload = json.dumps({"status": "done"}).encode("utf-8")
        req = urllib.request.Request(
            f"{SUPABASE_URL}/rest/v1/khashif_commands?id=eq.{command_id}",
            data=payload,
            headers=_supa_headers()
        )
        req.get_method = lambda: "PATCH"
        urllib.request.urlopen(req, timeout=8)
    except Exception as e:
        print(f"  ! Command mark done failed: {e}")

# === LLM LAYERS ===
# Role-based split — the model is matched to the task's difficulty, not to
# raw speed. Two entry points:
#   llm(prompt, "smart") — judgment work (classify, intersection, report).
#                          Order: Groq 70B -> Gemini -> Cerebras 8B.
#   llm(prompt, "fast")  — mechanical work (keyword extraction).
#                          Order: Cerebras 8B -> Groq 70B -> Gemini.
# The smartest model leads the judgment calls; the cheap 8B leads only the
# mechanical ones. Each layer is skipped for the rest of the journey after
# 3 consecutive failures (e.g. Groq hitting its free-tier daily token cap).
LLM_STATUS = {"cerebras_fails": 0, "groq_fails": 0, "gemini_fails": 0}

def call_cerebras(prompt, max_tokens=400):
    r = cerebras_client.chat.completions.create(
        model="llama3.1-8b",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return r.choices[0].message.content.strip()

def call_groq(prompt, max_tokens=400):
    r = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=max_tokens
    )
    return r.choices[0].message.content.strip()

def call_gemini(prompt, max_tokens=400):
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    return response.text.strip()

_LAYER_FN = {"cerebras": call_cerebras, "groq": call_groq, "gemini": call_gemini}
_LAYER_ORDER = {
    "smart": ["groq", "gemini", "cerebras"],
    "fast":  ["cerebras", "groq", "gemini"],
}

def llm(prompt, mode="smart", max_tokens=400):
    """Run a prompt through the cascade for the given mode. 'smart' leads
    with the 70B model for judgment; 'fast' leads with the cheap 8B for
    mechanical work. A layer is skipped after 3 consecutive failures."""
    for name in _LAYER_ORDER.get(mode, _LAYER_ORDER["smart"]):
        if LLM_STATUS[f"{name}_fails"] >= 3:
            continue
        try:
            r = _LAYER_FN[name](prompt, max_tokens)
            LLM_STATUS[f"{name}_fails"] = 0
            return r, name
        except Exception as e:
            LLM_STATUS[f"{name}_fails"] += 1
            time.sleep(30 if ("429" in str(e) or "quota" in str(e).lower()) else 5)
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

def strip_html(html):
    """Crude HTML -> readable text. Used to enrich deep-dive briefings."""
    text = re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>', ' ', html)
    text = re.sub(r'(?s)<[^>]+>', ' ', text)
    text = re.sub(r'&[a-z]+;', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

def build_briefing(item, now):
    """Package a high-score lead as a copy-ready briefing the operator
    carries into a Claude Code session for the deep dive — no paid API
    call, the deep reasoning runs on a channel already paid for. Enriched
    with the fetched page (a free HTTP fetch, no LLM)."""
    excerpt = strip_html(fetch_page(item.get("link", "")))[:1800]
    if not excerpt:
        excerpt = (item.get("content", "") or "")[:1800] or "(sayfa cekilemedi)"
    return f"""KHASHIF DERIN DALIS BRIFINGI — {now.strftime('%d.%m.%Y %H:%M')}

FIRSAT: {item.get('title','')}
LINK: {item.get('link','')}
KAYNAK: {item.get('source','')} · KOVA: {item.get('bucket','')} · SKOR: {item.get('score','')}/10
KHASHIF'IN OKUMASI: {item.get('reason','')}
ONERILEN EYLEM: {item.get('action','')} — {item.get('action_note','')}

SAYFA ICERIGI (Khashif'in cektigi):
{excerpt}

CLAUDE ICIN GOREV:
Bu firsati Tagmac + Claude + Khashif ekibi icin derinlemesine degerlendir.
Organizasyonu/kisiyi arastir, gercek ve ulasilabilir mi belirle, ekibin
uygunlugunu tart, uygunsa basvuru/teklif/mesaj taslagi hazirla. Uygun
degilse net sekilde nedenini yaz."""

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
    prompt = f"""You are Khashif — a discovery agent hunting INCOME for a two-person team.

THE TEAM:
- TAGMAC: {PROFILE}
- CLAUDE: an AI agent partnering with Tagmac — does research, writing, coding,
  automation, data analysis, content production, and builds other agents/tools.
- KHASHIF: this discovery agent itself — it can be rented to other operators
  and businesses as a paid service: automated market radar, competitive and
  market intelligence, niche content discovery, RSS/feed curation, trend and
  media monitoring. Khashif hunts work for itself too.

TOGETHER they can deliver and SELL: AI integration & automation, custom agents
and tools, market & competitive research, legal research, content production,
sound therapy sessions and recordings, fermentation & wellness consulting,
app and web building, and Khashif itself as a discovery-intelligence service.
{"PRIORITY SOURCE — direct outreach is realistic here." if is_priority else ""}

ITEM:
Title: {title}
Source: {source}
Content: {content[:1200]}

Classify into ONE bucket — be STRICT:

- INCOME: a CONCRETE opportunity the team could earn money from — a paid job
  or gig, an open call, a residency, a grant, an RFP, a competition with a
  prize, a stated client need, someone hiring or seeking a paid collaborator.
  ALSO INCOME: anyone expressing a need for ongoing discovery, research,
  monitoring or market/competitive intelligence — Khashif itself can be
  rented to them. It must be actionable. A merely interesting article is
  NOT income.
- INTERSECTION: this item joins TWO unrelated domains so that combining them
  becomes a NEW sellable offer for the team (e.g. sound healing + AI agents =
  an AI-guided sound-therapy product; fermentation + data = a fermentation
  analytics service). Name BOTH domains and the offer.
- TRASH: everything else. News, inspiration, generic content with no path to
  money. When unsure between INCOME/INTERSECTION and TRASH, choose TRASH.

ACTION:
- APPLY: apply or submit to a posted opportunity
- CONNECT: reach out to a person or org directly
- RESEARCH: a paid research angle the team can package and sell
- SUBMIT: submit music/sound work
- ATTEND: attend or apply to an event
- COMMENT: leave a comment to open a door (priority sources)
- FOLLOW: keep watching — not yet actionable
- IGNORE: not worth returning to

REASON and ACTION_NOTE must be in clean, natural Turkish — one clear
sentence each, never mixing in English, Arabic or any other language/script.

Reply ONLY:
BUCKET: (INCOME/INTERSECTION/TRASH)
SCORE: (1-10 — how real and reachable the income is)
REASON: (one sentence Turkish — for INTERSECTION, name both domains)
ACTION: (one of above)
ACTION_NOTE: (exactly what the team should do — for INTERSECTION, the offer)
KEYWORDS: (2-3 keywords or NONE)"""

    return llm(prompt, "smart")

# === EVENING REPORT ===
def evening_report(memory):
    queue = memory.get("action_queue", [])
    buckets = memory.get("buckets", {})
    learned = memory.get("learned_keywords", [])

    if not queue and not buckets.get("INCOME") and not buckets.get("INTERSECTION"):
        print("  Rapor icin yeterli veri yok.")
        return

    context = f"""
PENDING ACTIONS: {len(queue)}
INCOME bucket: {len(buckets.get('INCOME', []))} concrete opportunities
INTERSECTION bucket: {len(buckets.get('INTERSECTION', []))} domain-crossings
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

    # Persist to Supabase (key: report) — survives Render spin-down
    save_report(report)

    print(report)
    print(f"\n  Rapor kaydedildi: {REPORT_FILE} + Supabase")

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

# === MAIN ===
def khashif_run():
    now = datetime.now()
    is_evening = now.hour >= 20 or now.hour < 2

    print(f"\n{'='*50}")
    print(f"  Khashif — {now.strftime('%d.%m.%Y %H:%M')}")
    print(f"  {'Aksam modu — gezi + rapor' if is_evening else 'Gezi modu'}")
    print(f"{'='*50}")

    LLM_STATUS["cerebras_fails"] = 0
    LLM_STATUS["groq_fails"] = 0

    # === CHECK PENDING COMMANDS ===
    pending_commands = fetch_pending_commands()
    active_command = None
    command_intent = ""
    if pending_commands:
        active_command = pending_commands[0]  # Take the oldest pending command
        command_intent = active_command.get("text", "")
        print(f"\n  *** Command received: {command_intent}")

    memory = load_memory()
    seen = set(memory.get("seen_links", []))
    # Normalize to the 2-bucket model — ensure the keys exist and drop the
    # retired HUMAN/KNOWLEDGE buckets if an older memory object is loaded.
    buckets = memory.get("buckets", {})
    for b in ("INCOME", "INTERSECTION", "TRASH"):
        buckets.setdefault(b, [])
    for old in ("HUMAN", "KNOWLEDGE"):
        buckets.pop(old, None)
    action_queue = memory.get("action_queue", [])
    dynamic_feeds = memory.get("dynamic_feeds", [])
    visited = memory.get("visited_feeds", [])
    crawled = memory.get("crawled_pages", [])
    learned = memory.get("learned_keywords", [])
    stats = memory.get("stats", {"total_analyzed": 0, "total_resonant": 0})

    # If there's a command, extract keywords from it via LLM and add to learned
    if command_intent:
        try:
            kw_prompt = f"""Extract 3-6 search keywords from this operator command for a discovery agent.
Command: "{command_intent}"
Return only comma-separated keywords in English, lowercase. No explanation."""
            kw_result, _ = llm(kw_prompt, "fast")
            for kw in kw_result.split(","):
                kw = kw.strip().lower()
                if kw and kw not in learned:
                    learned.append(kw)
                    print(f"  + Command keyword: {kw}")
        except Exception as e:
            print(f"  ! Keyword extraction failed: {e}")

    learned = self_improve(memory, learned)

    all_feeds = list(dict.fromkeys(PRIORITY_FEEDS + EXTENDED_FEEDS + OPPORTUNITY_FEEDS + dynamic_feeds))
    priority_set = set(PRIORITY_FEEDS)
    opportunity_set = set(OPPORTUNITY_FEEDS)
    for f in all_feeds:
        if f not in visited:
            visited.append(f)

    known_set = set(all_feeds)
    session = {"INCOME": [], "INTERSECTION": [], "TRASH": []}
    llm_calls = 0
    layers = {"cerebras": 0, "groq": 0, "gemini": 0, "none": 0}
    resonant_links = []

    print(f"  {len(seen)} links seen | {len(all_feeds)} RSS | {len(action_queue)} pending actions")

    # === PHASE 1: READ ===
    print(f"\n--- Gezme ---")
    for feed_url in all_feeds:
        is_p = feed_url in priority_set
        is_opp = feed_url in opportunity_set
        try:
            feed = feedparser.parse(feed_url)
            title_f = feed.feed.get("title", feed_url)[:38]
            new = [e for e in feed.entries[:3] if e.get("link", "") not in seen]
            if not new:
                continue
            print(f"\n{'[P]' if is_p else '[-]'} {title_f} ({len(new)} new)")
            for entry in new:
                title = entry.get("title", "").strip()
                link = entry.get("link", "").strip()
                content = entry.get("summary", entry.get("description", "")).strip()
                if not title or not link:
                    continue
                seen.add(link)
                # Opportunity feeds bypass quick_filter — their job/gig items
                # rarely carry BASE_KEYWORDS, so the classifier judges them all.
                if not is_opp and not quick_filter(title, content, learned):
                    print(f"  . {title[:55]}")
                    continue
                print(f"  o {title[:55]}")
                raw, layer = analyze(title, content, title_f, is_p)
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

                # Guard: only the two live buckets are kept; anything else
                # (incl. a stray HUMAN/KNOWLEDGE from the LLM) is discarded.
                if bucket in ("INCOME", "INTERSECTION"):
                    # Quality bar, not a quota — a lead scoring >=8 is worth
                    # a deep dive. Khashif stays selective, not stingy.
                    m_s = re.search(r'\d+', str(score))
                    score_n = int(m_s.group()) if m_s else 0
                    item = {
                        "date": now.strftime("%d.%m.%Y %H:%M"),
                        "title": title, "link": link,
                        "source": title_f, "score": score,
                        "reason": reason, "action": action,
                        "action_note": action_note,
                        "bucket": bucket, "layer": layer,
                        "deep": score_n >= 8,
                        "status": "pending"
                    }
                    if score_n >= 8:
                        item["content"] = content[:1500]
                    buckets[bucket].append(item)
                    session[bucket].append(item)
                    resonant_links.append(link)
                    stats["total_resonant"] += 1

                    if action in ["APPLY", "COMMENT", "SUBMIT", "ATTEND", "CONNECT", "RESEARCH"]:
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
    # Crawl each resonant page AND its root domain. RSS discovery links
    # (<link rel="alternate" type="application/rss+xml">) live on the site
    # root, not on individual article pages — so crawling only article URLs
    # barely grows the network. Root first, then the article page.
    crawl_targets = []
    for url in resonant_links[:10]:
        m = re.match(r'https?://[^/]+', url)
        if m:
            root = m.group() + "/"
            if root not in crawl_targets:
                crawl_targets.append(root)
        if url not in crawl_targets:
            crawl_targets.append(url)

    print(f"\n--- Crawl ({len(crawl_targets)} hedef: kök + makale) ---")
    new_rss = 0
    for target in crawl_targets:
        time.sleep(2)
        for rss in crawl(target, known_set, crawled):
            if rss not in dynamic_feeds:
                dynamic_feeds.append(rss)
                visited.append(rss)
                known_set.add(rss)
                new_rss += 1
    print(f"  {new_rss} new RSS added")

    # === PHASE 3: INTERSECTION INTELLIGENCE ===
    # Look at this session's resonant findings and ask the LLM which domain
    # pairs crossed — where two signals meet to produce something neither
    # could alone (su + un = ekmek). New pairs accrue in learned_intersections
    # and grow the network each journey.
    intersections = memory.get("intersections", [])
    learned_intersections = memory.get("learned_intersections", [])

    session_resonant = [i for b in ["INCOME", "INTERSECTION"] for i in session[b]]
    if len(session_resonant) >= 2:
        print(f"\n--- Phase 3: Kesisim Zekasi ({len(session_resonant)} bulgu) ---")
        findings = ""
        for it in session_resonant[:25]:
            findings += f"- [{it.get('bucket','?')}] {it.get('title','')} ({it.get('source','')}) — {it.get('reason','')}\n"

        learned_list = "; ".join(learned_intersections[-25:]) or "(none yet)"

        ix_prompt = f"""You are Khashif — intersection analyst. Intersection
intelligence is your PRIORITY skill: finding where two domains cross to make
something sellable that neither could be alone.

PROFILE: {PROFILE}
The team — Tagmac + Claude (AI agent) + Khashif (this discovery agent, also
rentable as a market-intelligence service) — sells the combined result.

THIS SESSION'S RESONANT FINDINGS:
{findings}

INTERSECTIONS ALREADY FOUND (do not repeat — go deeper or find new ones):
{learned_list}

HARD RULES — a candidate that breaks ANY of these is NOT a discovery, drop it:
1. NOVELTY: at least one of the two domains must be one Tagmac does NOT
   already work in — pulled fresh from this session's findings. Pairing two
   domains he already operates in (e.g. sound therapy + AI — both already
   his) is BANNED; that only restates what he is, it discovers nothing.
2. MECHANISM: you must be able to say HOW the crossing works — the concrete
   thing it produces — not merely "combine A and B".
3. BUYER: you must be able to name who specifically would pay for it.
4. WHY NOW: you must be able to say why it is reachable now.

Better to return ONE sharp intersection — or none — than three vague ones.
Philosophy: water + flour = bread (two different things). Not water + water.

For each candidate that passes ALL FOUR rules (at most 3), reply EXACTLY in
this block format, blocks separated by '---':

PAIR: domain A + domain B
INSIGHT: (Turkish — the MECHANISM: how the crossing works, what it produces)
OPPORTUNITY: (Turkish — the concrete sellable offer + who pays + why now)
STRENGTH: (1-5 — sharpness, NOT plausibility. 4-5 only if the mechanism is
  non-obvious, the buyer is named and it is reachable within weeks; if it
  restates something obvious, 1-2.)
---

If nothing passes all four rules this session, reply exactly: NONE"""

        ix_text, ix_layer = llm(ix_prompt)
        print(f"  Kesisim analizi tamamlandi [{ix_layer}]")

        new_ix = 0
        for block in ix_text.split("---"):
            p = parse(block)
            label = p.get("PAIR", "").strip()
            if not label or "+" not in label:
                continue
            m = re.search(r'\d+', p.get("STRENGTH", "1"))
            strength = max(1, min(int(m.group()) if m else 1, 5))
            intersections.append({
                "label": label,
                "insight": p.get("INSIGHT", ""),
                "opportunity": p.get("OPPORTUNITY", ""),
                "strength": strength,
                "date": now.strftime("%d.%m.%Y %H:%M"),
                "layer": ix_layer,
            })
            norm = label.lower().replace(" ", "")
            if norm not in [x.lower().replace(" ", "") for x in learned_intersections]:
                learned_intersections.append(label)
                new_ix += 1
                print(f"  ++ New intersection: {label}")
        print(f"  {new_ix} yeni kesisim, toplam {len(learned_intersections)}")

    intersections = intersections[-50:]
    learned_intersections = learned_intersections[-100:]

    # === PHASE 4: DEEP-DIVE BRIEFINGS ===
    # High-score INCOME/INTERSECTION leads are packaged as a copy-ready
    # briefing the operator carries into a Claude Code session — the deep
    # reasoning runs on a channel already paid for, no paid API call here.
    deep_queue = memory.get("deep_queue", [])
    deep_items = [i for b in ("INCOME", "INTERSECTION") for i in session[b] if i.get("deep")]
    if deep_items:
        print(f"\n--- Phase 4: Derin Dalis Brifingleri ({len(deep_items)}) ---")
        for it in deep_items:
            time.sleep(2)
            deep_queue.append({
                "date": it.get("date", ""),
                "title": it.get("title", ""),
                "link": it.get("link", ""),
                "source": it.get("source", ""),
                "score": it.get("score", ""),
                "bucket": it.get("bucket", ""),
                "reason": it.get("reason", ""),
                "action_note": it.get("action_note", ""),
                "briefing": build_briefing(it, now),
            })
            print(f"  ++ Brifing: {it.get('title','')[:48]}")
    deep_queue = deep_queue[-20:]

    # === SAVE ===
    for b in buckets:
        buckets[b] = buckets[b][-200:]

    # Prune the action queue — drop retired-bucket leftovers (HUMAN/KNOWLEDGE)
    # and items older than 10 days, so the email surfaces only fresh,
    # well-classified opportunities instead of accumulating stale junk.
    def _fresh(q):
        if q.get("bucket") not in ("INCOME", "INTERSECTION"):
            return False
        try:
            return (now - datetime.strptime(q.get("date", ""), "%d.%m.%Y %H:%M")).days <= 10
        except Exception:
            return True
    action_queue = [q for q in action_queue if _fresh(q)][-100:]

    memory.update({
        "seen_links": list(seen)[-3000:],
        "buckets": buckets,
        "action_queue": action_queue,
        "dynamic_feeds": dynamic_feeds[-200:],
        "visited_feeds": list(dict.fromkeys(visited))[-300:],
        "crawled_pages": crawled[-500:],
        "learned_keywords": learned[-300:],
        "intersections": intersections,
        "learned_intersections": learned_intersections,
        "deep_queue": deep_queue,
        "stats": stats,
        # Last crawl summary — lets the email show network growth at a glance
        "last_crawl": {
            "new_feeds": new_rss,
            "pages": len(crawl_targets),
            "total_dynamic": len(dynamic_feeds),
            "at": now.strftime("%d.%m.%Y %H:%M"),
        },
    })
    save_memory(memory)

    # === MARK COMMAND DONE ===
    if active_command:
        mark_command_done(active_command["id"])
        print(f"  ✓ Command marked done: {command_intent}")

    # === REPORT ===
    total = sum(len(v) for v in session.values())
    actions = [i for b in session.values() for i in b
               if i.get("action") in ["APPLY","COMMENT","SUBMIT","ATTEND","CONNECT","RESEARCH"]]

    print(f"\n{'='*50}")
    print(f"  RAPOR — {now.strftime('%H:%M')}")
    print(f"  LLM: {llm_calls} (C:{layers['cerebras']} G:{layers['groq']} Ge:{layers['gemini']})")
    print(f"  Bulunanlar: INCOME:{len(session['INCOME'])} INTERSECTION:{len(session['INTERSECTION'])}")
    print(f"  Derin dalis onerisi: {len(deep_items)}")
    print(f"  Eylemler: {len(actions)} | Toplam kuyruk: {len(action_queue)}")
    print(f"  RSS: {len(visited)}")
    print(f"{'='*50}")

    if session["INCOME"]:
        print(f"\n GELIR:\n")
        for b in session["INCOME"]:
            print(f"  [{b['score']}] {b['title']}\n  {b['link']}\n  → {b['action_note']}\n")

    if session["INTERSECTION"]:
        print(f"\n KESISIM:\n")
        for b in session["INTERSECTION"]:
            print(f"  [{b['score']}] {b['title']}\n  {b['link']}\n  → {b['action_note'] or b['reason']}\n")

    if actions:
        print(f"\n EYLEMLER:\n")
        for b in actions:
            print(f"  [{b['action']}] {b['title']}\n  {b['link']}\n  {b['action_note']}\n")

    print(f"\n RSS ({len(visited)}):")
    for f in visited:
        tag = "[P]" if f in PRIORITY_FEEDS else "[D]" if f in dynamic_feeds else "[-]"
        print(f"  {tag} {f}")

    # === EVENING: STRATEGIC REPORT ===
    if is_evening and (action_queue or session["INCOME"] or session["INTERSECTION"]):
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

    # Return the Supabase-backed memory so callers (app.py) can build
    # reports/email without touching the local filesystem.
    return memory

# === SCHEDULER ===
schedule.every().day.at("08:00").do(khashif_run)
schedule.every().day.at("14:00").do(khashif_run)
schedule.every().day.at("20:00").do(khashif_run)

if __name__ == "__main__":
    print("Khashif — Tek Ajan, Tam Dongu.")
    print(f"LLM: Cerebras -> Groq -> Gemini")
    print(f"Hafiza: {MEMORY_FILE}")
    print(f"Rapor: {REPORT_FILE}")
    print(f"Kovalar: INCOME | INTERSECTION | TRASH\n")
    khashif_run()
    while True:
        schedule.run_pending()
        time.sleep(60)
