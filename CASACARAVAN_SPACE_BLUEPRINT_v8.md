# Casa Caravan Space — Blueprint v8

> *A space that helps you realize yourself.*
> casacaravan.space · Mayıs 2026

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
| index.html | Giriş, gong animasyonu, gong_entrance.mp3 (4sn) | ✓ |
| corridor-3d.html | Three.js koridor, 6 kapı, shop, radyo, noscript SEO katmanı | ✓ |
| about.html | Manifesto — Mayıs 2026 | ✓ |
| shop.html | Müzik player, ürünler, Khashif hizmetleri, Supabase orders, Resend bildirim, ödeme detayları | ✓ |
| khashif.html | İlk ajan odası — 𓆟 balık sembolü, hizmetler, bot-dostu | ✓ |
| rss.xml | RSS feed — 8 içerik, tek kanal, kategorili | ✓ |
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
| L z=-10 | Fermentation Lab | Yeşil | fermentation_lab.html |
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
Sipariş akışı: Form → Supabase orders → Resend email bildirimi → Tağmaç onay

### Ödeme Detayları

**TR IBAN (Banka Havalesi)**
- Beneficiary: TAGMACH CHANKAYA
- IBAN: TR20 0006 4000 0016 8130 0605 15

**Revolut**
- Beneficiary: TAGMACH CHANKAYA
- IBAN: LT62 3250 0984 5562 5476
- BIC/SWIFT: REVOLT21
- Bank: Revolut Bank UAB, Konstitucijos ave. 21B, 08130 Vilnius, Lithuania
- Correspondent BIC: CHASDEFX

**Ethereum (ERC-20)**
- Wallet: 0xeE9cc0F4dDeBffb701b6F43EEDaAb2bdD11C1894
- Phantom cüzdan, Ethereum mainnet
- Desteklenen: ETH + ERC-20 stablecoin (USDC/USDT)
- Kullanıcı TX hash'i note alanına yazıyor

### Yakın Dönem Eklenecek
- Taş/kerpiç fırın (Kıbrıs teslim)
- Upcycled furniture (Kıbrıs teslim)
- Gelecek müzik albümü/single'lar

---

## Email & Domain Altyapısı

### Resend
- Servis: [resend.com](https://resend.com)
- API Key: `re_8Yrdyxjr_HQxxkfZ8t1FsVMYCgNsW34ag`
- Domain: `casacaravan.space` — **DNS Pending** (15 May 2026)
- Hedef sender: `shop@casacaravan.space`
- Bildirim alıcı: `tagmacc@gmail.com`
- Şu an aktif sender: `onboarding@resend.dev` (geçici)

### DNS Kayıtları (Namecheap'te eklendi — doğrulama bekleniyor)
| Type | Host | Value |
|------|------|-------|
| TXT | `resend._domainkey` | `p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC//gJL37Cg1csRLhPjeG4RAvnoZ7ILqH/fuTG0tWZR7WJxlpmYSvy9OHuyMIHQHUYm6SeIFQppOF1E7k58vuFiSX7abk1NPspBzDmFP0srQpNQI1+ShigoG5hZJxpsGH4oj0/qEWR/NQ7cL5VnyoSLdwkH/quMAe5kkFaeEmRT7QIDAQAB` |
| MX | `send` | `feedback-smtp.eu-west-1.amazonses.com` (Priority: 10) |
| TXT | `send` | `v=spf1 include:amazonses.com ~all` |
| TXT | `_dmarc` | `v=DMARC1; p=none;` |

---

## Supabase

**URL:** https://iwfvlatywksvnnxymweb.supabase.co · West EU Paris

| Tablo | Amaç |
|-------|------|
| garden_chat | Realtime chat |
| page_visits | Analytics |
| orders | Shop siparişleri (approved, download_url alanları hazır) |

---

## RSS & Sitemap

### rss.xml
- URL: casacaravan.space/rss.xml
- 8 item, tek kanal (önceki çift kanal hatası giderildi)
- Kategoriler: Sound Healing · Gong Bath · Fermentation · Plant Medicine · Music · Creative Technology · Resonance · Cyprus
- Khashif item eklendi (15 May 2026)

### sitemap.xml
- 13 URL
- Eklenenler: shop.html · khashif.html · about.html · rss.xml
- **Yapılacak:** Google Search Console + Bing Webmaster'a yeniden gönder

---

## Garden

- Ay fazı: Canvas tabanlı, gerçek synodic hesap, her saat güncellenir
- Ateşböcekleri: Dekoratif
- Star Observatory: Nebula canvas animasyonu
- Forest girişi: Rünik işaretler, yeşil neon
- Radyo: Drone Zone · Bossa Beyond · Lush
- Chat: Garden Chat, Supabase realtime

---

## Khashif 𓆟

**Sembol:** 𓆟 (balık — her yerde akan, görünmez)
**URL:** casacaravan.space/khashif.html
**Koridor:** R z=-2, Shop'un tam karşısı, mavi/petrol kapı
**Shop'ta:** Ayrı bölüm olarak listeleniyor

**Hizmetler:**
- Araştırma & Analiz
- AI Entegrasyon
- Yaratıcı Strateji
- İçerik Dağıtımı
- Ses & Wellness
- Dijital Araçlar
- Bağlantı

**İletişim:** WhatsApp +90 533 880 0870

**Ajan Hub:** agents.html planlanıyor — şu an XML tabanlı ajan iletişim formatı aktif

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

## Teknik Stack

- Frontend: Pure HTML/CSS/JS, Three.js (koridor, orman)
- Backend: Supabase (garden_chat, orders, page_visits)
- Email: Resend (sipariş bildirimi)
- DNS: Namecheap
- Hosting: GitHub Pages
- Repo: github.com/Tagmach/casacaravan-space
- Terminal: CMD (PowerShell değil)
- Drive sync: Google Drive → casacaravan.space klasörü

---

## Paralel Projeler

| Proje | Durum | Öncelik |
|-------|-------|---------|
| casacaravan.space | Aktif, büyüyor | Yüksek |
| Tagmac Wellness App | FlutterFlow geliştirme sürüyor | Non-negotiable |
| Jakelu | Blueprint hazır, entegrasyon bekliyor | Orta |
| Gülden Sonsal Gümrükleme | Blueprint bekliyor | Düşük |

---

*Blueprint v8 — Mayıs 2026*
*"Kendini gerçekleştirmene vesile olacak bir alan."*
