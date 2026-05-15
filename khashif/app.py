from flask import Flask, request, jsonify
import threading
import os
import json
from datetime import datetime

app = Flask(__name__)

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
                # İlk 3 yüksek öncelikli aksiyonu soru olarak gönder
                high_priority = [
                    q for q in queue 
                    if q.get("action") in ["COMMENT", "CONNECT", "SUBMIT", "ATTEND"]
                    and q.get("status") == "pending"
                ][:3]
                khashif_state["pending_questions"] = high_priority
    
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
            "HUMAN": len(b.get("HUMAN", [])),
            "INCOME": len(b.get("INCOME", [])),
            "KNOWLEDGE": len(b.get("KNOWLEDGE", [])),
            "TRASH": len(b.get("TRASH", [])),
            "action_queue": len(memory.get("action_queue", [])),
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
