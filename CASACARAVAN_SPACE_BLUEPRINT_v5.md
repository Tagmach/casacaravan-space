# Casa Caravan Space — Blueprint v5.2

> *A space that helps you realize yourself.*
> *Burası bir iş yeri. Emeğin karşılığını hak ediyor.*

---

## Vizyon

Amaç ormana gitmek. Ama çıkıldığında dönülecek bir ev olmalı.
Koridor ev. Bahçe geçiş. Orman asıl.

---

## İş Modeli

**Prensip:** Gelir getirmeyecekse maliyet oluşturmasın.

| Katman | Kim | Ücret | Durum |
|--------|-----|-------|-------|
| 1 — Açık | Herkes | Ücretsiz, sonsuza | ✓ Aktif |
| 2 — Kayıtlı | Email ile giriş | Ücretsiz | Beta'da gönüllü |
| 3 — Üye | Gelişmiş özellikler | Ücretli | Çalışılıyor |
| 4 — Kiracı | Oda kirası + komisyon | Ücretli | Trafik gelince |

---

## Koruma Mimarisi

- **Domain lock** — tool'lar sadece casacaravan.space'de çalışır
- **Beacon** — başka domain'den açılırsa ping atar, log tutulur
- **Sosyal paylaşım** — X, WhatsApp, Telegram, link kopyala — her tool'da
- **Repo** — şimdilik public, Katman 2 geçişinde private

---

## Canlı Dosyalar (Nisan 2026)

```
casacaravan.space/
├── index.html              — Giriş + Audio Sanctuary ✓
├── corridor-3d.html        — Three.js koridor ✓
├── garden.html             — Gece bahçesi, ses, chat ✓
├── games.html              — Magic Ball ✓
├── headspace.html          — Cymatics Simulator ✓
├── herbal_atelier.html     — Extract Calculator + Rehber ✓
├── fermentation_lab.html   — Bağlandı ✓
├── about.html              — Brand hikayesi ✓
└── cricket.mp3             — Bahçe sesi ✓
```

---

## Koridor Kapı Haritası

| Kapı | Renk | Dosya | Durum |
|------|------|-------|-------|
| Audio Sanctuary L z=-2 | Amber | index.html#sanctuary | ✓ |
| Fermentation Lab R z=-2 | Yeşil | fermentation_lab.html | ✓ |
| Games L z=-10 | Mor | games.html | ✓ |
| Headspace R z=-10 | Mavi | headspace.html | ✓ |
| Idea Basket L z=-18 | Turuncu | — | Soon |
| Herbal Atelier R z=-18 | Koyu yeşil | herbal_atelier.html | ✓ |
| The Garden (cam kapı) | Altın | garden.html | ✓ |

---

## SEO Stratejisi

- Katman 1 sonsuza açık — Google tarar
- Tool'lar arası internal linking — ağ sinyali
- Sosyal paylaşım butonları — organik yayılma
- sitemap.xml — bekliyor
- İçerik katmanı (blog/guide) — Phase 6

---

## Brand

- **Font:** Cormorant Garamond 300 + Jost 200-400
- **Renkler:** #0A0908 / #A08060 / #D2C3AF / #C8C2B8
- **Tagline aktif:** · create with life
- **Rezervde:** breath · resonate · evolve

---

## Paralel Projeler

- casacaravanshop.com — fiziksel, Kuzey Kıbrıs
- Tagmac Wellness App — Flutter/Supabase

---

*Blueprint v5.2 — Nisan 2026*
