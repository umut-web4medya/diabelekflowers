#!/usr/bin/env python3
"""Yayın öncesi denetim — hata varsa çıkış 1. Çalıştır: python3 _src/denetim.py"""
import glob, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import data as D
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
hata, uyari = [], []
basliklar, aciklamalar = {}, {}
for f in sorted(glob.glob(os.path.join(KOK, "**", "*.html"), recursive=True)):
    if "/_src/" in f: continue
    r = os.path.relpath(f, KOK); s = open(f, encoding="utf-8").read()
    metin = html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S))).lower()
    for t in D.TEYITSIZ:
        if t.lower() in metin: hata.append(f"{r}: teyitsiz ifade '{t}'")
    t = re.search(r"<title>(.*?)</title>", s); d = re.search(r'name="description" content="([^"]*)"', s)
    if t:
        tt = html.unescape(t.group(1))
        if len(tt) > 65 and r != "404.html": uyari.append(f"{r}: title {len(tt)} krk")
        basliklar.setdefault(tt, []).append(r)
    if d:
        aciklamalar.setdefault(d.group(1), []).append(r)
        if len(html.unescape(d.group(1))) > 160: uyari.append(f"{r}: description {len(html.unescape(d.group(1)))} krk")
    if s.count("<h1") != 1: hata.append(f"{r}: {s.count('<h1')} adet h1")
    taban = os.path.dirname(f)
    for u in re.findall(r'(?<![-\w])(?:href|src)="([^"]+)"', s) + [x.split()[0] for x in re.findall(r'srcset="([^"]+)"', s) for x in x.split(",")]:
        u = u.strip()
        if re.match(r"(https?:|tel:|mailto:|#)", u):
            if u.startswith("http") and not re.match(r"https://(wa\.me|maps\.google\.com|www\.web4medya\.com|diabelekflowers\.com)", u):
                hata.append(f"{r}: dış kaynak {u[:60]}")
            continue
        yol = u.split("?")[0].split("#")[0]
        p = os.path.join(KOK, yol.lstrip("/")) if yol.startswith("/") else os.path.normpath(os.path.join(taban, yol))
        if yol.endswith("/") or yol == "": p = os.path.join(p, "index.html")
        if not os.path.exists(p): hata.append(f"{r}: kırık bağlantı {u}")
    if "sigara" in s: hata.append(f"{r}: sigara görseli/metni")
for t, rs in basliklar.items():
    if len(rs) > 1: hata.append(f"tekrar eden title: {t} → {rs}")
for t, rs in aciklamalar.items():
    if len(rs) > 1: hata.append(f"tekrar eden description → {rs}")
print("\n".join(["UYARI " + x for x in uyari] + ["HATA " + x for x in hata]) or "temiz")
sys.exit(1 if hata else 0)
