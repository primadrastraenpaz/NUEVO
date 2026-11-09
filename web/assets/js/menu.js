(function () {
  var b = document.querySelector('.menu-boton');
  var m = document.getElementById('menu');
  if (b && m) {
    b.addEventListener('click', function () {
      var abierto = m.classList.toggle('abierto');
      b.setAttribute('aria-expanded', abierto ? 'true' : 'false');
    });
    m.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { m.classList.remove('abierto'); b.setAttribute('aria-expanded', 'false'); }
    });
  }
  var a = document.querySelectorAll('[data-anio]');
  for (var i = 0; i < a.length; i++) a[i].textContent = new Date().getFullYear();
})();
