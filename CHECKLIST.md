# Casa Caravan Space — Checklist

> casacaravan.space · GitHub: Tagmach/casacaravan-space
> Last updated: April 2026

---

## Phase 1 — Foundation ✓
- [x] Domain, GitHub Pages, HTTPS
- [x] Entrance — gong, animasyon, ses
- [x] about.html — brand hikayesi, Guatemala, ortam felsefesi
- [x] Full SEO — meta, OG, Twitter Card, JSON-LD

---

## Phase 2 — Corridor 3D ✓
- [x] corridor-3d.html — Three.js, arch kapılar, pencereler, billboard tabelalar
- [x] Kamera hareketi — 4 pozisyon, swipe desteği
- [x] Mobil FOV ayarı (85°), başlangıç pozisyonu
- [x] Tabelalar ve oklar clickable (desktop + mobile)
- [x] The Garden — taş kemer, çift cam kapı, "Garden" yazısı, zemin okları
- [x] Sconce'lar pencereler arasında ortalandı
- [x] index.html ↔ corridor-3d.html entegrasyonu

---

## Phase 3 — Odalar ✓
- [x] Audio Sanctuary — index.html içinde, stüdyo, kayıt
- [x] games.html — Magic Ball
- [x] headspace.html — Cymatics Simulator (Chladni)
- [x] fermentation_lab.html — bağlandı
- [x] herbal_atelier.html — full spectrum extract calculator + rehber
- [x] idea_basket.html — Supabase bağlı, moderasyon sistemi
- [x] garden.html — gece bahçesi, ses, chat
- [x] forest.html — Three.js jungle, ateş böcekleri, cricket sesi

---

## Phase 3b — Koruma & Paylaşım ✓
- [x] Domain lock — tool'lar sadece casacaravan.space'de çalışır
- [x] Beacon — başka domain'den açılırsa ping atar
- [x] Sosyal medya paylaşım butonları — X, WhatsApp, Telegram, link kopyala

---

## Phase 3c — Yapısal Temizlik
- [ ] **Audio Sanctuary'yi index.html'den çıkar → audio_sanctuary.html**
- [ ] Beacon loglarını yakala — Supabase edge function veya Cloudflare Worker

---

## Phase 4 — Supabase Entegrasyonları ✓
- [x] garden_chat tablosu — Supabase Realtime
- [x] idea_basket tablosu — Supabase, moderasyon
- [x] Idea Basket moderasyonu — Supabase Table Editor'den approve/disapprove
- [ ] Idea Basket → admin panel (opsiyonel, Supabase'den yönetiliyor şimdilik)

---

## Phase 5 — Mobil ✓ (kısmi)
- [x] Garden mobil responsive — overflow fix, z-index düzenlemeleri
- [x] Corridor mobil — FOV, swipe, başlangıç pozisyonu
- [ ] Headspace, Herbal Atelier mobil test
- [ ] Forest mobil test

---

## Phase 6 — Kullanıcı Katmanları

**Model (karar verildi):**
- **Katman 1** — Koridor + temel araçlar → sonsuza açık ✓
- **Katman 2** — Email kaydı → ücretsiz, beta'da gönüllü, sonra zorunlu
- **Katman 3** — Ücretli üyelik → çalışılacak, önce sen ikna olacaksın
- **Katman 4** — Kiracı modeli → trafik gelince masaya yatar

- [ ] Supabase auth — email kayıt (Katman 2)
- [ ] Cloud save — Audio Sanctuary kayıtları
- [ ] Beta → Katman 2 geçiş tetikleyicisi belirle

---

## Phase 7 — SEO & Büyüme
- [ ] sitemap.xml
- [ ] Blog/içerik katmanı
- [ ] Beta duyurusu — sistem üzerinden, Space ile etkileşim

---

## Phase 8 — Garden Tamamlama
- [ ] Star Lab — statik yıldız JSON, keyword chat (Claude API gelir gelince)
- [ ] Garden Chat moderasyon (şimdilik Supabase'den)
- [ ] Sit & Breathe aktivasyonu

---

## Phase 9 — Orman İçi
- [ ] forest.html — içerik, generatif
- [ ] Bahçeden geçiş animasyonu

---

## ⚠️ Karar Verilecekler
- Katman 3 fiyatlandırması — ne zaman, kaç?
- Beta bitiş tetikleyicisi: kaç kullanıcı?
- Repo ne zaman private?
- Star Lab: Claude API ne zaman açılır?

---

*"Kendini gerçekleştirmene vesile olacak bir alan."*
*Burası bir iş yeri. Emeğin karşılığını hak ediyor.*
