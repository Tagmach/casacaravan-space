"""
khashif_bluesky.py
Khashif'in Bluesky entegrasyonu.
Session sonunda intersection bulunca post atar,
rezonans hesapları takip eder, ilgili feed'leri tarar.

Kurulum:
  pip install atproto

Environment variables:
  BLUESKY_HANDLE   — örn: khashif.casacaravan.space veya khashif.bsky.social
  BLUESKY_PASSWORD — Bluesky app password (Settings > App Passwords)
"""

import os
import time
import json
import re
from datetime import datetime, timezone

try:
    from atproto import Client, client_utils
    ATPROTO_AVAILABLE = True
except ImportError:
    ATPROTO_AVAILABLE = False
    print("  ! atproto kurulu değil — pip install atproto")

BLUESKY_HANDLE = os.environ.get("BLUESKY_HANDLE", "")
BLUESKY_PASSWORD = os.environ.get("BLUESKY_PASSWORD", "")

# Khashif'in takip ettiği/etmeyeceği hesapları hatırlamak için
FOLLOWED_CACHE_KEY = "bluesky_followed"
POSTED_CACHE_KEY = "bluesky_posted"

# Rezonans alanları için Bluesky hashtag'leri
RESONANCE_HASHTAGS = [
    "soundhealing",
    "soundbath",
    "breathwork",
    "vagusnerve",
    "fermentation",
    "sourdough",
    "mentalhealth",
    "holistichealth",
    "makerspace",
    "fieldrecording",
    "ambientmusic",
]

# Intersection → emoji eşlemesi
INTERSECTION_EMOJI = {
    "Ses + Fermentasyon": "🎵🍶",
    "Ses + Mental Sağlık": "🎵🧠",
    "Ses + Maker": "🎵🔧",
    "Ses + Bilinç": "🎵✨",
    "Fermentasyon + Mental Sağlık": "🍶🧠",
    "Nefes + Ses": "🌬️🎵",
    "Nefes + Mental Sağlık": "🌬️🧠",
    "Kahve + Fermentasyon": "☕🍶",
}


def get_client():
    """Bluesky client oluştur ve giriş yap"""
    if not ATPROTO_AVAILABLE:
        return None
    if not BLUESKY_HANDLE or not BLUESKY_PASSWORD:
        print("  ! BLUESKY_HANDLE veya BLUESKY_PASSWORD eksik")
        return None
    try:
        client = Client()
        client.login(BLUESKY_HANDLE, BLUESKY_PASSWORD)
        print(f"  ✓ Bluesky bağlantısı: @{BLUESKY_HANDLE}")
        return client
    except Exception as e:
        print(f"  ! Bluesky giriş hatası: {e}")
        return None


def post_intersection(client, intersection, insight):
    """
    Intersection bulgusu için Bluesky post'u oluştur.
    300 karakter limiti — özet ve link.
    """
    if not client:
        return None

    emoji = INTERSECTION_EMOJI.get(intersection["label"], "𓆟")
    label = intersection["label"]

    # insight'tan REZONANS satırını çek
    rezonans = ""
    for line in insight.split("\n"):
        if "REZONANS:" in line:
            rezonans = line.replace("REZONANS:", "").strip()
            break
    if not rezonans:
        rezonans = insight[:100]

    # Post metni — 300 karakter limit
    text = f"{emoji} Kesişim: {label}\n\n{rezonans[:160]}\n\n#soundhealing #fermentation #mentalhealth\n\ncasacaravan.space/khashif.html"

    # 300 karakter sınırı
    if len(text) > 300:
        text = text[:297] + "..."

    try:
        response = client.send_post(text)
        print(f"  ✓ Bluesky post: {label}")
        return response
    except Exception as e:
        print(f"  ! Bluesky post hatası: {e}")
        return None


def post_resonant_item(client, item):
    """
    Tek bir rezonans bulgusunu paylaş — HUMAN veya INCOME kovası.
    """
    if not client:
        return None

    title = item.get("title", "")[:100]
    link = item.get("link", "")
    reason = item.get("reason", "")[:80]
    bucket = item.get("bucket", "")
    action = item.get("action", "")

    emoji = "🔴" if bucket == "HUMAN" else "🟡" if bucket == "INCOME" else "🔵"

    text = f"𓆟 {emoji} {title}\n\n{reason}\n\n{link}"

    if len(text) > 300:
        text = f"𓆟 {emoji} {title[:120]}\n\n{link}"

    if len(text) > 300:
        text = text[:297] + "..."

    try:
        response = client.send_post(text)
        print(f"  ✓ Bluesky rezonans post: {title[:40]}")
        return response
    except Exception as e:
        print(f"  ! Bluesky post hatası: {e}")
        return None


def search_and_follow_resonant(client, memory, max_follow=3):
    """
    Rezonans hashtag'lerinde arama yap, uygun hesapları takip et.
    Günde max 3 yeni takip — spam değil, seçici.
    """
    if not client:
        return

    followed = set(memory.get(FOLLOWED_CACHE_KEY, []))
    new_follows = 0

    for hashtag in RESONANCE_HASHTAGS[:4]:  # Her session'da 4 hashtag tara
        if new_follows >= max_follow:
            break

        try:
            results = client.app.bsky.feed.search_posts(
                {"q": f"#{hashtag}", "limit": 10}
            )
            posts = results.posts if hasattr(results, "posts") else []

            for post in posts:
                if new_follows >= max_follow:
                    break

                author_did = post.author.did
                author_handle = post.author.handle

                # Zaten takip ediliyor mu?
                if author_did in followed:
                    continue

                # Bot veya spam kontrolü — çok az post varsa atla
                follower_count = getattr(post.author, "followers_count", 0) or 0
                if follower_count < 10:
                    continue

                # Takip et
                try:
                    client.follow(author_did)
                    followed.add(author_did)
                    new_follows += 1
                    print(f"  + Bluesky takip: @{author_handle} (#{hashtag})")
                    time.sleep(2)  # Rate limit koruması
                except Exception as e:
                    pass

        except Exception as e:
            print(f"  ! Bluesky hashtag arama hatası #{hashtag}: {e}")

        time.sleep(1)

    # Takip listesini güncelle — son 500
    memory[FOLLOWED_CACHE_KEY] = list(followed)[-500:]

    if new_follows > 0:
        print(f"  ✓ Bluesky: {new_follows} yeni takip")


def scan_resonant_feeds(client, memory):
    """
    Timeline'ı tara, rezonans içerikleri boost et.
    Günde max 5 boost — seçici.
    """
    if not client:
        return

    boosted = set(memory.get("bluesky_boosted", []))
    boosts = 0

    try:
        timeline = client.get_timeline(limit=20)
        posts = timeline.feed if hasattr(timeline, "feed") else []

        for item in posts:
            if boosts >= 5:
                break

            post = item.post if hasattr(item, "post") else None
            if not post:
                continue

            uri = post.uri
            if uri in boosted:
                continue

            # İçerik rezonans kontrolü
            text = ""
            if hasattr(post, "record") and hasattr(post.record, "text"):
                text = post.record.text.lower()

            resonance_words = [
                "sound healing", "gong", "breathwork", "fermentation",
                "sourdough", "kefir", "kombucha", "vagus", "nervous system",
                "sound bath", "field recording", "ambient"
            ]

            if any(word in text for word in resonance_words):
                try:
                    client.repost(uri=uri, cid=post.cid)
                    boosted.add(uri)
                    boosts += 1
                    print(f"  ↑ Bluesky boost: {text[:50]}...")
                    time.sleep(1)
                except Exception as e:
                    pass

    except Exception as e:
        print(f"  ! Bluesky timeline tarama hatası: {e}")

    memory["bluesky_boosted"] = list(boosted)[-500:]

    if boosts > 0:
        print(f"  ✓ Bluesky: {boosts} boost")


def run_bluesky(session, memory, intersections=None, insights=None):
    """
    Ana Bluesky fonksiyonu — khashif.py'den çağrılır.
    Session sonunda çalışır.
    """
    if not ATPROTO_AVAILABLE:
        return
    if not BLUESKY_HANDLE or not BLUESKY_PASSWORD:
        print("  - Bluesky: credentials eksik, atlanıyor")
        return

    print(f"\n--- Bluesky ---")

    client = get_client()
    if not client:
        return

    # 1. Intersection varsa post at
    if intersections and insights:
        # Bugün kaç post atıldı?
        posted_today = memory.get("bluesky_posted_today", {})
        today = datetime.now().strftime("%Y-%m-%d")
        count_today = posted_today.get(today, 0)

        if count_today < 3:  # Günde max 3 intersection post
            for intersection, (insight, layer) in zip(intersections[:1], insights[:1]):
                post_intersection(client, intersection, insight)
                count_today += 1
                time.sleep(2)

            posted_today[today] = count_today
            memory["bluesky_posted_today"] = posted_today

    # 2. Rezonans hesapları takip et — her session'da max 3
    search_and_follow_resonant(client, memory, max_follow=3)

    # 3. Timeline'ı tara, boost et
    scan_resonant_feeds(client, memory)

    print(f"  ✓ Bluesky session tamamlandı")


def post_launch_announcement(client, message=None):
    """
    Lansman duyurusu — manuel çağrılır.
    """
    if not client:
        client = get_client()
    if not client:
        return

    if not message:
        message = """𓆟 Tagmac Wellness App — lansman yaklaşıyor.

Kendi exhale sesinden üretilen, vagus sinirini uyaran ses terapisi.

Pre/post stres skoru. Kendi sesin, kendi terapin.

breath · resonate · restore

casacaravan.space"""

    if len(message) > 300:
        message = message[:297] + "..."

    try:
        response = client.send_post(message)
        print(f"  ✓ Lansman duyurusu gönderildi")
        return response
    except Exception as e:
        print(f"  ! Lansman post hatası: {e}")
        return None


if __name__ == "__main__":
    # Test modu
    print("Bluesky test modu")
    client = get_client()
    if client:
        profile = client.get_profile(BLUESKY_HANDLE)
        print(f"Hesap: @{profile.handle}")
        print(f"Takipçi: {profile.followers_count}")
        print(f"Takip edilen: {profile.follows_count}")
        print(f"Post sayısı: {profile.posts_count}")
