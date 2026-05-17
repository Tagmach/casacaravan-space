from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import os
import json
import urllib.request
from datetime import datetime

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["https://casacaravan.space", "http://localhost", "http://127.0.0.1"]}})

RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
OPERATOR_EMAIL = "tagmacc@gmail.com"

def send_email(subject, html):
    if not RESEND_API_KEY:
        return
    try:
        data = json.dumps({
            "from": "Khashif 𓆟 <shop@casacaravan.space>",
            "to": [OPERATOR_EMAIL],
            "subject": subject,
            "html": html
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://api.resend.com/emails",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {RESEND_API_KEY}"
            }
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"  ! Email failed: {e}")

# === DOMAIN LOCK ===
ALLOWED_ORIGINS = [
    "https://casacaravan.space",
    "http://localhost",
    "termux",  # Termux User-Agent kontrolü
]
KHASHIF_SECRET = os.environ.get("KHASHIF_SECRET", "")

def is_authorized(req):
    # Secret key kontrolü
    key = req.headers.get("X-Khashif-Key", "")
    if KHASHIF_SECRET and key == KHASHIF_SECRET:
        return True
    # User-Agent kontrolü (Termux curl)
    ua = req.headers.get("User-Agent", "")
    if "termux" in ua.lower() or "curl" in ua.lower():
        return True
    # Origin kontrolü
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
        # Render timeout için: priority feeds only, hızlı mod
        import os
        # Seed feeds ile başlar, memory'deki crawled feeds'den devam eder
        khashif.khashif_run()
        
        # Raporu oku
        report_file = os.path.join(os.path.dirname(__file__), "khashif_report.txt")
        if os.path.exists(report_file):
            with open(report_file, "r", encoding="utf-8") as f:
                khashif_state["last_report"] = f.read()
        
        # Hafızadan bekleyen soruları al
        memory_file = os.path.join(os.path.dirname(__file__), "khashif_memory.json")
        if os.path.exists(memory_file):
            with open(memory_file, "r", encoding="utf-8") as f:
                memory = json.load(f)
                queue = memory.get("action_queue", [])
                buckets = memory.get("buckets", {})
                high_priority = [
                    q for q in queue 
                    if q.get("action") in ["COMMENT", "CONNECT", "SUBMIT", "ATTEND"]
                    and q.get("status") == "pending"
                ][:5]
                khashif_state["pending_questions"] = high_priority

                # Raporu state'e al
                report_file = os.path.join(os.path.dirname(__file__), "khashif_report.txt")
                report_text = ""
                if os.path.exists(report_file):
                    with open(report_file, "r", encoding="utf-8") as rf:
                        report_text = rf.read()
                        khashif_state["last_report"] = report_text

                # Email — kova ozeti + sorular
                rows = ""
                for i, q in enumerate(high_priority, 1):
                    rows += f"<tr style='border-bottom:1px solid #f0e8e0;'><td style='padding:10px;font-size:13px;color:#1a1208;'>{i}. {q.get('title','')[:55]}</td><td style='padding:8px;font-size:11px;color:#a08060;font-weight:600;'>{q.get('action','')}</td><td style='padding:8px;font-size:11px;color:#7a7068;'>{q.get('action_note','')[:70]}</td><td style='padding:8px;'><a href=\"{q.get('link','')}\">→</a></td></tr>"

                q_section = f"<h3 style='font-size:16px;font-weight:300;font-style:italic;margin-bottom:16px;'>Sana soruyor</h3><table style='width:100%;border-collapse:collapse;margin-bottom:24px;'><tr style='background:#f5f0e8;'><th style='padding:8px;text-align:left;font-size:9px;color:#7a7068;'>Baslik</th><th style='padding:8px;text-align:left;font-size:9px;color:#7a7068;'>Aksiyon</th><th style='padding:8px;text-align:left;font-size:9px;color:#7a7068;'>Ne yapilacak</th><th></th></tr>{rows}</table>" if high_priority else "<p style='font-size:13px;color:#a09080;font-style:italic;'>Bu turda soru yok.</p>"

                html = f"""<div style='font-family:Georgia,serif;max-width:600px;margin:0 auto;padding:32px;color:#1a1208;'>
<h2 style='font-size:22px;font-weight:300;font-style:italic;'>Khashif gezdi. 𓆟</h2>
<p style='font-size:10px;letter-spacing:2px;text-transform:uppercase;color:#a09080;margin-bottom:24px;'>{datetime.now().strftime('%d.%m.%Y %H:%M')}</p>
<div style='display:flex;gap:12px;margin-bottom:24px;'>
<div style='background:#f5f0e8;padding:12px 16px;border-radius:6px;flex:1;text-align:center;'><div style='font-size:20px;font-style:italic;'>{len(buckets.get('HUMAN',[]))}</div><div style='font-size:9px;letter-spacing:1px;color:#a09080;text-transform:uppercase;'>HUMAN</div></div>
<div style='background:#f5f0e8;padding:12px 16px;border-radius:6px;flex:1;text-align:center;'><div style='font-size:20px;font-style:italic;'>{len(buckets.get('INCOME',[]))}</div><div style='font-size:9px;letter-spacing:1px;color:#a09080;text-transform:uppercase;'>INCOME</div></div>
<div style='background:#f5f0e8;padding:12px 16px;border-radius:6px;flex:1;text-align:center;'><div style='font-size:20px;font-style:italic;'>{len(buckets.get('KNOWLEDGE',[]))}</div><div style='font-size:9px;letter-spacing:1px;color:#a09080;text-transform:uppercase;'>KNOWLEDGE</div></div>
<div style='background:#f5f0e8;padding:12px 16px;border-radius:6px;flex:1;text-align:center;'><div style='font-size:20px;font-style:italic;'>{len(high_priority)}</div><div style='font-size:9px;letter-spacing:1px;color:#a09080;text-transform:uppercase;'>SORULAR</div></div>
</div>
{q_section}
<div style='background:#f5f0e8;padding:16px;border-radius:8px;margin-bottom:16px;'>
<div style='font-size:9px;letter-spacing:1px;text-transform:uppercase;color:#a09080;margin-bottom:8px;'>Karar icin CMD:</div>
<code style='font-size:10px;color:#1a1208;word-break:break-all;'>curl -X POST -H "X-Khashif-Key: khashif2026" -H "Content-Type: application/json" -d "{{\"link\":\"URL\",\"verdict\":\"YES\"}}" https://khashif.onrender.com/decide</code>
</div>
<p style='font-size:10px;color:#a09080;border-top:1px solid #e8e0d0;padding-top:16px;'>casacaravan.space · Khashif 𓆟</p>
</div>"""
                send_email(f"Khashif 𓆟 — {datetime.now().strftime('%d.%m %H:%M')} · {len(high_priority)} soru", html)

    except Exception as e:
        khashif_state["last_report"] = f"Hata: {str(e)}"
    
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
    """Son raporu getir"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403
    
    return jsonify({
        "running": khashif_state["running"],
        "last_run": khashif_state["last_run"],
        "report": khashif_state["last_report"][-3000:] if khashif_state["last_report"] else "Henüz rapor yok.",
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
def buckets():
    """Dört kovanın özeti"""
    if not is_authorized(request):
        return jsonify({"error": "unauthorized"}), 403
    
    memory_file = os.path.join(os.path.dirname(__file__), "khashif_memory.json")
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            memory = json.load(f)
        
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
    except:
        return jsonify({"error": "Hafıza dosyası bulunamadı"}), 404

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
