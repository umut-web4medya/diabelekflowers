# -*- coding: utf-8 -*-
"""diabelekflowers.com — TEK VERİ KAYNAĞI. Fiyat/adres/telefon değişince YALNIZ burayı düzelt, build.py'yi çalıştır.

Kaynaklar (uydurma YOK):
  - Ürün adları, fiyatlar, açıklamalar: diaflowers.com (Hakikatperest/diaflowers index.html), 2026-10-13.
  - Adres + telefon: kullanıcı 2026-10-13 ("Belek, Vatan Cd. No:11 D:c, 07500 Serik/Antalya", 0534 603 21 15).
  - Harita: kullanıcının verdiği embed (GBP adı "Belek Flowers Dia").
  - "Her gün 24 saat" ve "aynı gün teslimat": diaflowers.com'da yazılı.
"""

SITE = {
    "alan": "https://diabelekflowers.com",
    "marka": "DİA Flowers Belek",
    "gbp_ad": "Belek Flowers Dia",
    "tel_goster": "0534 603 21 15",
    "tel_link": "+905346032115",
    "wa": "905346032115",
    "eposta": "info@serikdiaflowers.com",
    "adres_satir": "Belek, Vatan Cd. No:11 D:c",
    "posta": "07500",
    "ilce": "Serik",
    "il": "Antalya",
    "geo": (36.860642, 31.060966),
    "harita_embed": ("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3192.2413163143233!2d31.06096647576717"
                     "!3d36.860642264290156!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x14c3633cf203a503"
                     "%3A0xb12a54a4fdc8194a!2sBelek%20Flowers%20Dia!5e0!3m2!1str!2str!4v1791854930245!5m2!1str!2str"),
    "harita_link": "https://maps.google.com/?cid=12766109161344211274",
    "saat": "Her gün 24 saat",
}

# ✅ Sitede kullanılan iddialar (kaynağı diaflowers.com). Buraya olmayan iddia YAZMA.
ONAYLI = ["aynı gün teslimat", "her gün 24 saat", "WhatsApp'tan sipariş", "fiyatlar sitede açık"]
# ⛔ Teyitsiz — metinde geçerse denetim HATA verir.
TEYITSIZ = ["15 yıl", "yılı aşkın", "garanti", "en iyi", "en ucuz", "en hızlı", "1 numara", "lider",
            "ücretsiz teslimat", "bedava", "sigara"]

# ── KATEGORİLER (sayfa) ──────────────────────────────────────────────────────
KATEGORI = [
    {"slug": "gul-buketleri", "kapak": "21gullu1", "ad": "Gül Buketleri", "kisa": "Gül Buketi", "kisa_menu": "Gül Buketleri",
     "title": "Belek Gül Buketi — 9'dan 101 Güle Fiyatlarıyla",
     "h1": "Belek gül buketi", "ozet": "9 güllü renkli buketten 101 Rodos gülüne; her buketin fiyatı kartın üstünde."},
    {"slug": "orkide-teraryum", "kapak": "tereryum2", "ad": "Orkide ve Teraryum", "kisa": "Orkide", "kisa_menu": "Orkide & Teraryum",
     "title": "Belek Orkide ve Teraryum — Orkide 1.700 TL",
     "h1": "Belek orkide ve teraryum", "ozet": "Uzun ömürlü hediye arayanlar için ithal orkideler ve sukulent teraryumlar."},
    {"slug": "buketler", "kapak": "lisyantus1", "ad": "Karışık ve Mevsim Buketleri", "kisa": "Buket", "kisa_menu": "Buketler",
     "title": "Belek Çiçek Buketleri — Lisyantus, Krizantem, Şebboy",
     "h1": "Belek çiçek buketleri", "ozet": "Lisyantus, krizantem, şebboy, papatya ve mevsimin çiçekleriyle hazırlanan buketler."},
    {"slug": "kutuda-aranjman", "kapak": "kutudakirmiziarajman", "ad": "Kutuda Aranjmanlar", "kisa": "Kutu Aranjman", "kisa_menu": "Kutuda Aranjman",
     "title": "Belek Kutuda Çiçek Aranjmanı — Kalp Kutu 31 Gül",
     "h1": "Belek kutuda çiçek aranjmanı", "ozet": "Silindir ve kalp kutularda gül, şakayık ve karışık aranjmanlar."},
    {"slug": "hediye-ayicikli", "kapak": "kokoinali", "ad": "Ayıcıklı ve Hediyelik", "kisa": "Hediye", "kisa_menu": "Ayıcıklı & Hediye",
     "title": "Belek Ayıcıklı Buket ve Peluş Ayıcık Hediye",
     "h1": "Belek ayıcıklı buket ve hediyelik", "ozet": "Peluş ayıcıklar, ayıcıklı buketler ve çikolatalı kutular."},
    {"slug": "gelin-cicegi-arac-susleme", "kapak": "gelin1", "ad": "Gelin Çiçeği ve Araç Süsleme", "kisa": "Gelin & Araç", "kisa_menu": "Gelin & Araç Süsleme",
     "title": "Belek Gelin Çiçeği ve Gelin Arabası Süsleme",
     "h1": "Belek gelin çiçeği ve araç süsleme", "ozet": "Gelin buketleri ve düğün, nişan, sünnet için araç süsleme."},
]

# ── FİYATLI ÜRÜNLER (diaflowers.com'daki 18 ürün; fiyat BİREBİR) ─────────────
# gorsel: _src/kaynak/ içindeki dosya adları (uzantısız), ilki kapak
URUNLER = [
    {"ad": "İthal Orkideler", "fiyat": 1700, "kat": "orkide-teraryum",
     "aciklama": "Çeşitli renk ve boyutlarda ithal orkideler. Uzun ömürlü ve şık bir hediye seçeneği.",
     "gorsel": ["orkide1", "orkide2", "orkide3", "orkide4", "orkide5", "orkide6", "orkide7"]},
    {"ad": "İthal Renkli Orkide", "fiyat": 2200, "kat": "orkide-teraryum",
     "aciklama": "Özel ithal renkli orkide; uzun ömürlü, özel günler için şık bir hediye.",
     "gorsel": ["ithalrenkliorkide1", "ithalrenkliorkide2"]},
    {"ad": "Teraryum Çalışması", "fiyat": 1300, "kat": "orkide-teraryum",
     "aciklama": "Sukulentlerle hazırlanmış teraryum. Minimalist ve doğal bir dekorasyon ürünü.",
     "gorsel": ["tereryum1", "tereryum2", "tereryum3", "tereryum4", "tereryum5", "tereryum6"]},
    {"ad": "Dokuz Güllü Renkli Buket", "fiyat": 1300, "kat": "gul-buketleri",
     "aciklama": "9 adet renkli gülden oluşan canlı buket. Küçük sürprizler için.",
     "gorsel": ["dokuz"]},
    {"ad": "15 İthal Gül Buketi", "fiyat": 2300, "kat": "gul-buketleri",
     "aciklama": "15 adet ithal gülden oluşan buket.", "gorsel": ["15ithal"]},
    {"ad": "Erengül Buketi", "fiyat": 2500, "kat": "gul-buketleri",
     "aciklama": "Erengül çiçekleriyle hazırlanmış şık buket.", "gorsel": ["erengul"]},
    {"ad": "21 Güllü Buket", "fiyat": 2600, "kat": "gul-buketleri",
     "aciklama": "21 adet gülden oluşan buket.", "gorsel": ["21gullu1", "21gullu2", "21gullu3"]},
    {"ad": "51 Güllü Buket", "fiyat": 7000, "kat": "gul-buketleri",
     "aciklama": "51 adet gülden oluşan büyük buket.", "gorsel": ["51gul"]},
    {"ad": "51 Pembe Gül Buketi (60 cm)", "fiyat": 7000, "kat": "gul-buketleri",
     "aciklama": "60 cm boyunda 51 adet pembe gülden buket.", "gorsel": ["51pembe"]},
    {"ad": "101 Gül Buketi", "fiyat": 8600, "kat": "gul-buketleri",
     "aciklama": "101 adet gülden oluşan görkemli buket.", "gorsel": ["101gul"]},
    {"ad": "101 Rodos Gül Buketi (60 cm)", "fiyat": 8600, "kat": "gul-buketleri",
     "aciklama": "60 cm boyunda 101 adet Rodos gülünden buket.", "gorsel": ["rodos1"]},
    {"ad": "Karışık Krizantem Buketi", "fiyat": 1300, "kat": "buketler",
     "aciklama": "Orta boy, ithal ve yerli karışık krizantem (kasımpatı) buketi.",
     "gorsel": ["ithalyerli1", "ithalyerli2", "ithalyerli3"]},
    {"ad": "Lisyantus Orta Boy Renkli Buket", "fiyat": 1800, "kat": "buketler",
     "aciklama": "Orta boy, renkli lisyantus buketi; pastel renkli ve zarif.",
     "gorsel": ["lisyantus1", "lisyantus2", "lisyantus3"]},
    {"ad": "Kalp Kutu 31 Güllü Aranjman", "fiyat": 4000, "kat": "kutuda-aranjman",
     "aciklama": "Kalp şeklinde kutuda 31 adet gülden aranjman.", "gorsel": ["kalp1"]},
    {"ad": "Kokinalı Ayıcıklı Buket", "fiyat": 3200, "kat": "hediye-ayicikli",
     "aciklama": "Kokina ve peluş ayıcıkla hazırlanmış buket.", "gorsel": ["kokoinali"]},
    {"ad": "Büyük Boy Peluş Ayıcık", "fiyat": 3500, "kat": "hediye-ayicikli",
     "aciklama": "Büyük boy peluş ayıcık.", "gorsel": ["ayicik"]},
    {"ad": "Büyük Boy Peluş Ayıcık (Lisanslı)", "fiyat": 2600, "kat": "hediye-ayicikli",
     "aciklama": "Lisanslı, büyük boy peluş ayıcık.", "gorsel": ["ayicik2"]},
    {"ad": "Araç Süsleme", "fiyat": 3000, "fiyat_on": True, "kat": "gelin-cicegi-arac-susleme",
     "aciklama": "Düğün, nişan, sünnet ve özel günler için araç süsleme.",
     "gorsel": ["araba1", "araba2", "araba3"]},
]

# ── FİYATSIZ GALERİ (diaflowers deposunda olup sitede gösterilmeyen gerçek fotoğraflar) ──
# Fiyat yok → kartta "Fiyatı WhatsApp'tan sorun". ⛔ sigara.jpeg BİLEREK alınmadı (tütün; Ads politikası).
GALERI = {
    "buketler": [("ithalbuket", "Ortanca ve gül buketi"), ("ithalorta", "Lila güllü buket"),
                 ("ithalorta1", "Pastel karışık buket"), ("karisikithal1", "İthal karışık buket"),
                 ("kelebek1", "Kelebek ambalajlı buket"), ("kelebek2", "Kelebek ambalajlı buket"),
                 ("kelebek3", "Lisyantus kelebek buket"), ("kelebek4", "Kelebek ambalajlı buket"),
                 ("mevsimcicekleri1", "Gerbera ve krizantem buketi"), ("mevsimcicekleri2", "Mevsim çiçekleri buketi"),
                 ("mevsimcicekleri3", "Mor krizantem buketi"), ("mevsimcicekleri4", "Mevsim çiçekleri buketi"),
                 ("mevsimcicekleri5", "Mevsim çiçekleri buketi"), ("mevsimcicekleri6", "Mevsim çiçekleri buketi"),
                 ("mevsimcicekleri7", "Mevsim çiçekleri buketi"), ("mevsimcicekleri8", "Mevsim çiçekleri buketi"),
                 ("papatya", "Papatya buketi"), ("sebboy2", "Şebboy buketi"), ("sebboy3", "Şebboy buketi"),
                 ("sebboy4", "Şebboy buketi"), ("ithalaranjman1", "Çanta içinde krizantem"),
                 ("ithalaranjman2", "Çanta içinde aranjman"), ("ithalaranjman3", "Çanta içinde aranjman"),
                 ("yapay1", "Solmayan (yapay) gül buketi"), ("yapay5", "Solmayan (yapay) buket")],
    "kutuda-aranjman": [("kutudakirmiziarajman", "Siyah kutuda kırmızı güller"), ("kutudaarajman1", "Kutuda gül ve lisyantus"),
                        ("kutudaarajman2", "Kutuda aranjman"), ("kutudaarajman3", "Kutuda aranjman"),
                        ("ortakutu1", "Pembe kutuda gerbera ve karanfil"), ("orta2", "Kutuda yeşil karanfil"),
                        ("orta3", "Kutuda aranjman"), ("orta4", "Kutuda aranjman"),
                        ("sakayik2", "Pembe kutuda şakayık güller"), ("sakayim1", "Siyah kutuda şakayık güller"),
                        ("sakayik3", "Şakayık aranjman"), ("sakayikorta1", "Şakayık aranjman"),
                        ("ozel1", "Sepette pembe güller")],
    "hediye-ayicikli": [("ayicikli1", "Ayıcıklı buket"), ("ayicikli2", "Ayıcıklı buket"),
                        ("ayicikli3", "Ayıcıklı kırmızı güller"), ("ayicikli4", "Ayıcıklı buket"),
                        ("ayicikli5", "Ayıcıklı buket"), ("cikolata1", "Çikolata ve şekerleme kutusu"),
                        ("yapayarajman1", "Kırmızı ayıcıklı aranjman")],
    "gelin-cicegi-arac-susleme": [("gelin1", "Pembe güllü gelin buketi"), ("gelin2", "Gelin buketi"),
                                  ("gelin3", "Gelin buketi"), ("gelin4", "Gelin buketi"), ("gelin5", "Gelin buketi")],
}
MAGAZA = [("magaza", "DİA Flowers Belek mağazası, akşam"), ("dukkan1", "DİA Flowers mağaza vitrini"),
          ("dukkan2", "DİA Flowers mağaza önü")]

# ── BÖLGELER (sayfa) ─────────────────────────────────────────────────────────
# ⚠️ Doğakent sitenin eski teslimat listesinde YOKTU; kullanıcı Ads'te istedi (2026-10-12). Coğrafi detay
#    YAZILMADI — teyit gelince "konum" alanı doldurulur.
BOLGELER = [
    {"slug": "belek-cicekci", "ad": "Belek", "ana": True,
     "konum": "Mağazamız Belek'te, Vatan Caddesi üzerinde.",
     "one_cikan": ["101 Rodos Gül Buketi (60 cm)", "İthal Orkideler", "Kalp Kutu 31 Güllü Aranjman", "21 Güllü Buket"]},
    {"slug": "kadriye-cicekci", "ad": "Kadriye", "ana": False,
     "konum": "Kadriye, Belek'in batısında; siparişler Belek'teki mağazamızdan hazırlanıp yola çıkar.",
     "one_cikan": ["21 Güllü Buket", "İthal Renkli Orkide", "Lisyantus Orta Boy Renkli Buket", "Kokinalı Ayıcıklı Buket"]},
    {"slug": "dogakent-cicekci", "ad": "Doğakent", "ana": False,
     "konum": "Doğakent'e siparişler Belek'teki mağazamızdan hazırlanıp gönderilir.",
     "one_cikan": ["Dokuz Güllü Renkli Buket", "15 İthal Gül Buketi", "Teraryum Çalışması", "İthal Orkideler"]},
    {"slug": "serik-cicekci", "ad": "Serik", "ana": False,
     "konum": "Serik merkez ve mahallelerine siparişler Belek'teki mağazamızdan çıkar.",
     "one_cikan": ["51 Güllü Buket", "Karışık Krizantem Buketi", "Kalp Kutu 31 Güllü Aranjman", "Büyük Boy Peluş Ayıcık"]},
    {"slug": "bogazkent-cicekci", "ad": "Boğazkent", "ana": False,
     "konum": "Boğazkent, Belek'in doğusunda; siparişler Belek'teki mağazamızdan yola çıkar.",
     "one_cikan": ["Erengül Buketi", "İthal Orkideler", "21 Güllü Buket", "Teraryum Çalışması"]},
]

# ── SSS (anasayfa; FAQPage şeması bundan üretilir) ───────────────────────────
SSS = [
    ("Aynı gün teslimat yapıyor musunuz?",
     "Evet. Belek, Kadriye, Doğakent, Serik ve Boğazkent'e aynı gün teslimat yapıyoruz. Siparişin saatini "
     "WhatsApp'tan yazdığınızda teslim saatini size söylüyoruz."),
    ("Nasıl sipariş veririm?",
     "Beğendiğiniz ürünün altındaki WhatsApp düğmesine basın; ürün adı mesaja kendiliğinden yazılır. "
     "Teslimat adresini, alıcının adını ve kart notunu ekleyin. İsterseniz 0534 603 21 15'i de arayabilirsiniz."),
    ("Fiyatlar güncel mi?",
     "Sitedeki fiyatlar mağazadaki fiyatlarla aynıdır. Fiyatı yazmayan ürünler ve özel tasarımlar için "
     "WhatsApp'tan fotoğrafla fiyat sorabilirsiniz."),
    ("Mağazaya gelip kendim alabilir miyim?",
     "Evet. Mağazamız Belek, Vatan Caddesi No:11'de. Her gün 24 saat açığız."),
    ("Otel veya tatil köyüne teslim ediyor musunuz?",
     "Teslimat adresi olarak otel adını ve oda/misafir adını yazmanız yeterli; teslim koşullarını "
     "siparişte birlikte netleştiriyoruz."),
]

# ── Anasayfa yuvarlak kategori balonları (görsel, etiket, hedef sayfa#çapa) ──
BALON = [("101gul", "Güller", "gul-buketleri/"), ("21gullu1", "Gül Buketleri", "gul-buketleri/"),
         ("orkide2", "Orkide", "orkide-teraryum/"), ("tereryum1", "Teraryum", "orkide-teraryum/"),
         ("lisyantus1", "Lisyantus", "buketler/"), ("mevsimcicekleri1", "Mevsim Çiçekleri", "buketler/"),
         ("papatya", "Papatya", "buketler/"), ("kutudakirmiziarajman", "Kutuda Güller", "kutuda-aranjman/"),
         ("sakayim1", "Şakayık", "kutuda-aranjman/"), ("kokoinali", "Ayıcıklı", "hediye-ayicikli/"),
         ("cikolata1", "Çikolata", "hediye-ayicikli/"), ("gelin1", "Gelin Çiçeği", "gelin-cicegi-arac-susleme/"),
         ("araba1", "Araç Süsleme", "gelin-cicegi-arac-susleme/")]

# ── Anasayfa bannerları: (renk sınıfı, üst etiket, başlık, alt metin, görsel, hedef) — fiyatlar URUNLER ile tutarlı
BANNER_BUYUK = [
    ("pembe", "Güller", "Gül Buketleri", "9 gülden 101 güle · 1.300 TL'den", "101gul", "gul-buketleri/"),
    ("ada", "Uzun ömürlü hediye", "Orkide ve Teraryum", "İthal orkide 1.700 TL · teraryum 1.300 TL", "tereryum2", "orkide-teraryum/"),
]
BANNER_KUCUK = [
    ("lila", "Yıldönümü", "Kutuda Güller", "Kalp kutuda 31 gül 4.000 TL", "kalp1", "kutuda-aranjman/"),
    ("sari", "Doğum Günü", "Mevsim Buketleri", "Lisyantus, krizantem, papatya", "mevsimcicekleri2", "buketler/"),
    ("mavi", "Düğün · Nişan", "Gelin Çiçeği", "Gelin buketi ve araç süsleme", "gelin1", "gelin-cicegi-arac-susleme/"),
]
