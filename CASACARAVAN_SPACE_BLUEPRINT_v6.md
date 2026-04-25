# Casa Caravan Space — Blueprint v6

> *A space that helps you realize yourself.*
> casacaravan.space

---

## Vizyon
Amaç ormana gitmek. Ama çıkıldığında dönülecek bir ev olmalı.
Koridor ev. Bahçe geçiş. Orman asıl.

---

## Canlı Sayfalar

| Sayfa | İçerik |
|-------|--------|
| index.html | Giriş, gong |
| corridor-3d.html | Three.js koridor, 6 kapı, radyo |
| audio_sanctuary.html | Stüdyo, EQ Key IV, kayıt |
| fermentation_lab.html | Tarif hesaplayıcı, Key III |
| games.html | The Keys ARG — players, hints |
| headspace.html | Cymatics, Key I |
| idea_basket.html | Fikir sepeti, Supabase |
| herbal_atelier.html | Extract calculator, Key II |
| garden.html | Bahçe, chat, radyo, observatory |
| forest.html | Three.js orman, S-curve yol, kırmızı ağaç |
| observatory.html | Yıldız kubbesi, zodiac, 20 yıldız |
| about.html | Brand hikayesi |
| admin_analytics.html | Ziyaretçi paneli |

---

## The Keys — ARG

| # | Lokasyon | Mekanik |
|---|----------|---------|
| I | Headspace | M:7 N:3 cymatics, 10sn bekle |
| II | Herbal Atelier | Olive leaf sayfası firefly |
| III | Fermentation Lab | Sourdough tarifi firefly |
| IV | Audio Sanctuary | EQ gülen yüz [8,3,-5,-5,3,8] ±5 |
| V | Garden Chat | "i wish i had a key" + "your wish came true" |
| VI | Forest | Kırmızı ağaç, 5 anahtar şart |
| VII | Corridor | 6 anahtar → 7. kapı → welcome + form |

**Ödüller:** Kendi odası (1 ay ücretsiz) / Başka bir tool / Sonraki oyunun yapımcısı

---

## Supabase

**URL:** https://iwfvlatywksvnnxymweb.supabase.co · West EU Paris

| Tablo | Amaç |
|-------|------|
| garden_chat | Realtime chat |
| idea_basket | Fikirler, Key VII formları |
| page_visits | Analytics |
| players | ARG oyuncuları, keys_found[] |

---

## Garden Chat — Key V Flow
1. İsim gir (localStorage)
2. Son 60 mesaj yüklenir
3. "i wish i had a key" + "your wish came true" → ikisi de Key V alır
4. Chat hint: games.html'de açık yazılı

---

## Radyo İstasyonları
- **Drone Zone** — atmosferik minimal
- **Bossa Beyond** — latin/bossa
- **Lush** — yumuşak elektronik

Koridor + Bahçe'de aynı istasyonlar.

---

## Forest — Yol Sistemi
- CatmullRomCurve3 ile S-curve patikalar
- Sol → kırmızı ağaç (deeper in)
- Sağ → telefon ışığı (turn on your flashlight)
- Maya kalıntıları kırmızı ağacın yanında

---

## İş Modeli

| Katman | Durum |
|--------|-------|
| 1 — Açık | ✓ Aktif |
| 2 — Email kayıt | Beta'da gönüllü |
| 3 — Ücretli | Çalışılacak |
| 4 — Kiracı | Key VII kazananlardan başlar |

---

## Organik Büyüme Planı
- Hacker News — Show HN
- Reddit: r/InternetIsBeautiful, r/AR_Gaming, r/cymatics, r/fermentation, r/herbalism
- Product Hunt
- Discord: Indie Hackers, ARG communities

---

*Blueprint v6 — Nisan 2026*
