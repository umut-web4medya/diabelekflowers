#!/usr/bin/env python3
"""Siyah zeminli kesilmiş ürün fotoğraflarında zemini açık renge çevirir.
Yalnız KENARA DEĞEN koyu bölge zemin sayılır (ürünün içindeki siyah kutu/kurdele korunur).
Kenar geçişi yumuşatılır. Çıktı: _src/kaynak_acik/<ad>.jpeg — media.py bunları tercih eder.
"""
import os, sys
import numpy as np
from PIL import Image, ImageOps, ImageFilter
from scipy import ndimage

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAY, HED = os.path.join(KOK, "_src", "kaynak"), os.path.join(KOK, "_src", "kaynak_acik")
ZEMIN = np.array([255, 255, 255], dtype=np.float32)   # saf beyaz: kartta temiz, bannerda multiply ile kaybolur
T_ZEMIN, T_GECIS = 14, 70

def isle(ad):
    im = ImageOps.exif_transpose(Image.open(os.path.join(KAY, ad + ".jpeg"))).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    mx = a.max(axis=2)
    koyu = mx < T_ZEMIN
    etiket, n = ndimage.label(koyu)
    kenar = set(np.unique(np.concatenate([etiket[0], etiket[-1], etiket[:, 0], etiket[:, -1]]))) - {0}
    zemin = np.isin(etiket, list(kenar))
    if zemin.mean() < 0.08:          # siyah zeminli değil → dokunma
        return False
    zemin = ndimage.binary_opening(zemin, iterations=1)
    # geçiş bandı: zemine 3 px yakın ve koyu pikseller kısmen zemine karışır
    yakin = ndimage.binary_dilation(zemin, iterations=3) & ~zemin
    w = np.zeros(mx.shape, np.float32)
    w[zemin] = 1.0
    gb = yakin & (mx < T_GECIS)
    w[gb] = np.clip((T_GECIS - mx[gb]) / (T_GECIS - T_ZEMIN), 0, 1)
    w = np.asarray(Image.fromarray((w * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) / 255
    out = a * (1 - w[..., None]) + ZEMIN * w[..., None]
    Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(os.path.join(HED, ad + ".jpeg"), quality=92)
    return True

if __name__ == "__main__":
    os.makedirs(HED, exist_ok=True)
    adlar = sys.argv[1:] or sorted(f[:-5] for f in os.listdir(KAY) if f.endswith(".jpeg"))
    say = sum(isle(a) for a in adlar)
    print(f"tamam: {say}/{len(adlar)} görselin zemini açıldı")
