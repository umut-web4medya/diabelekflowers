(function () {
  // mobil menü
  var d = document.querySelector('.menu-d'), m = document.getElementById('menu');
  if (d && m) d.addEventListener('click', function () {
    var a = m.classList.toggle('acik'); d.setAttribute('aria-expanded', a ? 'true' : 'false');
  });
  // masaüstü açılır menü: dokunmatikte tıkla-aç
  document.querySelectorAll('.acilir-d').forEach(function (b) {
    b.addEventListener('click', function () {
      var p = b.parentNode, a = p.classList.toggle('acik'); b.setAttribute('aria-expanded', a ? 'true' : 'false');
    });
  });
  // harita: tıklanana kadar iframe yok (üçüncü parti istek 0)
  document.querySelectorAll('.harita').forEach(function (h) {
    var b = h.querySelector('.harita-d');
    if (b) b.addEventListener('click', function () {
      var f = document.createElement('iframe');
      f.src = h.getAttribute('data-src'); f.loading = 'lazy'; f.title = 'DİA Flowers Belek konumu';
      f.referrerPolicy = 'strict-origin-when-cross-origin'; f.allowFullscreen = true;
      h.innerHTML = ''; h.appendChild(f);
    });
  });
  // dock: sayfa dibine yaklaşınca gizle (Web4Medya imzası örtülmesin)
  var k = document.querySelector('.dock');
  if (k) {
    var t = false;
    var bak = function () {
      t = false;
      var kalan = document.documentElement.scrollHeight - (window.scrollY + window.innerHeight);
      k.classList.toggle('gizli', kalan < 140);
    };
    window.addEventListener('scroll', function () { if (!t) { t = true; requestAnimationFrame(bak); } }, { passive: true });
    bak();
  }
  // arama: assets/ara.json ilk odakta bir kez yüklenir; Türkçe harfe duyarsız
  var f = document.querySelector('.ara');
  if (f) {
    var g = f.querySelector('input'), kutu = f.querySelector('.ara-sonuc'), kok = f.getAttribute('data-kok') || '';
    var veri = null, secili = -1;
    var sade = function (t) {
      return (t || '').toLocaleLowerCase('tr').replace(/ı/g, 'i').replace(/ğ/g, 'g').replace(/ü/g, 'u')
        .replace(/ş/g, 's').replace(/ö/g, 'o').replace(/ç/g, 'c').replace(/â/g, 'a');
    };
    var yukle = function () {
      if (veri) return Promise.resolve(veri);
      return fetch(kok + 'assets/ara.json').then(function (r) { return r.json(); })
        .then(function (d) { veri = d.map(function (x) { x.s = sade(x.t + ' ' + x.k); return x; }); return veri; });
    };
    var kapat = function () { kutu.hidden = true; secili = -1; };
    var goster = function () {
      var q = sade(g.value.trim());
      if (q.length < 2) { kapat(); return; }
      yukle().then(function (d) {
        var p = q.split(/\s+/);
        var s = d.filter(function (x) { return p.every(function (k) { return x.s.indexOf(k) > -1; }); }).slice(0, 8);
        kutu.innerHTML = s.length ? s.map(function (x) {
          return '<a href="' + kok + x.u + '"><img src="' + kok + 'images/' + x.g + '-480.webp" alt="" loading="lazy">' +
            '<span><b></b><small></small></span><em></em></a>';
        }).join('') : '<div class="ara-bos">Sonuç yok. WhatsApp\'tan sorabilirsiniz: 0534 603 21 15</div>';
        Array.prototype.forEach.call(kutu.querySelectorAll('a'), function (a, i) {
          a.querySelector('b').textContent = s[i].t; a.querySelector('small').textContent = s[i].k;
          a.querySelector('em').textContent = s[i].f;
        });
        kutu.hidden = false; secili = -1;
      }).catch(kapat);
    };
    g.addEventListener('focus', function () { yukle(); });
    g.addEventListener('input', goster);
    g.addEventListener('keydown', function (e) {
      var l = kutu.querySelectorAll('a');
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        if (!l.length) return; e.preventDefault();
        secili = (secili + (e.key === 'ArrowDown' ? 1 : -1) + l.length) % l.length;
        Array.prototype.forEach.call(l, function (a, i) { a.classList.toggle('sec', i === secili); });
      } else if (e.key === 'Enter') {
        var h = l[secili > -1 ? secili : 0]; if (h) location.href = h.href;
      } else if (e.key === 'Escape') { kapat(); }
    });
    document.addEventListener('click', function (e) { if (!f.contains(e.target)) kapat(); });
  }
})();
