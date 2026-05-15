# Casa Caravan Space — Checklist

> casacaravan.space · GitHub: Tagmach/casacaravan-space
> Last updated: 15 May 2026

---

## Phase 1 — Foundation ✓
- [x] Domain, GitHub Pages, HTTPS
- [x] Entrance — gong, animasyon, ses (gong_entrance.mp3, 4sn)
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
- [x] Shop kapısı — kırmızı, L z=-2 → shop.html
- [x] Khashif kapısı — mavi/petrol, R z=-2 → khashif.html
- [x] noscript SEO katmanı eklendi

---

## Phase 3 — Odalar ✓
- [x] audio_sanctuary.html — stüdyo, EQ, kayıt
- [x] headspace.html — Cymatics Simulator
- [x] fermentation_lab.html — tarif hesaplayıcı
- [x] herbal_atelier.html — extract calculator + rehber
- [x] garden.html — bahçe, chat, radyo, ay fazı, star observatory, rünik işaretler
- [x] forest.html — Three.js jungle, S-curve yol ayrımı, kırmızı ağaç
- [x] observatory.html — yıldız kubbesi, takımyıldızları, zodiac
- [x] Audio Sanctuary sub-choice — Recording Room + Cymatics Tool overlay
- [x] khashif.html — ilk ajan odası, 𓆟, hizmetler, bot-dostu HTML, Schema.org

---

## Phase 4 — Supabase ✓
- [x] garden_chat — Realtime chat
- [x] idea_basket — moderasyon
- [x] page_visits — analytics
- [x] players — ARG oyuncuları (ARG kaldırıldı, tablo korundu)
- [x] orders — shop siparişleri (approved, download_url alanları hazır)

---

## Phase 5 — The Keys ARG (Kaldırıldı / Askıya Alındı)
- ARG mekaniği temizlendi — keys.js, tüm firefly'lar, Key VII kapısı kaldırıldı
- Kapı pozisyonları korundu, içerikler değişti

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

## Phase 8 — Shop ✓ (Aktif)

### Tamamlanan
- [x] shop.html — açık tema (#F5F0E8), Casa Caravan ruhu
- [x] Ürünler: Sonic Journey (bireysel/duo/online), Ukiyo Butter, Coconut Butter, Sourdough Starter
- [x] Dijital grid — gong/nefes/müzik kayıtları €1/adet, 12 parça
- [x] Müzik player — mini player, Supabase Storage'dan stream
- [x] Sepet sistemi — add/remove, fiziksel/dijital ayrımı
- [x] Sipariş formu — isim, email, telefon, adres (fiziksel için)
- [x] Ödeme detayları açık gösterim — her yöntemi seçince detaylar açılıyor
- [x] TR IBAN: TR20 0006 4000 0016 8130 0605 15
- [x] Revolut IBAN: LT62 3250 0984 5562 5476 · BIC: REVOLT21
- [x] ETH cüzdan: 0xeE9cc0F4dDeBffb701b6F43EEDaAb2bdD11C1894 (Phantom, ERC-20)
- [x] Copy butonları — IBAN, BIC, ETH adresi kopyalanabilir
- [x] EUR/TRY canlı kur — Frankfurter API
- [x] Supabase orders tablosu entegrasyonu
- [x] Resend sipariş bildirimi — sipariş gelince tagmacc@gmail.com'a email
- [x] Khashif hizmetleri bölümü eklendi
- [x] corridor-3d.html → shop.html bağlantısı

### Yapılacak — Shop
- [ ] ETH/Phantom web extension doğrudan bağlantı (window.ethereum inject)
- [ ] Resend domain doğrulandıktan sonra from: `shop@casacaravan.space` güncelle
- [ ] Sipariş bildirimi alıcısı: tagmacc@gmail.com ✓ (shop.html'de mevcut)
- [ ] Admin panel — orders tablosunu görüp approved yapabileceğin basit arayüz
- [ ] Dijital ürün onayı — approved=true olunca kullanıcıya download linki gönder
- [ ] Supabase Storage — dijital dosyaları yükle (gong kayıtları, müzik, nefes)
- [ ] Signed URL sistemi — satın alınan dosya için zamanlı indirme linki
- [ ] El yapımı taş/kerpiç fırın ürün olarak ekle
- [ ] Ürün görselleri — her ürün için fotoğraf
- [ ] Casacaravanshop.com → casacaravan.space/shop yönlendirmesi veya merge kararı

---

## Phase 9 — Email & Domain Altyapısı (Aktif)

### Tamamlanan
- [x] Resend hesabı kuruldu — API key: `re_8Yrdyxjr_HQxxkfZ8t1FsVMYCgNsW34ag`
- [x] Resend'de casacaravan.space domain eklendi
- [x] Namecheap Advanced DNS'e 4 kayıt eklendi:
  - TXT `resend._domainkey` — DKIM
  - MX `send` → feedback-smtp.eu-west-1.amazonses.com (priority 10)
  - TXT `send` — SPF
  - TXT `_dmarc` — DMARC
- [x] Resend bildirim entegrasyonu shop.html'de aktif

### Yapılacak — Email
- [ ] Resend DNS doğrulaması tamamlandı mı? → Resend dashboard'dan kontrol et
- [ ] DNS verify olduktan sonra shop.html'de from adresini güncelle:
  `from: 'Casa Caravan Shop <shop@casacaravan.space>'`
- [ ] Test siparişi ver, email'in tagmacc@gmail.com'a geldiğini doğrula

---

## Phase 10 — RSS & Sitemap (Tamamlandı — Aksiyon Gerekli)

### Tamamlanan
- [x] rss.xml — çift kanal hatası giderildi, tek temiz XML
- [x] rss.xml — Khashif item eklendi, 8 item
- [x] sitemap.xml — 13 URL, shop/khashif/about/rss eklendi

### Yapılacak — SEO Aksiyon
- [ ] **Google Search Console'a git → sitemap.xml yeniden gönder**
  URL: `https://casacaravan.space/sitemap.xml`
- [ ] **Bing Webmaster'a git → sitemap.xml yeniden gönder**
- [ ] RSS feed kategorileri için /feeds/ dizini oluştur (oda bazlı feed'ler)
- [ ] Ay fazı güncellemeleri — her yeni ay, dolunay, çeyrek için RSS item
- [ ] Sonic Journey session notları — Çarşamba sonrası kısa gözlem
- [ ] Structured data — Schema.org Review (9 yorum işaretle)

---

## Phase 11 — İçerik & Büyüme (Yapılacak)

### Organik
- [ ] Hacker News — Show HN: "I built a 3D corridor with rooms for fermentation, sound, and herbalism"
- [ ] Reddit: r/InternetIsBeautiful, r/cymatics, r/fermentation, r/herbalism, r/sourdough
- [ ] Product Hunt — koridor + about manifesto ile lansman
- [ ] Mastodon — RSS otomatik besleme
- [ ] Substack — About manifestosundan ilk yazı

### SEO
- [ ] /notes/ dizini — düzenli içerik
- [ ] Backlink hedefleri — fermentasyon, sound therapy, Cyprus blogs

### Topluluk
- [ ] Garden Chat'i tanıt — ziyaretçileri oraya yönlendir
- [ ] Sonic Journey booking — WhatsApp yerine casacaravan.space üzerinden form
- [ ] Email list — sipariş verenler otomatik listeye girer, izinle

---

## Phase 12 — Ajanlar & Otomasyon (Yapılacak)

### Khashif Sistemi
- [x] khashif.html — aktif, korridor'da açık
- [ ] ETH/Phantom web extension bağlantısı (window.ethereum)
- [ ] agents.html — ajan hub (şu an XML tabanlı ajan iletişim formatı)
- [ ] Khashif hizmetleri için ayrı form/landing

### Jakelu — Dağıtım Zekası
- [ ] Jakelu blueprint ve checklist entegrasyon
- [ ] Platform profilleri — Instagram, Mastodon, Reddit, HN
- [ ] RSS → Jakelu pipeline

### Tagmac Wellness App
- [ ] Blueprint v5 hazır — FlutterFlow geliştirme devam
- [ ] Nefes-bağlantılı dinamik adaptasyon (breath-sync) — Session ekranı
- [ ] App → casacaravan.space/shop bağlantısı

---

## Phase 13 — Migration & Dokümantasyon ✓
- [x] CASACARAVAN_PARTNER_BRIEF_v1.md
- [x] CASACARAVAN_SPACE_BLUEPRINT_v8.md — bu dosya
- [x] CHECKLIST.md — bu dosya
- [x] Google Drive sync aktif — casacaravan.space klasörü
- [x] GitHub Integration — Claude Chat'ten dosya attach edilebiliyor

---

## Sıradaki Oturum İçin

**Acil (DNS verify sonrası):**
- [ ] Resend verify → shop.html from adresi güncelle
- [ ] Google Search Console + Bing'e sitemap gönder
- [ ] ETH/Phantom web extension bağlantısı ekle

**Orta vadeli:**
- [ ] Dijital ürün download akışı — approved=true → link gönder
- [ ] Admin panel — sipariş onaylama arayüzü
- [ ] Sonic Journey online tanıtımı — yoga/wellness topluluklarına

---

## Pending Kararlar
- [ ] Casacaravanshop.com ne olacak — merge mi, redirect mi?
- [ ] index.html sanctuary bölümü temizliği

*"Kendini gerçekleştirmene vesile olacak bir alan."*
