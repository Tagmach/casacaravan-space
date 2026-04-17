# Casa Caravan Space — Blueprint v5.0

> *A space that helps you realize yourself.*

**Tagline:** Hayatla birlikte üret. — Create with life.
**Domain:** casacaravan.space
**Language:** English (global)

---

## The One Sentence

> A space that helps you realize yourself.

---

## Canlı Mimari (Nisan 2026)

```
casacaravan.space/
│
├── index.html
│   └── Entrance — gong strike → corridor-3d.html
│
├── corridor-3d.html  ← YENİ
│   └── Three.js 3D koridor
│       ├── Audio Sanctuary (L, z=-2)     → index.html#sanctuary
│       ├── Fermentation Lab (R, z=-2)    → coming soon
│       ├── Games (L, z=-10)              → coming soon
│       ├── Headspace (R, z=-10)          → coming soon
│       ├── Idea Basket (L, z=-18)        → coming soon
│       ├── Herbal Atelier (R, z=-18)     → coming soon
│       └── The Forest (arka duvar)       → coming soon
│
├── about.html
│   └── Guatemala hikayesi + Casa Caravan origin
│
└── og-image.png, gong sounds, CNAME
```

---

## Koridor Teknik Detaylar

- **Engine:** Three.js r128 (CDN)
- **Perspektif:** PerspectiveCamera, FOV 65
- **Koridor:** W=5, H=4, L=32 birim
- **Kamera pozisyonları:** z=1, -6, -14, -20 (4 adım)
- **Kapılar:** MeshStandardMaterial, canvas texture tabelalar, billboard
- **Pencereler:** Her 4 birimde bir, gece gökyüzü, ay, yıldızlar
- **Işıklandırma:** Ambient + Directional + sconce PointLights
- **Hareket:** Smooth lerp (t*4), 0.75s geçiş hissi

---

## Felsefe

Koridorun sonunda bilinen biter, orman başlar.
Işığı kapattığında ateş böceklerini görürsün.

Beden ve rezonans aynı şeyin iki yüzü.
Beslenme ve ses. Fermentasyon ve nefes.

---

## Kapı Renk Dili

| Kapı | Renk | Dünya |
|------|------|-------|
| Audio Sanctuary | Amber/altın | Ses, kayıt, sıcaklık |
| Fermentation Lab | Yeşil | Canlı, büyüyen |
| Games | Mor/indigo | Oyun, felsefe |
| Headspace | Mavi | Sessizlik, nefes |
| Idea Basket | Turuncu/terracotta | Bırak, bul |
| Herbal Atelier | Koyu yeşil | Bitki, kök |
| The Forest | Gece yeşili | Bilinmez, sürpriz |

---

## Hedef Kitle

28–50 yaş. Üretici, meraklı, derinlik arayan.
Dijitalde kalite arayan, marjinal değil ama ana akımdan sıkılmış.

---

## Gelir Modeli

| Aşama | Ne | Durum |
|-------|-----|-------|
| 1 | Audio Sanctuary — Lemon Squeezy | Bekliyor |
| 2 | Fermentation Lab, physical products | Planlandı |
| 3 | Membership — Supabase | Phase 5 |

---

## Paralel Projeler

- **casacaravanshop.com** — fiziksel ürünler, Kuzey Kıbrıs
- **Tagmac Wellness App** — Flutter/Supabase, ayrı proje

---

*Blueprint v5.0 — Nisan 2026*
*"Kendini gerçekleştirmene vesile olacak bir alan."*
