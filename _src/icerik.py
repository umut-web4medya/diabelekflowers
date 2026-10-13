# -*- coding: utf-8 -*-
"""Sayfa gövde metinleri — işletme sahibinin ağzından (kullanıcı 2026-10-13: "benim gibi davranarak").
Yapı: sayfa anahtarı → [(h2, [paragraf, ...], işaret)]. İşaret: None | "urunler" (öne çıkan kartlar)
| "fiyat" (fiyat tablosu, data.py'den) | "adim" (sipariş adımları) | "magaza".
⛔ Rakamlı süre / teslim ücreti / "fotoğrafını atarız" gibi teyitsiz söz YOK — teyit gelince eklenir.
Ekler elle yazıldı (Belek'e, Kadriye'ye, Serik'te…); şablonla üretme, Türkçe ek bozulur.
"""
TEL = "0534 603 21 15"

TESLIM_ORTAK = [
    "Siparişiniz bize ulaştığı anda çiçeğinizi Belek'teki mağazamızda hazırlamaya başlıyoruz. Buketi "
    "sizin seçtiğiniz ürüne göre hazırlıyor, kart notunuzu ekliyoruz.",
    "Teslim saatini sipariş sırasında birlikte konuşuyoruz. \"Sabah ilk iş kapıda olsun\" ya da \"akşam eve "
    "geldiğinde sürpriz olsun\" diyorsanız ona göre planlıyoruz. Aynı gün teslimat yapıyoruz ama net saati "
    "telefonda söylemek en doğrusu, çünkü yoğun günlerde (14 Şubat, Anneler Günü gibi) sıra uzayabiliyor.. "
    "Bunu baştan dürüstçe söylüyoruz :)",
    "Çiçek yola çıkmadan önce adresi ve alıcının telefonunu bir kez daha kontrol ediyoruz. Alıcıya "
    "ulaşamadığımız bir durum olursa sizi arıyoruz; çiçeği kapıya bırakıp gitmiyoruz.",
]

SAYFA = {
# ─────────────────────────────── ANASAYFA = BELEK ───────────────────────────────
"": [
    ("Belek Çiçekçi Numarası: " + TEL, [
        "Belek'te çiçek göndermek istiyorsanız en kısa yol bizi aramak ya da WhatsApp'tan yazmak. Numaramız "
        f"<a href=\"tel:+905346032115\">{TEL}</a>; telefon da WhatsApp da aynı hatta, her gün 24 saat açık.",
        "WhatsApp'tan yazarsanız ürünün fotoğrafını, adresi ve kart notunu tek mesajda gönderebilirsiniz. "
        "Sitedeki her ürünün altındaki <em>Sipariş ver</em> düğmesi mesaja ürün adını kendisi "
        "yazıyor; size sadece adresi eklemek kalıyor.",
    ], None),
    ("Belek En Yakın Çiçekçi", [
        "Mağazamız Belek'in içinde, Vatan Caddesi No:11'de. Belek'te bir otelde, sitede ya da evde "
        "olun; çiçeğiniz başka bir şehirden ya da ilçeden yola çıkmıyor, buradan çıkıyor. "
        "En yakın çiçekçiyi arıyorsanız aradığınız yer burası :)",
        "İsterseniz mağazaya gelip çiçeği kendiniz de seçebilirsiniz. Vitrindeki çiçekleri görüp "
        "\"şunu biraz daha büyük yapalım\" demek bazen fotoğraftan seçmekten çok daha kolay.",
    ], "magaza"),
    ("Belek Çiçek Sipariş Ver", [
        "Sipariş vermek için üç bilgi yeterli: hangi çiçek, kime ve nereye. Gerisini biz soruyoruz.",
    ], "adim"),
    ("Belek'e Çiçek Teslimatı Nasıl Yapılıyor?", TESLIM_ORTAK + [
        "Belek'te otellere de çiçek gönderiliyor. Bu durumda otelin adını, misafirin adını ve "
        "biliyorsanız oda numarasını yazmanız yeterli; teslimi siparişte birlikte netleştiriyoruz.",
    ], None),
    ("Belek Çiçek Fiyatları", [
        "Buketlerimiz 1.300 TL'den başlayan fiyatlarla. Aşağıdaki tabloda her kategorinin başlangıç "
        "fiyatı var; beğendiğiniz ürünün fiyatını WhatsApp'tan ya da telefonla hemen söylüyoruz.",
    ], "fiyat"),
],
# ─────────────────────────────── KADRİYE ───────────────────────────────
"kadriye-cicekci": [
    ("Kadriye Çiçekçi Numarası: " + TEL, [
        "Kadriye'ye çiçek göndermek için bizi arayabilir ya da WhatsApp'tan yazabilirsiniz: "
        f"<a href=\"tel:+905346032115\">{TEL}</a>. Telefon ve WhatsApp aynı numara, her gün 24 saat açık.",
        "Kadriye'de tatildeyseniz ve otelden arıyorsanız da sorun değil; otelin adını söylemeniz yeterli.",
    ], None),
    ("Kadriye En Yakın Çiçekçi", [
        "Kadriye'nin hemen yanındaki Belek'teyiz. Mağazamız Belek Vatan Caddesi'nde; Kadriye'ye giden "
        "çiçekler buradan hazırlanıp yola çıkıyor. Yani \"Kadriye'ye en yakın çiçekçi\" diye "
        "arıyorsanız komşunuzuz :)",
        "Kadriye otellerin ve yazlık sitelerin olduğu bir bölge; tatildeki birine yıldönümü ya da doğum günü "
        "sürprizi yapmak isteyenler için aşağıda dört ürün önerdik.",
    ], "urunler"),
    ("Kadriye Çiçek Sipariş Ver", [
        "Ürünün altındaki WhatsApp düğmesine bastığınızda mesaja ürün adı ve Kadriye bilgisi "
        "kendiliğinden yazılıyor. Siz alıcının adını, adresini ve kartta yazmasını istediğiniz notu ekleyin.",
    ], "adim"),
    ("Kadriye'ye Çiçek Teslimatı Nasıl Yapılıyor?", TESLIM_ORTAK + [
        "Kadriye'de site ya da otel adresine gönderiyorsanız blok, kapı numarası veya oda numarasını "
        "eklemeyi unutmayın; büyük sitelerde doğru kapıyı bulmak en çok zaman alan kısım oluyor.",
    ], None),
    ("Kadriye Çiçek Fiyatları", [
        "Kadriye'ye gönderilen çiçeklerin fiyatı mağazadaki fiyatla aynı. Başlangıç fiyatları aşağıda; "
        "kategoriye tıklayınca tüm ürünleri görürsünüz.",
    ], "fiyat"),
],
# ─────────────────────────────── DOĞAKENT ───────────────────────────────
"dogakent-cicekci": [
    ("Doğakent Çiçekçi Numarası: " + TEL, [
        f"Doğakent'e çiçek siparişi için numaramız <a href=\"tel:+905346032115\">{TEL}</a>. "
        "Arayabilir ya da WhatsApp'tan yazabilirsiniz; her gün 24 saat açığız.",
        "Gece geç saatte aklınıza geldiyse de yazın. Siparişi alıp teslim saatini sizinle konuşuyoruz.",
    ], None),
    ("Doğakent En Yakın Çiçekçi", [
        "Doğakent'e giden çiçekler Belek'teki mağazamızdan hazırlanıyor. Mağazamız Belek Vatan "
        "Caddesi'nde; adres ve yol tarifi bu sayfanın altında.",
        "\"Bir sürpriz yapayım ama abartmayayım\" diyenler için 9 güllü renkli buket ve 15 ithal gül buketi iyi bir başlangıç. "
        "Uzun süre kalsın istiyorsanız teraryum ya da orkide öneriyoruz.",
    ], "urunler"),
    ("Doğakent Çiçek Sipariş Ver", [
        "Ürünü seçin, WhatsApp düğmesine basın, adres ve kart notunu yazın. Mesajda ürün adı ve "
        "Doğakent bilgisi zaten yazılı geliyor.",
    ], "adim"),
    ("Doğakent'e Çiçek Teslimatı Nasıl Yapılıyor?", TESLIM_ORTAK, None),
    ("Doğakent Çiçek Fiyatları", [
        "Doğakent'e gönderdiğimiz çiçeklerin fiyatı sitedeki fiyatla aynı; aşağıda her kategorinin "
        "başlangıç fiyatını görebilirsiniz.",
    ], "fiyat"),
],
# ─────────────────────────────── SERİK ───────────────────────────────
"serik-cicekci": [
    ("Serik Çiçekçi Numarası: " + TEL, [
        f"Serik'e çiçek göndermek için <a href=\"tel:+905346032115\">{TEL}</a> numarasını arayın ya da "
        "WhatsApp'tan yazın. Aynı hat, her gün 24 saat.",
        "Daha önce \"Serik DİA Flowers\" adıyla bizden çiçek aldıysanız doğru yerdesiniz; aynı mağaza, "
        "aynı ekip, aynı numara.",
    ], None),
    ("Serik En Yakın Çiçekçi", [
        "Mağazamız Serik ilçesine bağlı Belek'te, Vatan Caddesi No:11'de. Serik merkeze ve mahallelerine "
        "giden çiçekler buradan hazırlanıp yola çıkıyor.",
        "Doğum günü, nişan, söz ya da yıldönümü için 51 güllü buketi ve "
        "kalp kutuda 31 gülü öneriyoruz; daha sade bir şey istiyorsanız krizantem "
        "buketini öneriyoruz.",
    ], "urunler"),
    ("Serik Çiçek Sipariş Ver", [
        "Siparişi WhatsApp'tan vermek en pratik yol: ürünün altındaki düğmeye basın, mesaj ürün adı ve "
        "Serik bilgisiyle açılsın. Adres, alıcı adı ve kart notunu ekleyip gönderin.",
    ], "adim"),
    ("Serik'e Çiçek Teslimatı Nasıl Yapılıyor?", TESLIM_ORTAK + [
        "Serik'te mahalle ve sokak adını yazarken bir de tarif eklerseniz (\"camiinin karşısı\" gibi) "
        "çiçek daha hızlı bulur, bunu deneyimle söylüyoruz :)",
    ], None),
    ("Serik Çiçek Fiyatları", [
        "Serik'e gönderilen çiçeklerin fiyatı mağaza fiyatıyla aynı. Kategorilerin başlangıç fiyatları aşağıda.",
    ], "fiyat"),
],
# ─────────────────────────────── BOĞAZKENT ───────────────────────────────
"bogazkent-cicekci": [
    ("Boğazkent Çiçekçi Numarası: " + TEL, [
        f"Boğazkent'e çiçek siparişi için <a href=\"tel:+905346032115\">{TEL}</a> numarasını arayabilir ya "
        "da WhatsApp'tan yazabilirsiniz. Her gün 24 saat açığız.",
    ], None),
    ("Boğazkent En Yakın Çiçekçi", [
        "Boğazkent, Belek'in doğusunda; tatil köylerinin ve otellerin olduğu bir bölge. Boğazkent'e giden "
        "çiçekler Belek Vatan Caddesi'ndeki mağazamızdan hazırlanıp yola çıkıyor.",
        "Tatildeki birine sürpriz yapmak istiyorsanız erengül buketi ya da orkide iyi gider; orkide otel "
        "odasında da uzun süre güzel kalır. Aşağıda Boğazkent için önerdiğimiz ürünler var.",
    ], "urunler"),
    ("Boğazkent Çiçek Sipariş Ver", [
        "Ürünün altındaki WhatsApp düğmesine basın; mesaja ürün adı ve Boğazkent bilgisi yazılı gelir. "
        "Otelin ya da sitenin adını, alıcının adını ve kart notunu ekleyin.",
    ], "adim"),
    ("Boğazkent'e Çiçek Teslimatı Nasıl Yapılıyor?", TESLIM_ORTAK + [
        "Otele gönderiyorsanız otelin adını, misafirin adını ve biliyorsanız oda numarasını yazın; "
        "teslimi siparişte birlikte netleştiriyoruz.",
    ], None),
    ("Boğazkent Çiçek Fiyatları", [
        "Boğazkent'e gönderdiğimiz çiçeklerin fiyatı sitedeki fiyatla aynı. Başlangıç fiyatları aşağıda.",
    ], "fiyat"),
],
}

# Kategori sayfalarında teslimat kısa; uzun anlatım anasayfa + bölge sayfalarında (aynı 3 paragraf 10 sayfada tekrar etmesin)
TESLIM_KISA = [
    "Siparişiniz gelince çiçeği Belek'teki mağazamızda hazırlıyor, kart notunuzu ekleyip aynı gün yola "
    "çıkarıyoruz. Teslim saatini sipariş sırasında birlikte konuşuyoruz; yoğun günlerde (14 Şubat, Anneler "
    "Günü) sıra uzayabildiği için net saati telefonda söylüyoruz.",
    "Teslimatın adım adım nasıl yapıldığını <a href=\"../#teslimat\">anasayfada</a> anlattık.",
]

# ── KATEGORİ SAYFALARI ── (urunler işareti: o kategorinin fiyatlı kartları)
KATEGORI = {
"gul-buketleri": [
    ("Belek Gül Buketi Fiyatları", [
        "Gül buketlerimiz 1.300 TL'den başlayan fiyatlarla; 9 güllü buketten 101 güllü bukete kadar "
        "seçenek var. Beğendiğiniz buketin fiyatını WhatsApp'tan hemen yazıyoruz.",
    ], "urunler"),
    ("Kaç Gül Göndermeli?", [
        "Küçük bir \"seni düşündüm\" için 9 gül yeter. 15 ve 21 gül doğum günü "
        "ve yıldönümü için uygun boy. 51 ve 101 gül ise söz, nişan, evlilik teklifi gibi \"bu gün "
        "unutulmasın\" denilen anlar için; 60 cm boylu Rodos ve pembe gül seçeneklerimiz de bu grupta.",
        "Bütçeyi aşmadan etkili bir şey istiyorsanız 21 güllü buket iyi bir orta nokta.",
    ], None),
    ("Belek Gül Buketi Sipariş Ver", [
        f"Buketi seçip altındaki WhatsApp düğmesine basın ya da {TEL} numarasını arayın. "
        "Belek, Kadriye, Doğakent, Serik ve Boğazkent'e aynı gün gönderiyoruz.",
    ], "adim"),
    ("Gül Buketi Teslimatı Nasıl Yapılıyor?", TESLIM_KISA, None),
],
"orkide-teraryum": [
    ("Belek Orkide Fiyatları", [
        "Orkide ve teraryumlarımız 1.300 TL'den başlayan fiyatlarla. Beğendiğiniz ürünün fiyatını "
        "WhatsApp'tan hemen yazıyoruz.",
    ], "urunler"),
    ("Orkide mi Buket mi?", [
        "Kesme çiçek birkaç gün güzel kalır; orkide ise doğru yerde haftalarca çiçekte kalabilir. Bu yüzden "
        "\"uzun süre dursun\" diyen, ofise ya da yeni eve hediye gönderen müşterilerimize orkide öneriyoruz.",
        "Orkideye bakmak zor değil: doğrudan güneş almayan aydınlık bir köşe ve haftada bir kez, saksının "
        "altından süzülecek kadar su. Teraryum ise daha da az ilgi ister; sukulentler az suyla yaşar.",
    ], None),
    ("Belek Orkide Sipariş Ver", [
        f"Orkideyi seçip WhatsApp'tan yazın ya da {TEL} numarasını arayın; aynı gün gönderiyoruz.",
    ], "adim"),
    ("Orkide Teslimatı Nasıl Yapılıyor?", TESLIM_KISA, None),
],
"buketler": [
    ("Belek Çiçek Buketi Fiyatları", [
        "Buketlerimiz 1.300 TL'den başlayan fiyatlarla. Mevsime göre değişen çiçeklerle hazırlandıkları "
        "için fiyatlarını WhatsApp'tan söylüyoruz.",
    ], "urunler"),
    ("Mevsim Çiçeklerinde Fiyat Neden Değişiyor?", [
        "Şebboy, şakayık, papatya ve lisyantus gibi çiçeklerin fiyatı mevsime ve o hafta gelen çiçeğe göre "
        "değişiyor. Bu yüzden bu buketlere sabit fiyat yazmıyoruz; fotoğrafın altındaki düğmeyle sorduğunuzda "
        "o günün fiyatını söylüyoruz. Bütçenizi söylerseniz ona göre de hazırlarız.",
    ], None),
    ("Belek Buket Sipariş Ver", [
        f"Beğendiğiniz buketin fotoğrafını WhatsApp'tan gönderin ya da {TEL} numarasını arayın.",
    ], "adim"),
    ("Buket Teslimatı Nasıl Yapılıyor?", TESLIM_KISA, None),
],
"kutuda-aranjman": [
    ("Belek Kutuda Aranjman Fiyatları", [
        "Kutuda aranjmanlarımız 4.000 TL'den başlayan fiyatlarla. Kalp ve silindir kutudaki gül, şakayık "
        "ve karışık aranjmanların fiyatını çiçeğe göre WhatsApp'tan söylüyoruz.",
    ], "urunler"),
    ("Kutuda Aranjman mı Buket mi?", [
        "Kutuda aranjmanın en büyük artısı vazo istememesi: çiçek ıslak köpükte durduğu için alıcının "
        "uğraşmasına gerek kalmıyor. Ofise, hastane ziyaretine ya da vazosu olmayan birine gönderiyorsanız "
        "kutu daha pratik. Elden verilecek, \"kucak dolusu\" bir hediye istiyorsanız buket daha etkili.",
    ], None),
    ("Belek Kutuda Çiçek Sipariş Ver", [
        f"Aranjmanı seçip WhatsApp'tan yazın ya da {TEL} numarasını arayın; aynı gün gönderiyoruz.",
    ], "adim"),
    ("Kutuda Aranjman Teslimatı Nasıl Yapılıyor?", TESLIM_KISA, None),
],
"hediye-ayicikli": [
    ("Belek Ayıcıklı Buket Fiyatları", [
        "Ayıcıklı ve hediyelik ürünlerimiz 2.600 TL'den başlayan fiyatlarla. Beğendiğiniz ürünün "
        "fiyatını WhatsApp'tan hemen yazıyoruz.",
    ], "urunler"),
    ("Ayıcıklı Buketi Kime Gönderilir?", [
        "Ayıcıklı buketler sevgiliye, yeni doğan bebeği olan ailelere ve çocuklara güzel gider. "
        "Çikolata ve şekerleme kutumuz da çiçek sevmeyen ama tatlıya hayır demeyenler için :)",
    ], None),
    ("Belek Hediye Sipariş Ver", [
        f"Ürünü seçip WhatsApp'tan yazın ya da {TEL} numarasını arayın.",
    ], "adim"),
    ("Hediye Teslimatı Nasıl Yapılıyor?", TESLIM_KISA, None),
],
"gelin-cicegi-arac-susleme": [
    ("Belek Gelin Arabası Süsleme Fiyatı", [
        "Araç süslemesi 3.000 TL'den başlıyor; son fiyat aracın boyuna ve kullanılacak çiçeğe göre belli "
        "oluyor. Gelin buketlerinin fiyatını da çiçek seçimine göre WhatsApp'tan söylüyoruz.",
    ], "urunler"),
    ("Gelin Çiçeği Seçerken", [
        "Gelin buketini gelinliğin rengine ve modeline göre birlikte seçiyoruz; fotoğrafını gönderirseniz "
        "ona uygun öneri yaparız. Düğün, nişan ya da kına tarihiniz belliyse erkenden haber verin; "
        "özellikle düğün sezonunda takvim çabuk doluyor.",
    ], None),
    ("Belek Gelin Çiçeği Sipariş Ver", [
        f"Tarihi ve aracın fotoğrafını WhatsApp'tan gönderin ya da {TEL} numarasını arayın.",
    ], "adim"),
    ("Gelin Çiçeği ve Araç Süsleme Teslimi", [
        "Gelin buketini düğün günü istediğiniz adrese teslim ediyoruz ya da mağazadan alabilirsiniz. "
        "Araç süslemesi için aracı hangi saatte ve nerede süsleyeceğimizi önceden birlikte planlıyoruz.",
    ], None),
],
}
