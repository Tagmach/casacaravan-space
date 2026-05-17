"""
khashif_network_viz.py
Khashif her session sonunda bu modülü çağırır.
Memory'deki rezonans bulguları ve RSS kaynaklarını network HTML'e yazar.
"""

import json
import os
import re
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
NETWORK_FILE = os.path.join(SCRIPT_DIR, "khashif_network.html")
MEMORY_FILE = os.path.join(SCRIPT_DIR, "khashif_memory.json")

SEED_FEEDS = [
    "https://disquiet.com/feed/",
    "https://www.wildfermentation.com/feed/",
    "https://www.permaculturenews.org/feed/",
    "https://opensource.com/feed",
]


def domain_of(url):
    m = re.search(r'https?://(?:www\.)?([^/]+)', url)
    return m.group(1) if m else url[:30]


def generate(memory=None):
    """Network HTML'i memory'deki verilerle güncelle"""

    # Memory yükle
    if memory is None:
        try:
            if os.path.exists(MEMORY_FILE):
                with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                    memory = json.load(f)
        except Exception as e:
            print(f"  ! Memory yüklenemedi: {e}")
            return

    if not memory:
        return

    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    seed_set = set(SEED_FEEDS)
    dynamic_feeds = memory.get("dynamic_feeds", [])
    buckets = memory.get("buckets", {})
    stats = memory.get("stats", {})
    learned = memory.get("learned_keywords", [])
    intersections = memory.get("intersections", [])

    # === NODES ===
    nodes = []

    # Merkez
    nodes.append({
        "id": "tagmac",
        "label": "Tagmac",
        "type": "center",
        "connections": 0,
        "score": None,
        "action": None,
        "url": "https://casacaravan.space"
    })

    # Seed feeds
    for f in SEED_FEEDS:
        d = domain_of(f)
        nodes.append({
            "id": d,
            "label": d,
            "type": "seed",
            "connections": 1,
            "score": None,
            "action": None,
            "url": f
        })

    # Crawled / dynamic feeds
    for f in dynamic_feeds[-30:]:
        d = domain_of(f)
        if not any(n["id"] == d for n in nodes):
            nodes.append({
                "id": d,
                "label": d,
                "type": "dynamic",
                "connections": 1,
                "score": None,
                "action": None,
                "url": f
            })

    # Rezonans içerikler — tüm bucket'lardan son 40
    all_resonant = []
    for bucket_name in ["HUMAN", "INCOME", "KNOWLEDGE"]:
        for item in buckets.get(bucket_name, [])[-15:]:
            all_resonant.append({**item, "bucket": bucket_name})

    # Skor ve tarihe göre sırala
    all_resonant.sort(key=lambda x: (float(x.get("score", 0) or 0), x.get("date", "")), reverse=True)

    content_ids = set()
    for item in all_resonant[:40]:
        link = item.get("link", "")
        if not link or link in content_ids:
            continue
        content_ids.add(link)

        source_domain = domain_of(item.get("source", ""))
        # Kaynak node bulunamazsa tagmac'a bağla
        source_id = source_domain if any(n["id"] == source_domain for n in nodes) else "tagmac"

        nodes.append({
            "id": link,
            "label": item.get("title", "")[:40],
            "type": "content",
            "connections": 1,
            "score": item.get("score", "5"),
            "action": item.get("action", ""),
            "reason": item.get("reason", ""),
            "bucket": item.get("bucket", ""),
            "url": link,
            "source": source_id
        })

    # Intersection node'ları
    for ix in intersections[-5:]:
        ix_id = f"ix_{ix.get('label','').replace(' ','_').replace('+','_')}"
        if not any(n["id"] == ix_id for n in nodes):
            nodes.append({
                "id": ix_id,
                "label": ix.get("label", ""),
                "type": "intersection",
                "connections": ix.get("strength", 1),
                "score": None,
                "action": "INTERSECTION",
                "reason": ix.get("insight", "")[:100],
                "url": "",
                "source": "tagmac"
            })

    # Connection sayısını güncelle
    nodes[0]["connections"] = len(nodes) - 1

    # === EDGES ===
    edges = []

    node_ids = {n["id"] for n in nodes}

    # Tagmac → feed'ler
    for n in nodes:
        if n["type"] in ["seed", "dynamic"]:
            strength = 0.8 if n["type"] == "seed" else 0.5
            edges.append({"from": "tagmac", "to": n["id"], "strength": strength})

    # Feed → içerik
    for n in nodes:
        if n["type"] == "content":
            src = n.get("source", "tagmac")
            if src in node_ids:
                score = float(n.get("score") or 5)
                strength = round(score / 10, 1)
                edges.append({"from": src, "to": n["id"], "strength": strength})
            else:
                edges.append({"from": "tagmac", "to": n["id"], "strength": 0.3})

    # Intersection → tagmac
    for n in nodes:
        if n["type"] == "intersection":
            edges.append({"from": "tagmac", "to": n["id"], "strength": 0.9})

    # === STATS ===
    total_resonant = stats.get("total_resonant", 0)
    total_analyzed = stats.get("total_analyzed", 0)
    total_feeds = len(SEED_FEEDS) + len(dynamic_feeds)
    keyword_count = len(learned)
    intersection_count = len(intersections)

    stats_html = (
        f"{len(nodes)} düğüm · {len(edges)} bağlantı<br>"
        f"{total_resonant} rezonans · {intersection_count} kesişim<br>"
        f"{total_feeds} RSS · {keyword_count} kelime"
    )

    keywords_html = ", ".join(learned[-20:]) if learned else ""

    # Legend güncelle — yeni type'lar
    legend_html = """
    <div class="leg"><div class="leg-dot" style="background:#c8965a;"></div>seed kaynak</div>
    <div class="leg"><div class="leg-dot" style="background:#5ac88a;"></div>crawled kaynak</div>
    <div class="leg"><div class="leg-dot" style="background:#c85a7a;"></div>rezonans içerik</div>
    <div class="leg"><div class="leg-dot" style="background:#a060c8;"></div>intersection</div>
    <div class="leg"><div class="leg-dot" style="background:#ffffff;box-shadow:0 0 5px #fff;"></div>eylem gerekli</div>
"""

    # colorOf fonksiyonu güncelle
    color_fn = """function colorOf(n) {
  if (n.action && ['COMMENT','SUBMIT','ATTEND','CONNECT'].includes(n.action)) return '#ffffff';
  if (n.type === 'center') return '#c8965a';
  if (n.type === 'seed') return '#c8965a';
  if (n.type === 'dynamic') return '#5ac88a';
  if (n.type === 'intersection') return '#a060c8';
  if (n.bucket === 'HUMAN') return '#c85a7a';
  if (n.bucket === 'INCOME') return '#c8965a';
  if (n.bucket === 'KNOWLEDGE') return '#5a8fc8';
  return '#c85a7a';
}"""

    # === HTML OLUŞTUR ===
    try:
        with open(NETWORK_FILE, "r", encoding="utf-8") as f:
            html = f.read()
    except FileNotFoundError:
        print(f"  ! Network HTML bulunamadı: {NETWORK_FILE}")
        return

    # NODES ve EDGES güncelle
    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)

    html = re.sub(r'const NODES = \[.*?\];', f'const NODES = {nodes_json};', html, flags=re.DOTALL)
    html = re.sub(r'const EDGES = \[.*?\];', f'const EDGES = {edges_json};', html, flags=re.DOTALL)

    # Stats güncelle
    html = re.sub(r'<div id="updated">.*?</div>', f'<div id="updated">son gezi: {now}</div>', html)
    html = re.sub(r'<div id="stats">.*?</div>', f'<div id="stats">{stats_html}</div>', html, flags=re.DOTALL)
    html = re.sub(r'<div id="keywords">.*?</div>', f'<div id="keywords">{keywords_html}</div>', html, flags=re.DOTALL)
    html = re.sub(r'<div id="legend">.*?</div>', f'<div id="legend">{legend_html}</div>', html, flags=re.DOTALL)

    # colorOf fonksiyonunu güncelle
    html = re.sub(r'function colorOf\(n\) \{.*?\}', color_fn, html, flags=re.DOTALL)

    with open(NETWORK_FILE, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  ✓ Network güncellendi — {len(nodes)} node, {len(edges)} edge, {intersection_count} kesişim")


if __name__ == "__main__":
    generate()
    print("Network HTML güncellendi.")
