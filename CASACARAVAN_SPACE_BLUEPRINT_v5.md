# Casa Caravan Space — Blueprint v5.0

> *A space that helps you realize yourself.*

**Tagline:** Hayatla birlikte üret. — Create with life.
**Domain:** casacaravan.space
**Language:** English (global)

---

## The One Sentence

> A space that helps you realize yourself.

---

## Vizyon

Amaç ormana gitmek.
Ama çıkıldığında dönülecek bir ev olmalı.

Koridor ev. Bahçe geçiş. Orman asıl.

---

## Mimari

```
casacaravan.space/
│
├── index.html — Giriş (gong strike)
│       ↓
├── corridor-3d.html — Koridor (ev, odalar, araçlar)
│   ├── Audio Sanctuary    — ses stüdyosu ✓
│   ├── Fermentation Lab   — coming soon
│   ├── Games              — Magic Ball ✓
│   ├── Headspace          — coming soon
│   ├── Idea Basket        — coming soon
│   ├── Herbal Atelier     — coming soon
│   └── The Forest kapısı  → garden.html
│           ↓
├── garden.html — Bahçe (mevsimsel, organik, topluluk)
│   ├── Idea Basket buraya taşınır
│   ├── Ukiyo köşesi
│   └── Orman kapısı → forest.html
│           ↓
└── forest.html — Orman (bilinmez, generatif, sonsuz)
        Çıkış var ama harita yok.
        Her girişte farklı.
        Kiracı götüremez, satılamaz.
```

---

## Şu An Canlı (Nisan 2026)

- `index.html` — giriş, gong, animasyon
- `corridor-3d.html` — Three.js 3D koridor, 6 kapı
- `about.html` — hikaye
- `games.html` — Magic Ball
- Full SEO, OG image

---

## Koridor Teknik

- Three.js r128, PerspectiveCamera FOV 65
- W=5, H=4, L=32 birim
- 4 kamera pozisyonu, smooth lerp
- Billboard tabelalar, canvas texture
- Gece pencereleri, ay, yıldızlar
- 40Hz ses eklenecek (Phase 4)

---

## Üç Alan Felsefesi

**Koridor (Ev)**
Araçlar burada. Üreticiler burada çalışır.
Kiracılar bu koridorda oda açar.
Günlük hayata dokunan, fonksiyonel.

**Bahçe**
Mevsimsel. Değişir. Büyür.
Koridorun sertliği yok, ormanın belirsizliği de yok.
Geçiş alanı. Nefes yeri.

**Orman**
Amaç bu.
Generatif, sonsuz, her girişte farklı.
Satılamaz, kiralanamaz.
Bilinen biter, bilinmez başlar.

---

## Kapı Renk Dili

| Kapı | Renk | Dünya |
|------|------|-------|
| Audio Sanctuary | Amber/altın | Ses, kayıt |
| Fermentation Lab | Yeşil | Canlı, büyüyen |
| Games | Mor/indigo | Oyun, felsefe |
| Headspace | Mavi | Sessizlik |
| Idea Basket | Turuncu | Bırak, bul |
| Herbal Atelier | Koyu yeşil | Bitki, kök |
| The Forest | Gece yeşili | Bilinmez |

---

## Kiracı Modeli (Değerlendirmede)

Bağımsız üreticiler koridorda oda açabilir.
Aracını getirir, biz yerleştiririz.
Aylık kira + satış komisyonu (karar verilmedi).
Detay: TENANT_MODEL_v1.md

---

## Hedef Kitle

28–50 yaş. Üretici, meraklı, derinlik arayan.
Dijitalde kalite arayan.

---

## Paralel Projeler

- `casacaravanshop.com` — fiziksel ürünler, Kuzey Kıbrıs
- Tagmac Wellness App — Flutter/Supabase

---

*Blueprint v5.0 — Nisan 2026*
*"Kendini gerçekleştirmene vesile olacak bir alan."*
