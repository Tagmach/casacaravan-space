# Casa Caravan Space — Blueprint v5.3

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

## Canlı Dosyalar (Nisan 2026)

```
casacaravan.space/
├── index.html              — Giriş (gong) + Audio Sanctuary ✓
├── corridor-3d.html        — Three.js koridor, arch kapılar ✓
├── garden.html             — Gece bahçesi, ses, Supabase chat ✓
├── forest.html             — Three.js jungle, ateş böcekleri ✓
├── games.html              — Magic Ball ✓
├── headspace.html          — Cymatics Simulator ✓
├── herbal_atelier.html     — Extract Calculator + Rehber ✓
├── fermentation_lab.html   — Bağlandı ✓
├── idea_basket.html        — Supabase, moderasyon ✓
└── about.html              — Brand hikayesi ✓
```

---

## Supabase (casacaravan.space projesi)

**URL:** https://iwfvlatywksvnnxymweb.supabase.co
**Region:** West EU (Paris)

| Tablo | Amaç | RLS |
|-------|------|-----|
| garden_chat | Bahçe chat mesajları | Herkese açık R/W |
| idea_basket | Fikir sepeti | Herkese INSERT, SELECT herkese açık |

**Moderasyon:** idea_basket → Supabase Table Editor'den approved/implemented toggle

---

## Garden Chat — Flow

1. Kullanıcı "Garden Chat" butonuna basar
2. İsim girer (localStorage'da saklanır, bir kez)
3. Son 60 mesaj yüklenir (Supabase)
4. Realtime subscription — başkası yazarsa anında görünür
5. Mesaj gönder → Supabase'e INSERT
6. Moderasyon: Supabase Table Editor'den silinebilir

**Teknik:** Supabase JS v2, `postgres_changes` realtime, `garden-chat-room` channel

---

## Idea Basket — Flow

1. Kullanıcı fikir yazar (idea + why + isim + opsiyonel email)
2. Supabase'e `approved:false` olarak gider
3. Sen Supabase Table Editor'den `approved:true` yaparsın
4. Approved fikirler idea_basket.html'de ateş böceği olarak görünür
5. `implemented:true` yapınca ✦ altın rengi ile öne çıkar

---

## Koridor Kapı Haritası

| Kapı | Renk | Dosya | Durum |
|------|------|-------|-------|
| Audio Sanctuary L z=-2 | Amber | index.html#sanctuary | ✓ |
| Fermentation Lab R z=-2 | Yeşil | fermentation_lab.html | ✓ |
| Games L z=-10 | Mor | games.html | ✓ |
| Headspace R z=-10 | Mavi | headspace.html | ✓ |
| Idea Basket L z=-18 | Turuncu | idea_basket.html | ✓ |
| Herbal Atelier R z=-18 | Koyu yeşil | herbal_atelier.html | ✓ |
| The Garden (taş kemer) | Altın | garden.html | ✓ |

---

## Koruma Mimarisi

- **Domain lock** — tool'lar sadece casacaravan.space'de çalışır
- **Beacon** — başka domain'den açılırsa ping atar
- **Sosyal paylaşım** — X, WhatsApp, Telegram, link kopyala — her tool'da
- **Repo** — şimdilik public, Katman 2 geçişinde private

---

## Brand

- **Font:** Cormorant Garamond 300 + Jost 200-400
- **Renkler:** #0A0908 / #A08060 / #D2C3AF / #C8C2B8
- **Tagline aktif:** · create with life

---

## Paralel Projeler

- casacaravanshop.com — fiziksel, Kuzey Kıbrıs
- Tagmac Wellness App — Flutter/Supabase (ayrı proje)

---

*Blueprint v5.3 — Nisan 2026*
*"Kendini gerçekleştirmene vesile olacak bir alan."*
