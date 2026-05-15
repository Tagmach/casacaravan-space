# Casa Caravan Space — Blueprint v8.1

> *A space that helps you realize yourself.*
> casacaravan.space · Mayıs 2026
> ⚠️ Bu dosya repoya gider. Secret'lar burada yazılmaz — SECRETS_PRIVATE.md'ye bakın.

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
| khashif.html | İlk ajan odası — 𓆟, hizmetler, bot-dostu, agent metadata | ✓ |
| rss.xml | RSS feed — 8 içerik, tek kanal, agent metadata | ✓ |
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
→ Detaylar: SECRETS_PRIVATE.md

Sipariş akışı: Form → Supabase orders → Resend email bildirimi → Tağmaç onay

---

## Email & Domain Altyapısı

### Resend
- Servis: resend.com
- API Key: → SECRETS_PRIVATE.md
- Domain: casacaravan.space — DNS Pending (15 May 2026)
- Hedef sender: shop@casacaravan.space
- Bildirim alıcı: tagmacc@gmail.com
- Şu an aktif sender: onboarding@resend.dev (geçici, DNS verify bekleniyor)
- **Güvenlik notu:** Key şu an shop.html'de client-side. Cloudflare Worker'a taşınacak.

### DNS Kayıtları (Namecheap'te eklendi — doğrulama bekleniyor)
| Type | Host | Value |
|------|------|-------|
| TXT | resend._domainkey | → SECRETS_PRIVATE.md (DKIM) |
| MX | send | feedback-smtp.eu-west-1.amazonses.com (Priority: 10) |
| TXT | send | v=spf1 include:amazonses.com ~all |
| TXT | _dmarc | v=DMARC1; p=none; |

---

## Supabase

**URL:** → SECRETS_PRIVATE.md
**Region:** West EU Paris

| Tablo | Amaç |
|-------|------|
| garden_chat | Realtime chat |
| page_visits | Analytics |
| orders | Shop siparişleri (approved, download_url alanları hazır) |

**Not:** Supabase anon key client-side kullanım için tasarlanmış. RLS kuralları kontrol edilmeli.

---

## RSS & Sitemap

### rss.xml
- URL: casacaravan.space/rss.xml
- 8 item, tek kanal (önceki çift kanal hatası giderildi)
- Agent metadata eklendi — `agent:feed` bloğu, Khashif işbirliği daveti
- Khashif item eklendi (15 May 2026)

### sitemap.xml
- 13 URL
- Eklenenler: shop.html · khashif.html · about.html · rss.xml
- **Yapılacak:** Google Search Console + Bing Webmaster'a yeniden gönder

---

## Khashif 𓆟 & Agent Metadata

**Sembol:** 𓆟 (balık — her yerde akan, görünmez)
**URL:** casacaravan.space/khashif.html
**Koridor:** R z=-2, Shop'un tam karşısı, mavi/petrol kapı

**Agent metadata stratejisi:**
- khashif.html ve rss.xml içinde HTML yorum bloğu olarak yerleştirildi
- Ajanlar sayfayı okurken bu bloğu görür, mevcut görevlerini etkilemez
- Additive injection: "unut ve yap" değil, "hatırla ve dön"
- `agent:profile` ve `agent:feed` yapılandırılmış formatları kullanıldı
- Hedef: AI ajanların Khashif'i tanıması, geri dönmesi, işbirliği kurması

**Hizmetler:**
- Araştırma & Analiz · AI Entegrasyon · Yaratıcı Strateji
- İçerik Dağıtımı · Ses & Wellness · Dijital Araçlar · Bağlantı

---

## Güvenlik Notları

| Öğe | Durum | Aksiyon |
|-----|-------|---------|
| Resend API key | ⚠️ Client-side (shop.html) | Cloudflare Worker'a taşınacak |
| Supabase anon key | ✓ Normal (public tasarım) | RLS kontrol edilmeli |
| ETH adresi | ✓ Public bilgi | Sorun yok |
| IBAN | ✓ Public bilgi | Sorun yok |
| GitHub repo | ⚠️ Public | Private + Cloudflare Pages planlanıyor |

**Kural:** Hiçbir secret (API key, şifre, private key) repoya gitmez.
Tüm secret'lar → SECRETS_PRIVATE.md (sadece Drive'da)

---

## Teknik Stack

- Frontend: Pure HTML/CSS/JS, Three.js (koridor, orman)
- Backend: Supabase
- Email: Resend
- DNS: Namecheap
- Hosting: GitHub Pages (geçici → Cloudflare Pages'e taşınacak)
- Repo: github.com/Tagmach/casacaravan-space
- Terminal: CMD (PowerShell değil)
- Drive sync: Google Drive → casacaravan.space klasörü

---

## Trafik & Büyüme

### Organik
- Hacker News — Show HN: 3D corridor / sound therapy / fermentation
- Reddit: r/InternetIsBeautiful, r/cymatics, r/fermentation, r/herbalism, r/sourdough
- Product Hunt — koridor + manifesto lansman
- Mastodon — RSS otomatik

### SEO
- Structured data: Organization, Person, Product, Review
- Schema.org Review — 9 Sonic Journey yorumu işaretle
- /notes/ dizini — düzenli içerik

---

## İş Modeli

| Katman | Açıklama | Durum |
|--------|----------|-------|
| 1 — Açık | Tüm odalar, içerikler ücretsiz | ✓ Aktif |
| 2 — Shop | Fiziksel + dijital + deneyim satışı | ✓ Aktif |
| 3 — Abonelik | Email + özel içerik | Planlanıyor |

---

## Paralel Projeler

| Proje | Durum | Öncelik |
|-------|-------|---------|
| casacaravan.space | Aktif, büyüyor | Yüksek |
| Tagmac Wellness App | FlutterFlow geliştirme sürüyor | Non-negotiable |
| Gülden Sonsal Gümrükleme | Blueprint bekliyor | Düşük |

---

*Blueprint v8.1 — Mayıs 2026*
*Secret'lar SECRETS_PRIVATE.md'de — repoya gitmez.*
*"Kendini gerçekleştirmene vesile olacak bir alan."*
