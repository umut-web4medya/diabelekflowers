#!/usr/bin/env python3
"""Görsel türevleri: _src/kaynak/<ad>.jpeg → images/<ad>-480.webp + <ad>-900.webp (uzun kenar değil GENİŞLİK).
Kaynaklar Hakikatperest/diaflowers deposundan (gerçek ürün/mağaza fotoğrafları). Var olan türev yeniden üretilmez.
"""
import os, sys
from PIL import Image, ImageOps
KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAY, HED = os.path.join(KOK, "_src", "kaynak"), os.path.join(KOK, "images")
GEN = (480, 900)

ACIK = os.path.join(KOK, "_src", "kaynak_acik")   # zemin.py çıktısı (siyah zemin → açık); varsa o kullanılır


def uret(ad):
    src = os.path.join(ACIK, ad + ".jpeg")
    if not os.path.exists(src):
        src = os.path.join(KAY, ad + ".jpeg")
    im = None
    out = {}
    for w in GEN:
        p = os.path.join(HED, f"{ad}-{w}.webp")
        if not os.path.exists(p):
            if im is None:
                im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
            k = im.copy()
            if k.width > w:
                k = k.resize((w, round(k.height * w / k.width)), Image.LANCZOS)
            k.save(p, "WEBP", quality=80, method=5)
        with Image.open(p) as t:
            out[w] = t.size
    return out

def boyut(ad):
    """(genişlik, yükseklik) of 900 türevi — HTML width/height için."""
    return uret(ad)[900]

if __name__ == "__main__":
    os.makedirs(HED, exist_ok=True)
    for f in sorted(os.listdir(KAY)):
        if f.endswith(".jpeg"): uret(f[:-5])
    print("tamam")
