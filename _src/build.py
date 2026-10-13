#!/usr/bin/env python3
"""diabelekflowers.com statik site üreticisi. ⛔ HTML'i elle düzenleme — burayı ve data.py'yi düzelt, çalıştır.
Çalıştır: python3 _src/build.py   (sonra: python3 _src/denetim.py)
Tüm iç yollar göreli (ONEK) → GitHub Pages alt yolunda da çalışır. 404.html istisna (kökten /).
"""
import hashlib, html, json, os, re, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
import icerik as I
import media

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = D.SITE
E = html.escape
KAT = {k["slug"]: k for k in D.KATEGORI}
URUN = {u["ad"]: u for u in D.URUNLER}
SAYFALAR = []  # sitemap


def surum(yol):
    with open(os.path.join(KOK, yol), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def fiyat_yaz(u):
    t = f"{u['fiyat']:,}".replace(",", ".") + " TL"
    return t + "'den" if u.get("fiyat_on") else t


def yonelme(ad):
    """Türkçe yönelme eki: Belek'e, Kadriye'ye, Serik'e."""
    son = [c for c in ad.lower() if c in "aeıioöuü"][-1]
    ek = "e" if son in "eiöü" else "a"
    return f"{ad}'{'y' if ad[-1].lower() in 'aeıioöuü' else ''}{ek}"


def wa(metin):
    return f"https://wa.me/{S['wa']}?text=" + urllib.parse.quote(metin)


# ── ikonlar (satır içi SVG, dış istek yok) ──────────────────────────────────
IK = {
    "tel": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.25-.12-1.47-.72-1.7-.8-.23-.09-.4-.13-.56.12-.17.25-.64.8-.79.97-.14.17-.29.19-.54.06a6.7 6.7 0 0 1-3.3-2.9c-.25-.43.25-.4.71-1.33a.45.45 0 0 0-.02-.42c-.06-.12-.56-1.35-.77-1.85-.2-.48-.4-.42-.56-.42h-.47a.9.9 0 0 0-.65.3 2.7 2.7 0 0 0-.85 2.02 4.7 4.7 0 0 0 1 2.5 10.8 10.8 0 0 0 4.1 3.65c1.53.66 2.13.71 2.9.6.47-.07 1.47-.6 1.67-1.18.21-.58.21-1.08.15-1.18-.06-.1-.23-.17-.48-.29z"/></svg>',
    "konum": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
    "saat": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2zm.75 10.4 3.6 2.15-.75 1.25L11.25 13V7h1.5z"/></svg>',
    "teslim": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 5h11v9h2.2l1.3-4H20l1 3v4h-1.6a2.5 2.5 0 0 1-4.8 0H9.4a2.5 2.5 0 0 1-4.8 0H3zm4 13.2a1 1 0 1 0 0-2 1 1 0 0 0 0 2zm10 0a1 1 0 1 0 0-2 1 1 0 0 0 0 2z"/></svg>',
    "etiket": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 3h8l10 10-8 8L3 11zm4.5 6A1.5 1.5 0 1 0 6 7.5 1.5 1.5 0 0 0 7.5 9z"/></svg>',
    "ara": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10.5 3a7.5 7.5 0 0 1 5.9 12.1l4.3 4.3-1.4 1.4-4.3-4.3A7.5 7.5 0 1 1 10.5 3zm0 2a5.5 5.5 0 1 0 0 11 5.5 5.5 0 0 0 0-11z"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18v2H3zm0 5h18v2H3zm0 5h18v2H3z"/></svg>',
    "ok": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M13 5l7 7-7 7-1.4-1.4 4.6-4.6H4v-2h12.2l-4.6-4.6z"/></svg>',
}


def resim(on, ad, alt, sinif="", oncelik=False, sizes="(max-width:640px) 50vw, 300px"):
    w, h = media.boyut(ad)
    yukle = 'fetchpriority="high"' if oncelik else 'loading="lazy" decoding="async"'
    return (f'<img class="{sinif}" src="{on}images/{ad}-900.webp" '
            f'srcset="{on}images/{ad}-480.webp 480w, {on}images/{ad}-900.webp 900w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{E(alt)}" {yukle}>')


# ── kabuk ───────────────────────────────────────────────────────────────────
def florist_sema(tam=True):
    d = {"@context": "https://schema.org", "@type": "Florist", "@id": S["alan"] + "/#isletme",
         "name": S["marka"], "alternateName": [S["gbp_ad"], "Serik DİA Flowers"],
         "url": S["alan"] + "/", "telephone": "+90 534 603 21 15", "email": S["eposta"],
         "address": {"@type": "PostalAddress", "streetAddress": S["adres_satir"], "postalCode": S["posta"],
                     "addressLocality": S["ilce"], "addressRegion": S["il"], "addressCountry": "TR"},
         "geo": {"@type": "GeoCoordinates", "latitude": S["geo"][0], "longitude": S["geo"][1]},
         "hasMap": S["harita_link"], "priceRange": "1.300 TL – 8.600 TL",
         "openingHoursSpecification": {"@type": "OpeningHoursSpecification",
                                       "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                                                     "Saturday", "Sunday"], "opens": "00:00", "closes": "23:59"},
         "image": S["alan"] + "/images/magaza-900.webp"}
    if tam:
        d["areaServed"] = [{"@type": "Place", "name": b["ad"] + ", Serik, Antalya"} for b in D.BOLGELER]
    return d


def kirinti(on, yol):
    oge = [{"@type": "ListItem", "position": i + 1, "name": ad, "item": S["alan"] + "/" + u}
           for i, (ad, u) in enumerate(yol)]
    sema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": oge}
    html_ = " <span>/</span> ".join(
        f'<a href="{on}{u}">{E(ad)}</a>' if i < len(yol) - 1 else f'<span aria-current="page">{E(ad)}</span>'
        for i, (ad, u) in enumerate(yol))
    return f'<nav class="kirinti" aria-label="Sayfa yolu">{html_}</nav>', sema


def slug(t):
    tr = str.maketrans("çğıöşüÇĞİÖŞÜ", "cgiosuCGIOSU")
    return re.sub(r"[^a-z0-9]+", "-", t.translate(tr).lower()).strip("-")


def ust(on, aktif):
    bols = "".join(f'<a href="{on}{bolge_url(b)}">{E(b["ad"])}</a>' for b in D.BOLGELER)
    ac = ' aria-current="page"'
    kats = "".join(f'<a href="{on}{k["slug"]}/"{ac if aktif == k["slug"] else ""}>{E(k["kisa_menu"])}</a>'
                   for k in D.KATEGORI)
    return f"""<div class="duyuru"><div class="kap duyuru-ic">
 <span class="duyuru-slogan">Belek'in çiçekçisi</span>
 <span class="duyuru-orta">{IK['teslim']}<b>Aynı gün teslimat</b><span class="duyuru-ay">Belek · Kadriye · Doğakent · Serik · Boğazkent</span></span>
 <a class="duyuru-tel" href="tel:{S['tel_link']}">{IK['saat']}Her gün 24 saat · {S['tel_goster']}</a>
</div></div>
<header class="ust">
 <div class="kap ust-ic">
  <a class="logo" href="{on}" aria-label="DİA Flowers Belek anasayfa"><img src="{on}images/favicon-192.png" width="40" height="40" alt=""><span class="logo-y"><span class="logo-dia">DİA <i>Flowers</i></span><small>Belek · Serik</small></span></a>
  <form class="ara" role="search" action="{on}" data-kok="{on}" onsubmit="return false">
   <label class="atla" for="ara-g">Ürün, kategori ya da bölge ara</label>
   <input id="ara-g" type="search" placeholder="Gül, orkide, Kadriye… ara" autocomplete="off" enterkeyhint="search">
   <button type="submit" aria-label="Ara">{IK['ara']}</button>
   <div class="ara-sonuc" hidden></div>
  </form>
  <div class="ust-sag">
   <a class="ik-l" href="{on}iletisim/"{' aria-current="page"' if aktif == 'iletisim' else ''}>{IK['konum']}<span>Mağaza</span></a>
   <a class="dg dg-wa" href="{wa('Merhaba, çiçek siparişi vermek istiyorum.')}" rel="noopener" target="_blank">{IK['wa']}<span class="dg-yz">WhatsApp Sipariş</span></a>
   <button class="menu-d" type="button" aria-controls="menu" aria-expanded="false" aria-label="Menüyü aç">{IK['menu']}</button>
  </div>
 </div>
 <nav class="menu" id="menu" aria-label="Kategoriler">
  <div class="kap menu-ic">{kats}
   <div class="acilir"><button type="button" class="acilir-d" aria-expanded="false">Teslimat Bölgeleri</button><div class="acilir-ic">{bols}</div></div>
   <a href="{on}iletisim/" class="menu-son">İletişim</a>
  </div>
 </nav>
</header>"""


def alt(on):
    kats = "".join(f'<li><a href="{on}{k["slug"]}/">{E(k["ad"])}</a></li>' for k in D.KATEGORI)
    bols = "".join(f'<li><a href="{on}{bolge_url(b)}">{E(b["ad"])} çiçekçi</a></li>' for b in D.BOLGELER)
    return f"""<footer class="alt">
 <div class="kap alt-izgara">
  <div><p class="alt-logo">DİA Flowers <em>Belek</em></p>
   <p>{E(S['adres_satir'])}, {S['posta']} {S['ilce']}/{S['il']}</p>
   <p><a href="tel:{S['tel_link']}">{S['tel_goster']}</a> · {E(S['saat'])}</p>
   <p><a href="{S['harita_link']}" rel="noopener" target="_blank">Google Haritalar'da aç</a></p></div>
  <div><p class="alt-bas">Çiçekler</p><ul>{kats}</ul></div>
  <div><p class="alt-bas">Teslimat bölgeleri</p><ul>{bols}</ul></div>
 </div>
 <div class="kap alt-son"><span>© 2026 {E(S['marka'])}</span>
  <div class="w4"><div class="w4-bag"><span class="w4-etiket">Web Tasarım:</span> <a class="w4-ad" href="https://www.web4medya.com/" target="_blank" rel="noopener"><span class="w4-d">Web<b>4</b>Medya</span></a></div></div>
 </div>
</footer>
<div class="dock" aria-label="Hızlı iletişim">
 <a class="dock-ara" href="tel:{S['tel_link']}"><span class="dock-ik">{IK['tel']}</span><span class="dock-y"><b>Hemen Ara</b><small>{S['tel_goster']}</small></span></a>
 <a class="dock-wa" href="{wa('Merhaba, çiçek siparişi vermek istiyorum.')}" rel="noopener" target="_blank"><span class="dock-ik">{IK['wa']}</span><span class="dock-y"><b>WhatsApp</b><small>Sipariş yazın</small></span></a>
</div>"""


def sayfa(yol, title, desc, govde, semalar, aktif=""):
    """yol: '' (anasayfa) ya da 'slug/' — ONEK derinliğe göre."""
    derin = yol.count("/")
    on = "../" * derin
    canon = S["alan"] + "/" + yol
    css, js = surum("assets/css/site.css"), surum("assets/js/site.js")
    sema_html = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>'
                        for s in semalar)
    h = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{canon}">
<meta name="theme-color" content="#1F7A4D">
<meta property="og:type" content="website"><meta property="og:locale" content="tr_TR">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{S['alan']}/images/og.jpg">
<link rel="icon" href="{on}favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="192x192" href="{on}images/favicon-192.png">
<link rel="apple-touch-icon" href="{on}images/favicon-192.png">
<link rel="preload" href="{on}assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{on}assets/css/site.css?v={css}">
{sema_html}
</head>
<body>
<a class="atla" href="#icerik">İçeriğe geç</a>
{ust(on, aktif)}
<main id="icerik">
{govde(on)}
</main>
{alt(on)}
<script src="{on}assets/js/site.js?v={js}" defer></script>
</body>
</html>
"""
    hedef = os.path.join(KOK, yol, "index.html")
    os.makedirs(os.path.dirname(hedef), exist_ok=True)
    with open(hedef, "w", encoding="utf-8") as f:
        f.write(h)
    SAYFALAR.append(yol)


# ── bileşenler ──────────────────────────────────────────────────────────────
def urun_kart(on, u, bolge=None, oncelik=False):
    nereye = f" {bolge} adresine" if bolge else ""
    mesaj = f"Merhaba, {u['ad']} ({fiyat_yaz(u)}){nereye} sipariş vermek istiyorum."
    rozet = "" if u.get("fiyat_on") else '<span class="rozet">Aynı gün teslimat</span>'
    return f"""<article class="kart" id="{slug(u['ad'])}">
 <div class="kart-g">{resim(on, u['gorsel'][0], u['ad'] + ' — DİA Flowers Belek', oncelik=oncelik)}{rozet}</div>
 <div class="kart-ic">
  <h3>{E(u['ad'])}</h3>
  <p class="kart-a">{E(u['aciklama'])}</p>
  <p class="fiyat">{fiyat_yaz(u)}</p>
  <div class="kart-d"><a class="btn btn-wa" href="{wa(mesaj)}" rel="noopener" target="_blank">{IK['wa']}<span class="uzun">WhatsApp'tan sipariş</span><span class="kisa">Sipariş ver</span></a><a class="btn btn-ara" href="tel:{S['tel_link']}" aria-label="{E(u['ad'])} için ara">{IK['tel']}</a></div>
 </div>
</article>"""


def galeri_kart(on, ad, alt_):
    mesaj = f"Merhaba, sitenizdeki \"{alt_}\" ürününün fiyatını öğrenebilir miyim?"
    return f"""<figure class="gk">{resim(on, ad, alt_ + ' — DİA Flowers Belek', sizes='(max-width:640px) 50vw, 240px')}
 <figcaption><span>{E(alt_)}</span><a href="{wa(mesaj)}" rel="noopener" target="_blank">{IK['wa']}Fiyat sor</a></figcaption></figure>"""


def kat_kutu(on, k):
    kapak = k.get("kapak") or next((u["gorsel"][0] for u in D.URUNLER if u["kat"] == k["slug"]), None)
    say = sum(1 for u in D.URUNLER if u["kat"] == k["slug"])
    alt_ = f"{say} fiyatlı ürün" if say else "Fotoğraflı galeri"
    return f"""<a class="kk" href="{on}{k['slug']}/">{resim(on, kapak, k['ad'], sizes='(max-width:640px) 50vw, 320px')}
 <span class="kk-ic"><strong>{E(k['ad'])}</strong><small>{alt_}</small></span></a>"""


def guven(on):
    return f"""<ul class="guven kap">
 <li>{IK['teslim']}<span><b>Aynı gün teslimat</b>Belek, Kadriye, Doğakent, Serik, Boğazkent</span></li>
 <li>{IK['saat']}<span><b>Her gün 24 saat</b>Gece siparişinde de telefonu açıyoruz</span></li>
 <li>{IK['etiket']}<span><b>Fiyatlar açık</b>Her ürünün fiyatı kartında yazıyor</span></li>
 <li>{IK['wa']}<span><b>WhatsApp'tan sipariş</b>Ürün adı mesaja kendiliğinden yazılır</span></li>
</ul>"""


def adim_liste():
    return """<ol class="adim">
  <li><b>Ürünü seçin.</b> Kartın altındaki <em>Sipariş ver</em> düğmesi WhatsApp'ı ürün adıyla açar.</li>
  <li><b>Adresi ve notu yazın.</b> Alıcının adı, teslim adresi, teslim saati ve kartta yazmasını istediğiniz not.</li>
  <li><b>Hazırlayıp yola çıkaralım.</b> Siparişi Belek'teki mağazamızda hazırlayıp aynı gün teslim ediyoruz.</li>
 </ol>"""


def harita(on):
    return f"""<div class="harita" data-src="{E(S['harita_embed'])}">
 <button type="button" class="harita-d">{IK['konum']}<span>Haritayı yükle</span><small>Google Haritalar — {E(S['gbp_ad'])}</small></button>
</div>"""


def magaza_ic(on):
    fotos = "".join(f'<figure>{resim(on, a, t, sizes="(max-width:640px) 100vw, 360px")}</figure>' for a, t in D.MAGAZA[:2])
    return f"""<div class="magaza">
 <div class="mg-yazi">
  <ul class="bilgi">
   <li>{IK['konum']}<span>{E(S['adres_satir'])}, {S['posta']} {S['ilce']}/{S['il']}</span></li>
   <li>{IK['tel']}<a href="tel:{S['tel_link']}">{S['tel_goster']}</a></li>
   <li>{IK['saat']}<span>{E(S['saat'])}</span></li>
  </ul>
  <a class="btn btn-ana" href="{S['harita_link']}" rel="noopener" target="_blank">{IK['konum']}Yol tarifi al</a></div>
 <div class="mg-foto">{fotos}</div>
</div>"""


def fiyat_tablo(on):
    satir = ""
    for k in D.KATEGORI:
        us = [u for u in D.URUNLER if u["kat"] == k["slug"]]
        if not us: continue
        en = min(us, key=lambda u: u["fiyat"])
        satir += (f'<tr><th scope="row"><a href="{on}{k["slug"]}/">{E(k["ad"])}</a></th>'
                  f'<td>{len(us)}</td><td class="tf">{fiyat_yaz(dict(en, fiyat_on=True)) if not en.get("fiyat_on") else fiyat_yaz(en)}</td></tr>')
    return f"""<div class="tablo-k"><table class="tablo"><thead><tr><th scope="col">Kategori</th><th scope="col">Fiyatlı ürün</th><th scope="col">Başlangıç fiyatı</th></tr></thead>
<tbody>{satir}</tbody></table></div>"""


def metin(on, bolumler, urun_html=""):
    """icerik.py bölümleri → HTML. Paragraflar güvenilir kaynak (bizim dosyamız), içinde <a>/<em> olabilir."""
    out = ""
    for h2, paras, isaret in bolumler:
        ek = {"urunler": urun_html, "fiyat": fiyat_tablo(on), "adim": adim_liste(),
              "magaza": magaza_ic(on), None: ""}[isaret]
        sinif = " genis" if isaret in ("urunler", "magaza") else ""
        p = "".join(f"<p>{x}</p>" for x in paras)
        kimlik = ' id="teslimat"' if "Teslimatı Nasıl" in h2 else ""
        out += f'<section class="bolum kap yazi{sinif}"{kimlik}><h2>{E(h2)}</h2><div class="yz">{p}</div>{ek}</section>\n'
    return out


def cta(on, metin="Aklınızdaki çiçek listede yoksa fotoğrafını gönderin; benzerini hazırlayalım."):
    return f"""<section class="cta kap"><p>{E(metin)}</p>
 <div><a class="btn btn-wa" href="{wa('Merhaba, özel bir çiçek siparişi için bilgi almak istiyorum.')}" rel="noopener" target="_blank">{IK['wa']}WhatsApp'tan yazın</a>
 <a class="btn btn-acik" href="tel:{S['tel_link']}">{IK['tel']}{S['tel_goster']}</a></div></section>"""


def bolge_url(b):
    """Belek = anasayfa (dükkân Belek'te; ayrı Belek sayfası anasayfayla aynı niyeti kannibalize ederdi)."""
    return "" if b.get("ana") else b["slug"] + "/"


def bolge_linkleri(on, haric=None):
    return "".join(f'<a class="etk" href="{on}{bolge_url(b)}">{E(b["ad"])}</a>' for b in D.BOLGELER if b["slug"] != haric)


# ── sayfalar ────────────────────────────────────────────────────────────────
def anasayfa():
    populer = ["101 Rodos Gül Buketi (60 cm)", "İthal Orkideler", "Kalp Kutu 31 Güllü Aranjman", "21 Güllü Buket",
               "Lisyantus Orta Boy Renkli Buket", "Kokinalı Ayıcıklı Buket", "Dokuz Güllü Renkli Buket", "Teraryum Çalışması"]
    sss_sema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in D.SSS]}

    def g(on):
        kartlar = "".join(urun_kart(on, URUN[a], oncelik=False) for a in populer)
        kats = "".join(kat_kutu(on, k) for k in D.KATEGORI)
        sss = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in D.SSS)
        balon = "".join(f'<a class="balon" href="{on}{u}"><span class="balon-g">{resim(on, g_, a_, sizes="96px")}</span><span>{E(a_)}</span></a>'
                        for g_, a_, u in D.BALON)

        def ban(b, buyuk):
            renk, ust_, bas, alt_, g_, u = b
            return (f'<a class="ban ban-{renk}{" ban-b" if buyuk else ""}" href="{on}{u}"><span class="ban-y">'
                    f'<small>{E(ust_)}</small><strong>{E(bas)}</strong><em>{E(alt_)}</em>'
                    f'<span class="ban-p">{IK["teslim"]}Aynı gün teslimat</span></span>'
                    f'{resim(on, g_, bas, "ban-g", oncelik=buyuk, sizes="(max-width:640px) 45vw, 300px")}</a>')
        bans_b = "".join(ban(b, True) for b in D.BANNER_BUYUK)
        bans_k = "".join(ban(b, False) for b in D.BANNER_KUCUK)
        return f"""<section class="kap balonlar" aria-label="Çiçek kategorileri"><div class="balon-serit">{balon}</div></section>
<section class="kap vitrin" aria-label="Öne çıkanlar">
 <div class="vitrin-b">{bans_b}</div>
 <div class="vitrin-k">{bans_k}</div>
</section>
<section class="kap giris">
 <div><p class="ust-etiket">Belek · Kadriye · Doğakent · Serik · Boğazkent</p>
  <h1 class="giris-bas">Belek çiçekçi: <em>aynı gün</em> kapıda</h1>
  <p class="giris-p">Gül buketi, orkide, kutuda aranjman ve gelin çiçeği. Fiyatlar kartların üstünde; seçtiğiniz ürünü WhatsApp'tan yazın, Belek'teki mağazamızdan hazırlayıp gönderelim.</p></div>
 <div class="giris-d"><a class="btn btn-wa" href="{wa('Merhaba, çiçek siparişi vermek istiyorum.')}" rel="noopener" target="_blank">{IK['wa']}WhatsApp'tan sipariş</a><a class="btn btn-acik" href="tel:{S['tel_link']}">{IK['tel']}{S['tel_goster']}</a></div>
</section>
{guven(on)}
{metin(on, I.SAYFA[""][:2])}
<section class="bolum kap"><div class="bas"><h2>Belek'te Öne Çıkan Çiçekler</h2><p>Fiyatı belli, fotoğrafı mağazamızda çekilmiş ürünler.</p></div>
 <div class="izgara">{kartlar}</div></section>
<section class="bolum kap"><div class="bas"><h2>Çiçek Çeşitleri</h2><p>Altı başlıkta 18 fiyatlı ürün ve 50'yi aşkın fotoğraflı çalışma.</p></div>
 <div class="kk-izgara">{kats}</div></section>
{metin(on, I.SAYFA[""][2:])}
<section class="bolum kap"><div class="bas"><h2>Teslimat Bölgeleri</h2><p>Belek dışındaki her bölge için ayrı bir sayfamız var.</p></div>
 <div class="etk-satir">{bolge_linkleri(on)}</div></section>
<section class="bolum kap sss"><h2>Sık sorulan sorular</h2>{sss}</section>
{cta(on)}"""
    sayfa("", "Belek Çiçekçi — Aynı Gün Çiçek Teslimatı | DİA Flowers",
          "Belek, Kadriye, Doğakent, Serik ve Boğazkent'e aynı gün çiçek teslimatı. Gül buketi 1.300 TL'den, "
          "orkide 1.700 TL. Her gün 24 saat WhatsApp'tan sipariş.", g, [florist_sema(), sss_sema])


def kategori_sayfa(k):
    urunler = [u for u in D.URUNLER if u["kat"] == k["slug"]]
    galeri = D.GALERI.get(k["slug"], [])
    yol = k["slug"] + "/"
    kir_html, kir_sema = kirinti("../", [("Anasayfa", ""), (k["ad"], yol)])
    liste = {"@context": "https://schema.org", "@type": "ItemList", "name": k["ad"], "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "item": {
            "@type": "Product", "name": u["ad"], "description": u["aciklama"],
            "image": S["alan"] + f"/images/{u['gorsel'][0]}-900.webp",
            "offers": {"@type": "Offer", "price": u["fiyat"], "priceCurrency": "TRY",
                       "availability": "https://schema.org/InStock", "seller": {"@id": S["alan"] + "/#isletme"}}}}
        for i, u in enumerate(urunler)]}

    def g(on):
        kartlar = "".join(urun_kart(on, u, oncelik=(i == 0)) for i, u in enumerate(urunler))
        gal = "".join(galeri_kart(on, a, t) for a, t in galeri)
        diger = "".join(f'<a class="etk" href="{on}{x["slug"]}/">{E(x["ad"])}</a>' for x in D.KATEGORI if x is not k)
        gal_html = (f"""<section class="bolum kap"><div class="bas"><h2>Mağazadan diğer çalışmalar</h2>
 <p>Bu çalışmaların fiyatı çiçeğin mevsimine göre değişiyor. Fotoğrafın altındaki düğmeyle fiyat sorabilirsiniz.</p></div>
 <div class="g-izgara">{gal}</div></section>""" if gal else "")
        govde = metin(on, I.KATEGORI[k["slug"]], f'<div class="izgara">{kartlar}</div>')
        return f"""<section class="sb kap">{kir_html}<h1>{E(k['h1'])}</h1><p class="sb-p">{E(k['ozet'])} Belek, Kadriye, Doğakent, Serik ve Boğazkent'e aynı gün teslim ediyoruz.</p></section>
{guven(on)}
{govde}
{gal_html}
<section class="bolum kap"><h2>Diğer çiçekler</h2><div class="etk-satir">{diger}</div>
 <h2 class="ara-bas">Teslimat bölgeleri</h2><div class="etk-satir">{bolge_linkleri(on)}</div></section>
{cta(on)}"""
    desc = f"{k['ozet']} Belek'teki DİA Flowers'tan aynı gün teslimat; WhatsApp'tan sipariş."
    sema = [florist_sema(False), kir_sema] + ([liste] if urunler else [])
    sayfa(yol, k["title"] + " | DİA Flowers", desc[:158], g, sema, aktif=k["slug"])


def bolge_sayfa(b):
    yol = b["slug"] + "/"
    kir_html, kir_sema = kirinti("../", [("Anasayfa", ""), (b["ad"] + " çiçekçi", yol)])
    secilen = [URUN[a] for a in b["one_cikan"]]
    sss = [
        (f"{yonelme(b['ad'])} aynı gün çiçek gönderebilir miyim?",
         "Evet. Siparişi WhatsApp'tan ya da telefonla verin; teslim saatini sipariş sırasında söylüyoruz."),
        (f"{b['ad']} için hangi çiçekleri öneriyorsunuz?",
         "Bu sayfada önerdiğimiz dört ürün: " + ", ".join(b["one_cikan"]) + "."),
        ("Mağazanız nerede?", f"Mağazamız {S['adres_satir']}, {S['ilce']}/{S['il']} adresinde. Her gün 24 saat açığız."),
    ]
    sss_sema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in sss]}

    def g(on):
        kartlar = "".join(urun_kart(on, u, bolge=b["ad"], oncelik=(i == 0)) for i, u in enumerate(secilen))
        kats = "".join(kat_kutu(on, k) for k in D.KATEGORI)
        sss_h = "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in sss)
        return f"""<section class="sb kap">{kir_html}<h1>{E(b['ad'])} çiçekçi — aynı gün çiçek teslimatı</h1>
 <p class="sb-p">{E(b['konum'])} {E(b['ad'])} adresinize gül buketi, orkide, kutuda aranjman ya da ayıcıklı buket gönderiyoruz; fiyatlar aşağıdaki kartlarda yazıyor.</p></section>
{guven(on)}
{metin(on, I.SAYFA[b['slug']], f'<div class="izgara">{kartlar}</div>')}
<section class="bolum kap"><div class="bas"><h2>{E(b['ad'])} Çiçek Çeşitleri</h2><p>Bütün kategoriler; tıklayınca fiyatlarıyla açılır.</p></div><div class="kk-izgara">{kats}</div></section>
<section class="bolum kap"><h2>Mağazamızın Konumu</h2><div class="yz"><p>{E(S['adres_satir'])}, {S['posta']} {S['ilce']}/{S['il']} · {E(S['saat'])}</p></div>{harita(on)}</section>
<section class="bolum kap sss"><h2>{E(b['ad'])} çiçek siparişi: sorular</h2>{sss_h}</section>
<section class="bolum kap"><h2>Diğer teslimat bölgeleri</h2><div class="etk-satir">{bolge_linkleri(on, b['slug'])}</div></section>
{cta(on)}"""
    sayfa(yol, f"{b['ad']} Çiçekçi — Aynı Gün Çiçek Teslimatı | DİA Flowers",
          f"{b['ad']} çiçek siparişi: gül buketi, orkide ve kutuda aranjman aynı gün adrese. "
          f"Belek'teki DİA Flowers mağazasından; WhatsApp'tan sipariş, her gün 24 saat.",
          g, [florist_sema(False), kir_sema, sss_sema])


def iletisim():
    kir_html, kir_sema = kirinti("../", [("Anasayfa", ""), ("Mağaza ve iletişim", "iletisim/")])

    def g(on):
        fotos = "".join(f'<figure>{resim(on, a, t, sizes="(max-width:640px) 100vw, 380px")}</figure>' for a, t in D.MAGAZA)
        return f"""<section class="sb kap">{kir_html}<h1>Mağaza ve iletişim</h1>
 <p class="sb-p">Belek'te, Vatan Caddesi'ndeyiz. Her gün 24 saat telefon ve WhatsApp'tan sipariş alıyoruz.</p></section>
<section class="bolum kap ilt">
 <ul class="bilgi bilgi-buyuk">
  <li>{IK['konum']}<span><b>Adres</b>{E(S['adres_satir'])}, {S['posta']} {S['ilce']}/{S['il']}</span></li>
  <li>{IK['tel']}<span><b>Telefon</b><a href="tel:{S['tel_link']}">{S['tel_goster']}</a></span></li>
  <li>{IK['wa']}<span><b>WhatsApp</b><a href="{wa('Merhaba, çiçek siparişi vermek istiyorum.')}" rel="noopener" target="_blank">{S['tel_goster']}</a></span></li>
  <li>{IK['saat']}<span><b>Çalışma saatleri</b>{E(S['saat'])}</span></li>
 </ul>
 {harita(on)}
</section>
<section class="bolum kap"><h2>Mağazamız</h2><div class="mg-izgara">{fotos}</div></section>
{cta(on)}"""
    sayfa("iletisim/", "Mağaza ve İletişim — Belek Vatan Caddesi | DİA Flowers",
          "DİA Flowers Belek: Belek, Vatan Cd. No:11 D:c, 07500 Serik/Antalya. Telefon ve WhatsApp 0534 603 21 15, "
          "her gün 24 saat.", g, [florist_sema(), kir_sema], aktif="iletisim")


def yaz_404():
    on = "/"
    css, js = surum("assets/css/site.css"), surum("assets/js/site.js")
    govde = f"""<section class="sb kap"><h1>Sayfa bulunamadı</h1><p class="sb-p">Aradığınız sayfa taşınmış olabilir.</p>
<div class="etk-satir"><a class="etk" href="/">Anasayfa</a>{''.join(f'<a class="etk" href="/{k["slug"]}/">{E(k["ad"])}</a>' for k in D.KATEGORI)}</div></section>"""
    h = f"""<!doctype html><html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sayfa bulunamadı | DİA Flowers Belek</title><meta name="robots" content="noindex">
<link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/css/site.css?v={css}"></head><body>
{ust(on, '')}<main id="icerik">{govde}{cta(on)}</main>{alt(on)}<script src="/assets/js/site.js?v={js}" defer></script></body></html>"""
    open(os.path.join(KOK, "404.html"), "w", encoding="utf-8").write(h)


def ara_dizin():
    d = [{"t": u["ad"], "f": fiyat_yaz(u), "u": u["kat"] + "/#" + slug(u["ad"]), "g": u["gorsel"][0], "k": KAT[u["kat"]]["ad"]}
         for u in D.URUNLER]
    d += [{"t": k["ad"], "f": "", "u": k["slug"] + "/", "g": k["kapak"],
           "k": "Kategori"} for k in D.KATEGORI]
    d += [{"t": a + " (fotoğraf)", "f": "Fiyat sorun", "u": k + "/", "g": g, "k": KAT[k]["ad"]}
          for k, liste in D.GALERI.items() for g, a in liste]
    d += [{"t": b["ad"] + " çiçekçi", "f": "", "u": bolge_url(b), "g": "magaza", "k": "Teslimat bölgesi"} for b in D.BOLGELER]
    with open(os.path.join(KOK, "assets", "ara.json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, separators=(",", ":"))


def ekler():
    with open(os.path.join(KOK, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for y in SAYFALAR:
            f.write(f"  <url><loc>{S['alan']}/{y}</loc><lastmod>2026-10-13</lastmod></url>\n")
        f.write("</urlset>\n")
    open(os.path.join(KOK, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {S['alan']}/sitemap.xml\n")
    open(os.path.join(KOK, "CNAME"), "w").write("diabelekflowers.com\n")


if __name__ == "__main__":
    anasayfa()
    for k in D.KATEGORI: kategori_sayfa(k)
    for b in D.BOLGELER:
        if not b.get("ana"): bolge_sayfa(b)
    iletisim()
    yaz_404()
    ekler()
    ara_dizin()
    print(f"tamam: {len(SAYFALAR)} sayfa + 404")
