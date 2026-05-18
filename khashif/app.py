from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import os
import json
import urllib.request
import urllib.error
from datetime import datetime
from html import escape

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://casacaravan.space", "http://localhost", "http://127.0.0.1"]}})

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
OPERATOR_EMAIL = "tagmacc@gmail.com"

def send_email(subject, html):
    """Send an email via Resend. Returns True on success, False otherwise.
    Runs entirely server-side — no dependency on any local machine."""
    if not RESEND_API_KEY:
        print("  ! Email skipped: RESEND_API_KEY not set on the server")
        return False
    try:
        data = json.dumps({
            "from": "Khashif 𓆟 <khashif@casacaravan.space>",
            "to": [OPERATOR_EMAIL],
            "subject": subject,
            "html": html
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {RESEND_API_KEY}",
                # Cloudflare blocks the default Python-urllib User-Agent (error 1010)
                "User-Agent": "Mozilla/5.0",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            print(f"  Email sent → {OPERATOR_EMAIL} (HTTP {r.status})")
        return True
    except urllib.error.HTTPError as e:
        # Surface Resend's actual error body (unverified domain, bad key, ...)
        body = ""
        try:
            body = e.read().decode("utf-8", errors="ignore")
        except Exception:
            pass
        print(f"  ! Email failed: HTTP {e.code} — {body}")
        return False
    except Exception as e:
        print(f"  ! Email failed: {e}")
        return False

def fetch_report_text():
    """Fetch the latest report text from Supabase (key: report).
    No LLM cost — just reads what evening_report() last persisted
    (refreshed 2x/day). Returns "" on any failure."""
    SUPA_URL = os.environ.get("SUPABASE_URL", "https://iwfvlatywksvnnxymweb.supabase.co")
    SUPA_KEY = os.environ.get("SUPABASE_KEY", "")
    if not SUPA_KEY:
        return ""
    try:
        req = urllib.request.Request(
            f"{SUPA_URL}/rest/v1/khashif_memory?key=eq.report&select=value",
            headers={"apikey": SUPA_KEY, "Authorization": f"Bearer {SUPA_KEY}"}
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            rows = json.loads(r.read().decode())
        if rows:
            raw = rows[0].get("value", "")
            # value is json.dumps'd by save_report — decode it; tolerate
            # a legacy raw-text value too
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                return raw or ""
    except Exception as e:
        print(f"  ! fetch_report_text failed: {e}")
    return ""

# === DOMAIN LOCK ===
ALLOWED_ORIGINS = [
    "https://casacaravan.space",
    "http://localhost",
    "termux",  # Termux User-Agent kontrolü
]
KHASHIF_SECRET = os.environ.get("KHASHIF_SECRET", "")

def is_authorized(req):
    key = req.headers.get("X-Khashif-Key", "") or req.args.get("key", "")
    if key == "khashif2026":
        return True
    if KHASHIF_SECRET and key == KHASHIF_SECRET:
        return True
    ua = req.headers.get("User-Agent", "")
    if "termux" in ua.lower() or "curl" in ua.lower():
        return True
    origin = req.headers.get("Origin", req.headers.get("Referer", ""))
    if any(o in origin for o in ALLOWED_ORIGINS):
        return True
    return False

# === KHASHIF STATE ===
khashif_state = {
    "running": False,
    "last_run": None,
    "last_report": "",
    "pending_questions": [],
    "decisions": []
}

def run_khashif_task():
    """Khashif'i arka planda çalıştır"""
    if khashif_state["running"]:
        return {"status": "already_running"}
    
    khashif_state["running"] = True
    khashif_state["last_run"] = datetime.now().isoformat()
    
    try:
        import khashif

        # khashif_run() returns the Supabase-backed memory object.
        # The email is built straight from that return value — no local
        # files involved, so it works entirely on the cloud (Render).
        memory = khashif.khashif_run()
        if not isinstance(memory, dict):
            memory = {}

        bkts = memory.get("buckets", {})
        queue = memory.get("action_queue", [])
        high_priority = [
            q for q in queue
            if q.get("action") in ["COMMENT", "CONNECT", "SUBMIT", "ATTEND"]
            and q.get("status") == "pending"
        ][:5]
        khashif_state["pending_questions"] = high_priority

        # Report text — latest persisted report from Supabase (key: report).
        # No LLM cost; evening_report() refreshes it 2x/day. Best effort —
        # never blocks the email.
        report_text = fetch_report_text()
        if report_text:
            khashif_state["last_report"] = report_text

        # Email — kova ozeti + sorular
        rows = ""
        for i, q in enumerate(high_priority, 1):
            rows += f"<tr style='border-bottom:1px solid #f0e8e0;'><td style='padding:10px;font-size:13px;color:#1a1208;'>{i}. {q.get('title','')[:55]}</td><td style='padding:8px;font-size:11px;color:#a08060;font-weight:600;'>{q.get('action','')}</td><td style='padding:8px;font-size:11px;color:#7a7068;'>{q.get('action_note','')[:70]}</td><td style='padding:8px;'><a href=\"{q.get('link','')}\">→</a></td></tr>"

        q_section = f"<h3 style='font-size:16px;font-weight:300;font-style:italic;margin-bottom:16px;'>Sana soruyor</h3><table style='width:100%;border-collapse:collapse;margin-bottom:24px;'><tr style='background:#f5f0e8;'><th style='padding:8px;text-align:left;font-size:9px;color:#7a7068;'>Baslik</th><th style='padding:8px;text-align:left;font-size:9px;color:#7a7068;'>Aksiyon</th><th style='padding:8px;text-align:left;font-size:9px;color:#7a7068;'>Ne yapilacak</th><th></th></tr>{rows}</table>" if high_priority else "<p style='font-size:13px;color:#a09080;font-style:italic;'>Bu turda soru yok.</p>"

        # Report section — the full report text, embedded verbatim. Plain
        # text wrapped in <pre>; HTML-escaped so '=' separators etc. render.
        if report_text:
            report_section = (
                "<h3 style='font-size:16px;font-weight:300;font-style:italic;margin:24px 0 12px;'>Rapor</h3>"
                "<pre style='font-size:11px;line-height:1.5;background:#f5f0e8;padding:16px;border-radius:8px;"
                "white-space:pre-wrap;word-break:break-word;font-family:ui-monospace,Menlo,Consolas,monospace;"
                f"color:#1a1208;margin-bottom:24px;'>{escape(report_text.strip())}</pre>"
            )
        else:
            report_section = "<p style='font-size:13px;color:#a09080;font-style:italic;'>Henuz rapor yok.</p>"

        # Bucket contents — the actual items, not just counts. Newest 8 per
        # bucket, with score, title (linked), and note.
        def render_bucket(name, items):
            recent = items[-8:][::-1]
            if not recent:
                return ""
            li = ""
            for it in recent:
                title = escape(str(it.get("title", ""))[:90])
                link = escape(str(it.get("link", "")))
                score = escape(str(it.get("score", "")))
                note = escape(str(it.get("action_note") or it.get("reason") or "")[:120])
                li += (
                    "<div style='border-bottom:1px solid #f0e8e0;padding:8px 0;'>"
                    f"<div style='font-size:12px;color:#1a1208;'>[{score}] "
                    f"<a href=\"{link}\" style='color:#1a1208;'>{title}</a></div>"
                    f"<div style='font-size:11px;color:#7a7068;'>{note}</div></div>"
                )
            return (
                f"<h4 style='font-size:13px;font-weight:600;letter-spacing:1px;"
                f"text-transform:uppercase;color:#a08060;margin:16px 0 4px;'>{name} ({len(items)})</h4>{li}"
            )

        buckets_html = (
            render_bucket("HUMAN", bkts.get("HUMAN", []))
            + render_bucket("INCOME", bkts.get("INCOME", []))
            + render_bucket("KNOWLEDGE", bkts.get("KNOWLEDGE", []))
        )
        buckets_section = (
            "<h3 style='font-size:16px;font-weight:300;font-style:italic;margin:24px 0 8px;'>Kovalar</h3>"
            + (buckets_html or "<p style='font-size:13px;color:#a09080;font-style:italic;'>Kova bos.</p>")
        )

        # Network section — crawler growth at a glance
        lc = memory.get("last_crawl", {})
        net_section = (
            "<div style='background:#f5f0e8;padding:12px 16px;border-radius:8px;margin:0 0 24px;'>"
            "<div style='font-size:9px;letter-spacing:1px;text-transform:uppercase;color:#a09080;margin-bottom:6px;'>Ag durumu</div>"
            f"<div style='font-size:13px;color:#1a1208;'>Bu gezide <b>{lc.get('new_feeds', 0)}</b> yeni RSS &middot; "
            f"toplam <b>{lc.get('total_dynamic', len(memory.get('dynamic_feeds', [])))}</b> kesfedilen feed &middot; "
            f"<b>{lc.get('pages', 0)}</b> sayfa tarandi</div></div>"
        )

        html = f"""<div style='font-family:Georgia,serif;max-width:600px;margin:0 auto;padding:32px;color:#1a1208;'>
<h2 style='font-size:22px;font-weight:300;font-style:italic;'>Khashif gezdi. 𓆟</h2>
<p style='font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#a09080;margin-bottom:24px;'>{datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
<div style='display:flex;gap:12px;margin-bottom:24px;'>
<div style='background:#f5f0e8;padding:12px 16px;border-radius:6px;flex:1;text-align:center;'><div style='font-size:20px;font-style:italic;'>{len(bkts.get('HUMAN',[]))}</div><div style='font-size:9px;letter-spacing:1px;color:#a09080;text-transform:uppercase;'>HUMAN</div></div>
<div style='background:#f5f0e8;padding:12px 16px;border-radius:6px;flex:1;text-align:center;'><div style='font-size:20px;font-style:italic;'>{len(bkts.get('INCOME',[]))}</div><div style='font-size:9px;letter-spacing:1px;color:#a09080;text-transform:uppercase;'>INCOME</div></div>
<div style='background:#f5f0e8;padding:12px 16px;border-radius:6px;flex:1;text-align:center;'><div style='font-size:20px;font-style:italic;'>{len(bkts.get('KNOWLEDGE',[]))}</div><div style='font-size:9px;letter-spacing:1px;color:#a09080;text-transform:uppercase;'>KNOWLEDGE</div></div>
<div style='background:#f5f0e8;padding:12px 16px;border-radius:6px;flex:1;text-align:center;'><div style='font-size:20px;font-style:italic;'>{len(high_priority)}</div><div style='font-size:9px;letter-spacing:1px;color:#a09080;text-transform:uppercase;'>SORULAR</div></div>
</div>
{net_section}
{buckets_section}
{q_section}
{report_section}
<div style='background:#f5f0e8;padding:16px;border-radius:8px;margin-bottom:16px;'>
<div style='font-size:9px;letter-spacing:1px;text-transform:uppercase;color:#a09080;margin-bottom:8px;'>Karar icin CMD:</div>
<code style='font-size:10px;color:#1a1208;word-break:break-all;'>curl -X POST -H "X-Khashif-Key: khashif2026" -H "Content-Type: application/json" -d "{{\"link\":\"URL\",\"verdict\":\"YES\"}}" https://khashif.onrender.com/decide</code>
</div>
<p style='font-size:10px;color:#a09080;border-top:1px solid #e8e0d0;padding-top:16px;'>casacaravan.space · Khashif 𓆟</p>
</div>"""
        send_email(f"Khashif 𓆟 — {datetime.now().strftime('%d.%m %H:%M')} · {len(high_priority)} soru", html)

    except Exception as e:
        import traceback
        err = traceback.format_exc()
        khashif_state["last_report"] = f"HATA: {str(e)}\n\n{err}"
        print(f"Khashif error: {str(e)}")
        print(err)
        # Even on failure the operator must hear from Khashif — send an error email
        send_email(
            f"Khashif 𓆟 — HATA {datetime.now().strftime('%d.%m %H:%M')}",
            f"<div style='font-family:Georgia,serif;max-width:600px;margin:0 auto;padding:32px;color:#1a1208;'>"
            f"<h2 style='font-size:20px;font-weight:300;font-style:italic;'>Khashif bir hata ile karşılaştı.</h2>"
            f"<pre style='font-size:11px;background:#f5f0e8;padding:16px;border-radius:6px;white-space:pre-wrap;'>{str(e)}</pre></div>"
        )

    finally:
        khashif_state["running"] = False
    
    return {"status": "done"}

# === ENDPOINTS ===

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "agent": "Khashif 𓆟",
        "status": "awake",
        "base": "casacaravan.space",
        "protocol": "strike_and_wave_v1"
    })

@app.route("/task", methods=["POST"])
def task():
    """Khashif'i tetikle"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403
    
    if khashif_state["running"]:
        return jsonify({"status": "already_running", "started": khashif_state["last_run"]})
    
    # Arka planda çalıştır
    thread = threading.Thread(target=run_khashif_task)
    thread.daemon = True
    thread.start()
    
    return jsonify({
        "status": "started",
        "time": datetime.now().isoformat(),
        "message": "Khashif gezmeye çıktı."
    })

@app.route("/report", methods=["GET"])
def report():
    """Son raporu getir — Supabase'ten okur (key: report), Render spin-down'a
    dayanıklı. In-memory state'e fallback yapar."""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403

    report_text = fetch_report_text()

    # Fallback: in-memory state (fresh output before first Supabase save)
    if not report_text:
        report_text = khashif_state["last_report"]

    return jsonify({
        "running": khashif_state["running"],
        "last_run": khashif_state["last_run"],
        "report": report_text[-3000:] if report_text else "Henüz rapor yok.",
        "pending_questions": len(khashif_state["pending_questions"])
    })

@app.route("/questions", methods=["GET"])
def questions():
    """Khashif'in sana sorduğu sorular"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403
    
    return jsonify({
        "questions": khashif_state["pending_questions"],
        "count": len(khashif_state["pending_questions"]),
        "instructions": "Her soru için /decide endpoint'ine YES veya NO gönder"
    })

@app.route("/decide", methods=["POST"])
def decide():
    """Tağmaç'ın kararını kaydet"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403
    
    data = request.json
    link = data.get("link", "")
    verdict = data.get("verdict", "").upper()  # YES veya NO
    note = data.get("note", "")
    
    if not link or verdict not in ["YES", "NO"]:
        return jsonify({"error": "link ve verdict (YES/NO) gerekli"}), 400
    
    # Hafızaya yaz
    memory_file = os.path.join(os.path.dirname(__file__), "khashif_memory.json")
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            memory = json.load(f)
        
        # Queue'da bul ve güncelle
        for item in memory.get("action_queue", []):
            if item.get("link") == link:
                item["status"] = "approved" if verdict == "YES" else "rejected"
                item["operator_note"] = note
                item["decided_at"] = datetime.now().isoformat()
        
        # Karar geçmişine ekle
        memory.setdefault("decisions", []).append({
            "link": link,
            "verdict": verdict,
            "note": note,
            "date": datetime.now().isoformat()
        })
        
        with open(memory_file, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        
        # State'i güncelle
        khashif_state["pending_questions"] = [
            q for q in khashif_state["pending_questions"] 
            if q.get("link") != link
        ]
        khashif_state["decisions"].append({"link": link, "verdict": verdict})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    return jsonify({
        "status": "kaydedildi",
        "link": link,
        "verdict": verdict,
        "remaining_questions": len(khashif_state["pending_questions"])
    })

@app.route("/buckets", methods=["GET"])
def get_buckets():
    """Dört kovanın özeti"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403

    SUPA_URL = os.environ.get("SUPABASE_URL", "https://iwfvlatywksvnnxymweb.supabase.co")
    SUPA_KEY = os.environ.get("SUPABASE_KEY", "")

    try:
        req = urllib.request.Request(
            f"{SUPA_URL}/rest/v1/khashif_memory?key=eq.main&select=value",
            headers={
                "apikey": SUPA_KEY,
                "Authorization": f"Bearer {SUPA_KEY}"
            }
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            rows = json.loads(r.read().decode())
        if not rows:
            return jsonify({"error": "memory not found"}), 404
        memory = json.loads(rows[0]["value"])
        b = memory.get("buckets", {})
        return jsonify({
            "HUMAN": b.get("HUMAN", [])[-10:],
            "INCOME": b.get("INCOME", [])[-10:],
            "KNOWLEDGE": b.get("KNOWLEDGE", [])[-10:],
            "TRASH_count": len(b.get("TRASH", [])),
            "action_queue": memory.get("action_queue", [])[-10:],
            "learned_keywords": len(memory.get("learned_keywords", [])),
            "dynamic_feeds": len(memory.get("dynamic_feeds", [])),
            "stats": memory.get("stats", {})
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/status", methods=["GET"])
def status():
    """Khashif'in durumu"""
    return jsonify({
        "running": khashif_state["running"],
        "last_run": khashif_state["last_run"],
        "pending_questions": len(khashif_state["pending_questions"]),
        "decisions_today": len(khashif_state["decisions"])
    })


@app.route("/command", methods=["POST"])
def command():
    """Serbest komut al — Supabase khashif_commands tablosuna yaz"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403

    data = request.json
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "text gerekli"}), 400

    SUPA_URL = os.environ.get("SUPABASE_URL", "https://iwfvlatywksvnnxymweb.supabase.co")
    SUPA_KEY = os.environ.get("SUPABASE_KEY", "")

    try:
        # Supabase'e yaz
        if SUPA_KEY:
            payload = json.dumps({"text": text, "status": "pending"}).encode("utf-8")
            req = urllib.request.Request(
                f"{SUPA_URL}/rest/v1/khashif_commands",
                data=payload,
                headers={
                    "apikey": SUPA_KEY,
                    "Authorization": f"Bearer {SUPA_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=minimal"
                }
            )
            urllib.request.urlopen(req, timeout=10)

        # Khashif'i tetikle
        triggered = False
        if not khashif_state["running"]:
            thread = threading.Thread(target=run_khashif_task)
            thread.daemon = True
            thread.start()
            triggered = True

        return jsonify({
            "status": "queued",
            "command": text,
            "khashif_triggered": triggered
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/execute", methods=["POST"])
def execute():
    """YES sonrası gerçek aksiyon tetikle"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403

    data = request.json
    action = data.get("action", "").upper()
    link = data.get("link", "")
    title = data.get("title", "")
    note = data.get("note", "")

    if action == "RESEARCH":
        # LLM ile araştırma yap
        def do_research():
            try:
                import khashif as kh
                prompt = f"""You are Khashif — research agent for Tagmac Cankaya.

PROFILE: {kh.PROFILE}

RESEARCH REQUEST: {title}
{f"Additional context: {note}" if note else ""}
{f"Source: {link}" if link else ""}

Write a focused research report in Turkish. Include:
- Ana bulgular (3-5 madde)
- Tagmac için fırsat nedir?
- Önerilen aksiyon
- İlgili kaynaklar/linkler

Be specific and actionable."""
                result, layer = kh.llm(prompt)
                khashif_state["last_report"] = f"=== RESEARCH: {title} ===\n[{layer}]\n\n{result}\n\n" + khashif_state.get("last_report","")
                kh.save_report(khashif_state["last_report"])
            except Exception as e:
                khashif_state["last_report"] = f"Research error: {e}"

        thread = threading.Thread(target=do_research)
        thread.daemon = True
        thread.start()
        return jsonify({"status": "research_started", "title": title})

    elif action == "ATTEND":
        return jsonify({
            "status": "attend",
            "link": link,
            "instructions": f"Katılım linki: {link}. {note}"
        })

    elif action == "SUBMIT":
        # Gönderim taslağı oluştur
        def do_submit():
            try:
                import khashif as kh
                prompt = f"""Tagmac Cankaya için bu platforma müzik/iş gönderimi taslağı hazırla.

PLATFORM: {title}
LINK: {link}
NOT: {note}

TAGMAC PROFİLİ: {kh.PROFILE}

Türkçe olarak:
1. Gönderilecek eser/içerik önerisi (casacaravan.space müziklerinden)
2. Gönderim metni taslağı
3. Dikkat edilmesi gerekenler"""
                result, layer = kh.llm(prompt)
                khashif_state["last_report"] = f"=== SUBMIT TASLAK: {title} ===\n[{layer}]\n\n{result}\n\n" + khashif_state.get("last_report","")
                kh.save_report(khashif_state["last_report"])
            except Exception as e:
                khashif_state["last_report"] = f"Submit error: {e}"

        thread = threading.Thread(target=do_submit)
        thread.daemon = True
        thread.start()
        return jsonify({"status": "submit_draft_started", "title": title})

    return jsonify({"error": "unknown action"}), 400


@app.route("/agents", methods=["GET"])
def agents_list():
    """Khashif'in gezarken karşılaştığı diğer ajanlar"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403

    memory_file = os.path.join(os.path.dirname(__file__), "khashif_memory.json")
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            memory = json.load(f)
        return jsonify({
            "agents": memory.get("encountered_agents", []),
            "count": len(memory.get("encountered_agents", []))
        })
    except:
        return jsonify({"agents": [], "count": 0})


@app.route("/visitors", methods=["GET"])
def visitors():
    """Supabase page_visits - kim geldi, nereden"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403

    try:
        SUPA_URL = os.environ.get("SUPABASE_URL", "https://iwfvlatywksvnnxymweb.supabase.co")
        SUPA_KEY = os.environ.get("SUPABASE_KEY", "")

        if not SUPA_KEY:
            return jsonify({"visits": [], "count": 0, "note": "SUPABASE_KEY not set"})

        req = urllib.request.Request(
            f"{SUPA_URL}/rest/v1/page_visits?order=created_at.desc&limit=20",
            headers={
                "apikey": SUPA_KEY,
                "Authorization": f"Bearer {SUPA_KEY}"
            }
        )
        with urllib.request.urlopen(req, timeout=8) as r:
            data = json.loads(r.read().decode())
        return jsonify({"visits": data, "count": len(data)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/commands", methods=["GET"])
def commands_list():
    """Bekleyen operatör komutları"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403

    memory_file = os.path.join(os.path.dirname(__file__), "khashif_memory.json")
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            memory = json.load(f)
        cmds = memory.get("operator_commands", [])
        return jsonify({"commands": cmds[-10:], "count": len(cmds)})
    except:
        return jsonify({"commands": [], "count": 0})



@app.route("/analyze-music", methods=["POST"])
def analyze_music():
    """Ham akustik veriyi al, LLM ile analiz et"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403

    data = request.json
    tracks = data.get("tracks", [])
    if not tracks:
        return jsonify({"error": "No tracks provided"}), 400

    results = []
    for track in tracks:
        name = track.get("name", "Unknown")
        duration = track.get("duration", 0)
        dominant_freq = track.get("dominant_freq", 0)
        spectral_centroid = track.get("spectral_centroid", 0)
        rms_energy = track.get("rms_energy", 0)
        tempo_estimate = track.get("tempo_estimate", 0)
        freq_bands = track.get("freq_bands", {})
        
        # Frekans bandı yorumu
        low = freq_bands.get("low", 0)      # 0-200Hz
        mid = freq_bands.get("mid", 0)      # 200-2000Hz  
        high = freq_bands.get("high", 0)    # 2000Hz+
        
        prompt = f"""You are Khashif — music analyst and discovery agent for Tagmac Cankaya.

Analyze this track based on acoustic data:

Track: {name}
Duration: {duration:.1f} seconds
Dominant frequency: {dominant_freq:.1f} Hz
Spectral centroid (brightness): {spectral_centroid:.1f} Hz
RMS energy (dynamics): {rms_energy:.4f}
Tempo estimate: {tempo_estimate:.0f} BPM
Frequency bands:
  Low (0-200Hz): {low:.1%}
  Mid (200-2000Hz): {mid:.1%}  
  High (2000Hz+): {high:.1%}

TAGMAC CONTEXT:
- Gong maker and player, handpan, drone, breathwork, improvisation
- Sound healing, somatic practices, resonance
- Based in Lefkosa, Cyprus
- Creates: ambient, drone, sacred sound, experimental

Provide analysis in this exact format:
GENRE: (2-3 genres, comma separated)
MOD: (musical mode or quality: major/minor/modal/atonal/drone/rhythmic)
FLOW: (drone/ambient/meditative/rhythmic/melodic/textural/ceremonial)
DOMINANT_NOTE: (musical note if detectable, or "drone" or "noise")
ENERGY: (low/medium/high)
MOOD: (2-3 mood words in Turkish)
USE_CASE: (2-3 use cases: sound_healing/meditation/background/ceremony/movement/sleep)
DESCRIPTION_TR: (2-3 cümle Türkçe, sanatçı bakış açısıyla — ne taşıyor bu parça?)
DESCRIPTION_EN: (2-3 sentences English — what does this piece carry?)
RESONANCE: (1-5, how strongly this resonates with Tagmac's identity)"""

        try:
            import khashif as kh
            result, layer = kh.llm(prompt)
            
            # Parse result
            parsed = {}
            for line in result.strip().split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    parsed[k.strip()] = v.strip()
            
            results.append({
                "name": name,
                "duration": duration,
                "acoustic": {
                    "dominant_freq": dominant_freq,
                    "spectral_centroid": spectral_centroid,
                    "rms_energy": rms_energy,
                    "tempo_estimate": tempo_estimate,
                    "freq_bands": freq_bands
                },
                "analysis": {
                    "genre": parsed.get("GENRE", ""),
                    "mod": parsed.get("MOD", ""),
                    "flow": parsed.get("FLOW", ""),
                    "dominant_note": parsed.get("DOMINANT_NOTE", ""),
                    "energy": parsed.get("ENERGY", ""),
                    "mood": parsed.get("MOOD", ""),
                    "use_case": parsed.get("USE_CASE", ""),
                    "description_tr": parsed.get("DESCRIPTION_TR", ""),
                    "description_en": parsed.get("DESCRIPTION_EN", ""),
                    "resonance": parsed.get("RESONANCE", ""),
                },
                "layer": layer
            })
        except Exception as e:
            results.append({
                "name": name,
                "error": str(e)
            })

    return jsonify({"results": results, "count": len(results)})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)