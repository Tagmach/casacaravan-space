# Casa Caravan Space — Blueprint v7

> *A space that helps you realize yourself.*
> casacaravan.space · May 2026

---

## Vizyon

Amaç ormana gitmek. Ama çıkıldığında dönülecek bir ev olmalı.
Koridor ev. Bahçe geçiş. Orman asıl.

Tağmaç + AI hibrit üretkenliği ile dijital ağ örülüyor.
Elimizde ses, fermentasyon, bitkisel bilgi, müzik ve kod var.
Globalleşiyoruz. Eller hâlâ işte.

---

## Canlı Sayfalar

| Sayfa | İçerik | Durum |
|-------|--------|-------|
| index.html | Giriş, gong animasyonu | ✓ |
| corridor-3d.html | Three.js koridor, 6 kapı, shop, radyo | ✓ |
| about.html | Manifesto — Mayıs 2026 | ✓ |
| shop.html | Müzik player, ürünler, Khashif hizmetleri, Supabase orders | ✓ |
| khashif.html | İlk ajan odası — 𓆟 balık sembolü, hizmetler, bot-dostu | ✓ |
| rss.xml | RSS feed — 7 içerik, kategorili | ✓ |
| audio_sanctuary.html | Stüdyo, EQ, kayıt | ✓ |
| headspace.html | Cymatics Simulator | ✓ |
| fermentation_lab.html | Tarif hesaplayıcı | ✓ |
| herbal_atelier.html | Extract calculator | ✓ |
| garden.html | Bahçe, chat, radyo, ay fazı, rünik işaretler | ✓ |
| forest.html | Three.js orman, S-curve yol, kırmızı ağaç | ✓ |
| observatory.html | Yıldız kubbesi, zodiac, 20 yıldız | ✓ |
| admin_analytics.html | Ziyaretçi paneli | ✓ |

---

## Koridor Kapı Yapısı

| Pozisyon | Kapı | Renk | Hedef |
|----------|------|------|-------|
| L z=-2 | Shop | Kırmızı | shop.html |
| R z=-2 | Khashif Discovery Agent | Mavi/petrol | khashif.html |
| R z=-2 | Fermentation Lab | Yeşil | fermentation_lab.html |
| L z=-10 | Work in Progress | Mor | — |
| R z=-10 | Audio Sanctuary | Altın | sub-choice overlay |
| L z=-18 | Work in Progress | Turuncu | — |
| R z=-18 | Herbal Atelier | Yeşil | herbal_atelier.html |
| Son kapı | The Garden | — | garden.html |

Audio Sanctuary sub-choice: Recording Room → audio_sanctuary.html · Cymatics Tool → headspace.html

---

## Shop

### Ürünler
| Ürün | Fiyat | Tür |
|------|-------|-----|
| Sonic Journey — Bireysel | €75 | Deneyim |
| Sonic Journey — Duo | €37.50/kişi | Deneyim |
| Sonic Journey — Online | €60 | Deneyim |
| Ukiyo Nut Butter 6-pack | €52 | Fiziksel |
| Coconut Butter 6-pack | €51 | Fiziksel |
| Sourdough Starter | €15 | Fiziksel |
| Gong/Nefes/Müzik kayıtları | €1/adet | Dijital |

Fiziksel ürünler: Kıbrıs içi + €5 shipping
Ödeme: IBAN · Revolut · Ethereum
Sipariş akışı: Form → Supabase orders → Tağmaç onaylar → dijital için download link

### Yakın Dönem Eklenecek
- Taş/kerpiç fırın (Kıbrıs teslim)
- Upcycled furniture (Kıbrıs teslim)
- Gelecek müzik albümü/single'lar

---

## Supabase

**URL:** https://iwfvlatywksvnnxymweb.supabase.co · West EU Paris

| Tablo | Amaç |
|-------|------|
| garden_chat | Realtime chat |
| page_visits | Analytics |
| orders | Shop siparişleri, approved, download_url |

---

## Garden

- Ay fazı: Canvas tabanlı, gerçek synodic hesap, her saat güncellenir, hover'da faz adı
- Ateşböcekleri: Dekoratif, ARG firefly'ları kaldırıldı
- Star Observatory: Nebula canvas animasyonu
- Forest girişi: Rünik işaretler, yeşil neon
- Radyo: Drone Zone · Bossa Beyond · Lush
- Chat: Garden Chat, Supabase realtime

---

## RSS & İçerik Stratejisi

### Feed Kategorileri
- **Sound** — Sonic Journey notları, gong üretim süreci, ses & beden
- **Fermentation** — Ekşi maya günlüğü, kombucha, mevsim notları
- **Garden Notes** — Ay takvimi, bitki gözlemleri, bahçe
- **Music** — Yeni çıkışlar, kayıt notları
- **From the Workshop** — Tahta, metal, el işi

### Yayın Ritmi
- Ay fazı: Ayda 4 (yeni ay, dolunay, çeyrekler)
- Sonic Journey: Haftalık Çarşamba sonrası kısa not
- Diğerleri: Akışa göre, zorlamadan

---

## Trafik & Büyüme

### Organik Büyüme
- Hacker News — Show HN: 3D corridor / sound therapy / fermentation
- Reddit: r/InternetIsBeautiful, r/cymatics, r/fermentation, r/herbalism, r/sourdough
- Product Hunt — koridor + manifesto lansman
- Mastodon — RSS otomatik

### SEO Hedefleri
- Structured data: Organization, Person, Product, Review
- Schema.org Review — 9 Sonic Journey yorumu işaretle
- /notes/ dizini — düzenli içerik
- Backlink: fermentasyon, sound therapy, Cyprus

### Monetizasyon
- Shop: fiziksel + dijital + deneyim
- Email list: sipariş verenler otomatik, izinle büyür
- İleride: abonelik, workshop, online session paketi

---

## İş Modeli

| Katman | Açıklama | Durum |
|--------|----------|-------|
| 1 — Açık | Tüm odalar, içerikler ücretsiz | ✓ Aktif |
| 2 — Shop | Fiziksel + dijital + deneyim satışı | ✓ Aktif |
| 3 — Abonelik | Email + özel içerik | Planlanıyor |

---

## Üç Ayak

| Proje | Durum | Öncelik |
|-------|-------|---------|
| casacaravan.space | Aktif, büyüyor | Yüksek |
| Tagmac Wellness App | Geliştirme sürüyor | Non-negotiable |

---

*Blueprint v7.1 — Mayıs 2026*
*Khashif odası eklendi, shop güncellendi, migration belgeleri hazırlandı.*
*"Kendini gerçekleştirmene vesile olacak bir alan."*
