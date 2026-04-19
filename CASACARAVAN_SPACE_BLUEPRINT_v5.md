# Casa Caravan Space — Blueprint v5.1

> *A space that helps you realize yourself.*

**Tagline:** · create with life
**Domain:** casacaravan.space
**Language:** English (global)

---

## Vizyon

Amaç ormana gitmek.
Ama çıkıldığında dönülecek bir ev olmalı.

Koridor ev. Bahçe geçiş. Orman asıl.

---

## Canlı Mimari (Nisan 2026)

```
casacaravan.space/
│
├── index.html              — Giriş (gong) + Audio Sanctuary
│       ↓ 5 saniye
├── corridor-3d.html        — Three.js 3D koridor ✓
│   ├── Audio Sanctuary (L, z=-2)   → index.html#sanctuary ✓
│   ├── Fermentation Lab (R, z=-2)  → fermentation_lab.html ✓
│   ├── Games (L, z=-10)            → games.html ✓
│   ├── Headspace (R, z=-10)        → headspace.html ✓
│   ├── Idea Basket (L, z=-18)      → coming soon
│   ├── Herbal Atelier (R, z=-18)   → coming soon
│   └── The Garden (cam kapı)       → garden.html ✓
│           ↓
├── garden.html             — Gece bahçesi ✓
│   ├── Cırcır sesi (Howler.js) ✓
│   ├── Garden Chat (localStorage → Supabase) ✓
│   ├── Idea Basket köşesi — coming soon
│   ├── Star Lab köşesi — coming soon
│   └── The Forest → forest.html (coming soon)
│           ↓
└── forest.html             — Orman (henüz yok)
```

---

## Dosyalar

| Dosya | Durum | Not |
|-------|-------|-----|
| index.html | ✓ | Giriş + Audio Sanctuary gömülü |
| corridor-3d.html | ✓ | Three.js, 6 kapı, pencereler |
| garden.html | ✓ | Gece, ses, chat |
| games.html | ✓ | Magic Ball |
| headspace.html | ✓ | Cymatics Simulator |
| fermentation_lab.html | ✓ | Bağlandı |
| about.html | ✓ | Brand hikayesi |
| audio_sanctuary.html | ✗ | Sonraki adım — index'ten ayır |
| forest.html | ✗ | Phase 8 |

---

## Prensip

**Gelir getirmeyecekse maliyet oluşturmasın.**

- Star Lab → Claude API bağlantısı gelir gelince
- Supabase → Beta ücretsiz, sonra üyelik
- Tüm araçlar önce ücretsiz, sonra premium katman

---

## Koridor Teknik

- Three.js r128, PerspectiveCamera FOV 65
- W=5, H=4, L=32 — düz duvarlar, düz tavan
- 4 walk pozisyonu: z=1, -6, -14, -20
- Billboard tabelalar — Cormorant Garamond 300
- Sconce'lar pencereler arasında (z: -4,-8,-12,-16,-20,-24,-28)
- The Garden: cam kapı, W×0.68, yere kadar

---

## Oda Renk Dili

| Oda | Renk |
|-----|------|
| Audio Sanctuary | Amber #e8a830 |
| Fermentation Lab | Yeşil #70b040 |
| Games | Mor #9070d0 |
| Headspace | Mavi #6090c0 |
| Idea Basket | Turuncu #d07040 |
| Herbal Atelier | Koyu yeşil #78b038 |
| The Garden | Altın #A08060 |

---

## Brand

- **Font:** Cormorant Garamond 300 + Jost 200-400
- **Renkler:** #0A0908 / #A08060 / #D2C3AF / #C8C2B8
- **Ses:** breath · resonate · evolve (rezervde)
- **Tagline aktif:** · create with life

---

## Paralel Projeler

- casacaravanshop.com — fiziksel, Kuzey Kıbrıs
- Tagmac Wellness App — Flutter/Supabase

---

*Blueprint v5.1 — Nisan 2026*
*"Kendini gerçekleştirmene vesile olacak bir alan."*
