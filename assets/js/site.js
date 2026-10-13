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
})();
