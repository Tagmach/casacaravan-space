# Casa Caravan Space — Checklist

> casacaravan.space · GitHub: Tagmach/casacaravan-space
> Last updated: May 2026

---

## Phase 1 — Foundation ✓
- [x] Domain, GitHub Pages, HTTPS
- [x] Entrance — gong, animasyon, ses
- [x] about.html — manifesto, güncellenmiş Mayıs 2026
- [x] Full SEO — meta, OG, Twitter Card, sitemap, robots.txt
- [x] Google Search Console + Bing Webmaster — sitemap gönderildi

---

## Phase 2 — Corridor 3D ✓
- [x] corridor-3d.html — Three.js, arch kapılar, pencereler, tabelalar
- [x] Kamera hareketi — 4 pozisyon, swipe desteği
- [x] Mobil FOV, başlangıç pozisyonu
- [x] The Garden — taş kemer, çift cam kapı
- [x] Radyo widget — Drone Zone, Bossa Beyond, Lush
- [x] Neon tabelalar — Cormorant italic, yeşil neon
- [x] Shop kapısı — kırmızı, L z=-2 pozisyonu → shop.html
- [x] Work in Progress kapıları — eski Games + Idea Basket

---

## Phase 3 — Odalar ✓
- [x] audio_sanctuary.html — stüdyo, EQ, kayıt
- [x] headspace.html — Cymatics Simulator
- [x] fermentation_lab.html — tarif hesaplayıcı
- [x] herbal_atelier.html — extract calculator + rehber
- [x] garden.html — bahçe, chat, radyo, ay fazı (canvas, gerçek zamanlı), star observatory, rünik işaretler
- [x] forest.html — Three.js jungle, S-curve yol ayrımı, kırmızı ağaç
- [x] observatory.html — yıldız kubbesi, takımyıldızları, zodiac
- [x] Audio Sanctuary sub-choice — Recording Room + Cymatics Tool seçim overlay

---

## Phase 4 — Supabase ✓
- [x] garden_chat — Realtime chat
- [x] idea_basket — moderasyon
- [x] page_visits — analytics
- [x] players — ARG oyuncuları
- [x] orders — shop siparişleri (approved, download_url alanları hazır)

---

## Phase 5 — The Keys ARG (Kaldırıldı / Askıya Alındı)
- ARG mekaniği temizlendi — keys.js, tüm firefly'lar, Key VII kapısı kaldırıldı
- Kapı pozisyonları korundu, içerikler değişecek

---

## Phase 6 — Mobil & UX ✓
- [x] Garden mobil overflow fix
- [x] Corridor mobil swipe
- [x] Garden Back Inside → corridor-3d.html

---

## Phase 7 — Admin & Analytics ✓
- [x] admin_analytics.html — ziyaretçi paneli
- [x] tracking.js — tüm sayfalarda

---

## Phase 8 — Shop (Aktif)

### Tamamlanan
- [x] shop.html — sade liste tasarımı, Casa Caravan ruhu
- [x] Ürünler: Sonic Journey (bireysel/duo/online), Ukiyo Butter, Coconut Butter, Sourdough Starter
- [x] Dijital grid — gong/nefes/müzik kayıtları €1/adet
- [x] Sepet sistemi — add/remove, fiziksel/dijital ayrımı
- [x] Sipariş formu — isim, email, telefon, adres (fiziksel için)
- [x] Ödeme seçenekleri — IBAN, Revolut, Ethereum
- [x] Supabase orders tablosu entegrasyonu
- [x] Fiziksel ürünler Kıbrıs içi, +€5 shipping
- [x] corridor-3d.html → shop.html bağlantısı

### Yapılacak — Shop
- [ ] Sipariş bildirimi — Supabase webhook + Resend/email ile Tağmaç'a otomatik bildirim
- [ ] Admin panel — orders tablosunu görüp approved yapabileceğin basit arayüz
- [ ] Dijital ürün onayı — approved=true olunca kullanıcıya download linki gönder
- [ ] Supabase Storage — dijital dosyaları yükle (gong kayıtları, müzik, nefes)
- [ ] Signed URL sistemi — satın alınan dosya için zamanlı indirme linki
- [ ] El yapımı taş/kerpiç fırın ürün olarak ekle — fotoğraf + fiyat + Kıbrıs teslim
- [ ] Shop tasarımı beyaza/açık temaya geçiş — görsel ve video destekli
- [ ] Ürün görselleri — her ürün için fotoğraf entegrasyonu
- [ ] Casacaravanshop.com → casacaravan.space/shop yönlendirmesi veya merge kararı
- [ ] Fiyatları EUR olarak sabitle — kur değişimine karşı not ekle

---

## Phase 9 — İçerik & RSS (Yapılacak)

### RSS Feed
- [ ] rss.xml oluştur — casacaravan.space/rss.xml
- [ ] Feed kategorileri: Sound · Fermentation · Garden Notes · Music · From the Workshop
- [ ] Ay fazı güncellemesi — her yeni ay, dolunay, çeyrek için kısa not (ayda 4 post)
- [ ] Sonic Journey session notları — her Çarşamba sonrası kısa gözlem
- [ ] Fermentasyon mevsim notları — sezonsallıkla
- [ ] About manifestosu RSS'e gir — ilk içerik olarak
- [ ] Sitemap.xml güncelle — shop.html, about.html (yeni), rss.xml ekle
- [ ] Google/Bing'e yeniden gönder

### İçerik Üretimi
- [ ] Her oda için kısa "neden bu oda burada" metni — SEO + RSS ham maddesi
- [ ] Sonic Journey — 9 review'ı structured data olarak işaretle (Schema.org Review)
- [ ] Gong yapım süreci — fotoğraf + kısa metin serisi
- [ ] Ekşi maya günlüğü — haftalık basit not, RSS'e beslenir
- [ ] Casa Caravan hikayesi bölümleri — About'tan genişletilmiş seriler

---

## Phase 10 — Ajanlar & Otomasyon (Yapılacak)

### Jakelu — Dağıtım Zekası
- [ ] Jakelu blueprint ve checklist hazır — entegrasyon başlayacak
- [ ] Platform profilleri — Instagram, Mastodon, Reddit, HN için ayrı ses/format
- [ ] İçerik analizi — yüklenen materyali anlayıp platform stratejisi önermesi
- [ ] RSS → Jakelu pipeline — yeni post otomatik dağıtım kuyruğuna girer
- [ ] API maliyet kuralı — token artışı öncesi her zaman uyar

### Tagmac Wellness App
- [ ] Blueprint v5 hazır — FlutterFlow geliştirme devam ediyor
- [ ] Nefesle bağlantılı dinamik adaptasyon (breath-sync) — Session ekranına entegre edilecek
- [ ] App → casacaravan.space/shop bağlantısı planla

---

## Phase 11 — Trafik & Büyüme (Yapılacak)

### Organik
- [ ] Hacker News — Show HN: "I built a 3D corridor with rooms for fermentation, sound, and herbalism"
- [ ] Reddit: r/InternetIsBeautiful, r/cymatics, r/fermentation, r/herbalism, r/sourdough
- [ ] Product Hunt — koridor + about manifesto ile lansman
- [ ] Mastodon — RSS otomatik besleme
- [ ] Substack — About manifestosundan ilk yazı, casacaravan.space'e link

### SEO
- [ ] Structured data — Organization, Person, Product, Review schema
- [ ] Blog/notes dizini — /notes/ altında düzenli içerik
- [ ] Backlink hedefleri — fermentasyon, sound therapy, Cyprus blogs

### Topluluk
- [ ] Garden Chat'i tanıt — ziyaretçileri oraya yönlendir
- [ ] Sonic Journey booking — WhatsApp yerine casacaravan.space üzerinden form
- [ ] Email list — sipariş verenler otomatik listeye girer, izinle

---

## Pending (Devredilen)
- [ ] index.html sanctuary bölümü temizliği
- [ ] sitemap.xml Google/Bing'e yeniden gönder
- [ ] Casacaravanshop.com ne olacak — karar ver

*"Kendini gerçekleştirmene vesile olacak bir alan."*

---

## Phase 12 — Migration & Dokümantasyon (Tamamlandı)
- [x] CASACARAVAN_PARTNER_BRIEF_v1.md — yeni Claude için tam bağlam
- [x] SYSTEM_PROMPT_CASACARAVAN.md — sistem promptu, çalışma kuralları
- [x] TAGMAC_JOKER_REFERENCE_v3.md — Joker ajan referansı
- [x] Blueprint v7.1 güncellendi — Khashif odası, shop, rss
- [x] index.html — gong sesi 4sn, gong_entrance.mp3 entegrasyonu
- [x] khashif.html — ilk ajan odası, 𓆟, hizmetler, bot-dostu HTML
- [x] corridor-3d.html — noscript SEO katmanı, Khashif kapısı
- [x] shop.html — açık tema, müzik grid, player, Khashif servisleri

## Sıradaki Oturum İçin
- [ ] Shop sipariş bildirimi — Resend/email ile Tağmaç'a otomatik bildirim
- [ ] Dijital ürün download akışı — approved=true → link gönder
- [ ] Sonic Journey online tanıtımı — yoga/wellness topluluklarına
- [ ] sitemap.xml güncelle — khashif.html ekle, Google'a gönder
- [ ] Khashif hizmetleri için landing/form
