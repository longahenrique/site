/* Sugerir no mapa: desenhar um percurso, marcar um local novo ou assinalar um problema e enviar por email.
   Tudo fica no navegador até a pessoa clicar em "Enviar por email": o site não recebe nem guarda nada. */
(function () {
  'use strict';
  if (!window.SQ || !window.SQ.mapa || !window.L) return;
  var map = window.SQ.mapa, esc = window.SQ.esc, CATS = window.SQ.cats || [], EMAIL = 'geral@henriquelonga.pt';
  var coluna = document.querySelector('.sq-col-cartao'), corpoMapa = document.querySelector('.sq-corpo'), ctl = document.querySelector('.sq-ctl');
  if (!coluna || !corpoMapa || !ctl) return;
  // botão "Sugerir no mapa": junto aos botões do mapa, e só no ecrã inteiro (no computador)
  var abrir = document.createElement('button'); abrir.type = 'button'; abrir.className = 'sq-vertudo sq-sug-btn'; abrir.textContent = 'Sugerir no mapa'; abrir.hidden = true; ctl.appendChild(abrir);
  var COR = '#b0158f';
  var TIPOS = [['linha', 'Desenhar um percurso (ciclovia, passeio, linha de autocarro)'], ['local', 'Marcar um local novo (escola, paragem, parque…)'], ['problema', 'Assinalar um problema num sítio']];
  var SUB_LINHA = ['Ciclovia', 'Percurso pedonal', 'Linha ou faixa de autocarro', 'Outro percurso'];
  var SUB_LOCAL = CATS.filter(function (c) { return c.id !== 'obra'; }).map(function (c) { return c.nome; }).concat(['Outro']);

  var g = L.featureGroup().addTo(map), pts = [], tipo = 'linha', aberto = false;

  /* geometria */
  function metros(a, b) { return map.distance(a, b); }
  function comprimento() { var t = 0; for (var i = 1; i < pts.length; i++) t += metros(pts[i - 1], pts[i]); return t; }
  function simplifica(ll, tol) {   // Douglas–Peucker, tolerância em metros
    if (ll.length < 3) return ll.slice();
    var la0 = ll[0].lat * Math.PI / 180, kx = 111320 * Math.cos(la0), ky = 110574;
    var P = ll.map(function (p) { return { x: p.lng * kx, y: p.lat * ky, p: p }; }), keep = new Array(P.length);
    keep[0] = keep[P.length - 1] = true;
    (function rec(i, j) {
      var max = 0, k = -1, a = P[i], b = P[j], dx = b.x - a.x, dy = b.y - a.y, d2 = dx * dx + dy * dy;
      for (var m = i + 1; m < j; m++) {
        var t = d2 ? Math.max(0, Math.min(1, ((P[m].x - a.x) * dx + (P[m].y - a.y) * dy) / d2)) : 0;
        var ex = P[m].x - (a.x + t * dx), ey = P[m].y - (a.y + t * dy), d = Math.sqrt(ex * ex + ey * ey);
        if (d > max) { max = d; k = m; }
      }
      if (k > -1 && max > tol) { keep[k] = true; rec(i, k); rec(k, j); }
    })(0, P.length - 1);
    return P.filter(function (_, i) { return keep[i]; }).map(function (q) { return q.p; });
  }
  function encN(v) { v = v < 0 ? ~(v << 1) : (v << 1); var s = ''; while (v >= 0x20) { s += String.fromCharCode((0x20 | (v & 0x1f)) + 63); v >>= 5; } return s + String.fromCharCode(v + 63); }
  function codifica(ll) { var o = '', pa = 0, po = 0; ll.forEach(function (p) { var a = Math.round(p.lat * 1e5), b = Math.round(p.lng * 1e5); o += encN(a - pa) + encN(b - po); pa = a; po = b; }); return o; }
  function descodifica(str) {
    var i = 0, a = 0, b = 0, o = [], n = 0;
    function val() { var r = 0, sh = 0, c; do { c = str.charCodeAt(i++) - 63; r |= (c & 0x1f) << sh; sh += 5; } while (c >= 0x20 && i <= str.length); return (r & 1) ? ~(r >> 1) : (r >> 1); }
    while (i < str.length && n++ < 400) { a += val(); b += val(); o.push([a / 1e5, b / 1e5]); }
    return o;
  }

  /* desenho */
  function desenha() {
    g.clearLayers();
    if (!pts.length) return;
    if (tipo === 'linha' && pts.length > 1) L.polyline(pts, { color: COR, weight: 4, dashArray: '8 7', interactive: false }).addTo(g);
    pts.forEach(function (p, i) { L.circleMarker(p, { radius: tipo === 'linha' ? 5 : 9, color: '#fff', weight: 2, fillColor: COR, fillOpacity: 1, interactive: false }).addTo(g); });
  }

  /* painel */
  var painel = document.createElement('section');
  painel.className = 'sq-sug'; painel.hidden = true; painel.setAttribute('aria-labelledby', 'sq-sug-t');
  painel.innerHTML =
    '<div class="sq-sug-cab"><h3 id="sq-sug-t">Sugerir no mapa</h3><button type="button" class="sq-sug-x" aria-label="Fechar e apagar a sugestão">×</button></div>' +
    '<fieldset class="sq-sug-tipos"><legend>O que queres sugerir?</legend>' + TIPOS.map(function (t, i) { return '<label><input type="radio" name="sq-sug-tipo" value="' + t[0] + '"' + (i === 0 ? ' checked' : '') + '> ' + t[1] + '</label>'; }).join('') + '</fieldset>' +
    '<p class="sq-sug-ajuda" id="sq-sug-ajuda"></p>' +
    '<div class="sq-sug-ferr"><button type="button" data-a="centro">Marcar o centro do mapa</button><button type="button" data-a="desfazer">Desfazer o último</button><button type="button" data-a="limpar">Limpar</button></div>' +
    '<p class="sq-sug-estado" id="sq-sug-estado" role="status" aria-live="polite"></p>' +
    '<div class="sq-sug-campo" id="sq-sug-subw"><label for="sq-sug-sub">Qual?</label><select id="sq-sug-sub"></select></div>' +
    '<div class="sq-sug-campo"><label for="sq-sug-desc">Descreve a tua sugestão</label><textarea id="sq-sug-desc" rows="3" maxlength="600"></textarea></div>' +
    '<p class="sq-sug-nota">O email abre com a sugestão já escrita. Se não abrir, usa "Copiar sugestão" e envia-a para <a href="mailto:' + EMAIL + '">' + EMAIL + '</a>. O site não guarda nada do que desenhas ou escreves. Se não conseguires desenhar, descreve onde fica.</p>' +
    '<div class="sq-sug-acoes"><button type="button" class="sq-sug-env">Enviar por email</button><button type="button" class="sq-sug-cop">Copiar sugestão</button><button type="button" class="sq-sug-canc">Cancelar</button></div>';
  coluna.insertBefore(painel, coluna.firstChild);
  var $ = function (s) { return painel.querySelector(s); }, ajuda = $('#sq-sug-ajuda'), estado = $('#sq-sug-estado'), sel = $('#sq-sug-sub'), desc = $('#sq-sug-desc'), subw = $('#sq-sug-subw');

  function opcoes() { var l = tipo === 'linha' ? SUB_LINHA : SUB_LOCAL; sel.innerHTML = l.map(function (n) { return '<option>' + esc(n) + '</option>'; }).join(''); subw.hidden = tipo === 'problema'; $('label[for=sq-sug-sub]').textContent = tipo === 'linha' ? 'Que tipo de percurso?' : 'Que tipo de local?'; }
  function texto() {
    ajuda.textContent = tipo === 'linha' ? 'Toca ou clica no mapa para marcar os pontos do percurso, por ordem. Com o teclado, move o mapa e usa "Marcar o centro do mapa".' : 'Toca ou clica no mapa no sítio exato. Com o teclado, move o mapa e usa "Marcar o centro do mapa".';
    if (!pts.length) estado.textContent = 'Ainda sem localização marcada.';
    else estado.textContent = tipo === 'linha' ? pts.length + (pts.length === 1 ? ' ponto marcado' : ' pontos marcados') + (pts.length > 1 ? ', cerca de ' + (comprimento() >= 1000 ? (comprimento() / 1000).toFixed(1).replace('.', ',') + ' km' : Math.round(comprimento() / 10) * 10 + ' m') : '') + '.' : 'Local marcado.';
  }
  function marca(ll) { if (tipo === 'linha') { if (pts.length < 400) pts.push(ll); } else pts = [ll]; desenha(); texto(); }
  map.on('click', function (e) { if (!aberto) return; map.closePopup(); marca(e.latlng); });
  painel.addEventListener('change', function (e) { if (e.target.name !== 'sq-sug-tipo') return; tipo = e.target.value; if (tipo !== 'linha' && pts.length > 1) pts = [pts[pts.length - 1]]; opcoes(); desenha(); texto(); });
  painel.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var a = b.getAttribute('data-a');
    if (a === 'centro') marca(map.getCenter());
    else if (a === 'desfazer') { pts.pop(); desenha(); texto(); }
    else if (a === 'limpar') { pts = []; desenha(); texto(); }
    else if (b.classList.contains('sq-sug-x') || b.classList.contains('sq-sug-canc')) fechar(true);
    else if (b.classList.contains('sq-sug-env')) enviar();
    else if (b.classList.contains('sq-sug-cop')) copiar();
  });

  function abrirPainel() {
    aberto = true; coluna.classList.add('sq-sug-on'); painel.hidden = false; map.doubleClickZoom.disable(); map.getContainer().classList.add('sq-sug-modo');
    if (!map.hasLayer(g)) g.addTo(map); desenha(); texto(); var r = $('input[type=radio]:checked'); if (r) r.focus({ preventScroll: true });
  }
  function fechar(limpa) {
    aberto = false; coluna.classList.remove('sq-sug-on'); painel.hidden = true; map.doubleClickZoom.enable(); map.getContainer().classList.remove('sq-sug-modo');
    if (limpa) { pts = []; g.clearLayers(); desc.value = ''; }
    if (!abrir.hidden) abrir.focus();
  }
  // só no ecrã inteiro e no computador (cartão ao lado do mapa): no telemóvel desenhar num mapa pequeno seria demasiado complicado
  var mqPc = window.matchMedia('(min-width: 980px)');
  opcoes();
  var guardado = false;   // ao sair do ecrã inteiro, a sugestão fica guardada e reaparece quando se volta
  function aplicarPc() {
    var pc = corpoMapa.classList.contains('sq-cheio-corpo') && mqPc.matches;
    abrir.hidden = !pc;
    if (!pc) {
      if (aberto || pts.length || desc.value.trim()) guardado = true;
      if (aberto) { aberto = false; coluna.classList.remove('sq-sug-on'); painel.hidden = true; map.doubleClickZoom.enable(); map.getContainer().classList.remove('sq-sug-modo'); }
      if (map.hasLayer(g)) map.removeLayer(g);
    } else if (guardado) { guardado = false; abrirPainel(); }
  }
  abrir.addEventListener('click', function () { if (aberto) fechar(false); else abrirPainel(); });
  aplicarPc(); new MutationObserver(aplicarPc).observe(corpoMapa, { attributes: true, attributeFilter: ['class'] });
  if (mqPc.addEventListener) mqPc.addEventListener('change', aplicarPc); else mqPc.addListener(aplicarPc);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && aberto && painel.contains(document.activeElement)) fechar(false); });

  /* envio por email */
  function montar() {
    var d = desc.value.trim();
    if (!d && !pts.length) { estado.textContent = 'Escreve uma descrição ou marca um sítio no mapa antes de enviar.'; desc.focus(); return null; }
    var nomeTipo = tipo === 'linha' ? 'Percurso' : tipo === 'local' ? 'Local novo' : 'Problema', sub = tipo === 'problema' ? '' : sel.value, base = location.origin + location.pathname;
    var MAX = 1800, tol = 3, ll, geom, corpo, url;
    for (;;) {
      ll = tipo === 'linha' ? simplifica(pts, tol) : pts;
      geom = ll.length ? codifica(ll) : '';
      url = geom ? base + '#sugestao=' + encodeURIComponent(JSON.stringify({ t: tipo, k: sub, d: d.slice(0, 160), g: geom })) : '';
      corpo = 'Sugestão para o mapa do programa\n\nTipo: ' + nomeTipo + (sub ? ' (' + sub + ')' : '') + '\n\nDescrição:\n' + (d || '(sem descrição)') + '\n\n' +
        (url ? 'Ver no mapa:\n' + url + '\n\n' + (tipo === 'linha' ? 'Pontos do percurso (latitude, longitude):\n' : 'Localização (latitude, longitude):\n') + ll.map(function (p) { return p.lat.toFixed(5) + ', ' + p.lng.toFixed(5); }).join('\n') + '\n' : 'Sem localização marcada no mapa.\n');
      if (encodeURIComponent(corpo).length <= MAX || tol > 80 || tipo !== 'linha') break;
      tol *= 1.6;
    }
    if (encodeURIComponent(corpo).length > MAX) { corpo = corpo.slice(0, corpo.indexOf('Pontos do percurso')) + 'Os pontos seguem pelo link acima.\n'; }
    return { assunto: 'Sugestão para o mapa: ' + nomeTipo.toLowerCase(), corpo: corpo };
  }
  function enviar() {
    var m = montar(); if (!m) return;
    estado.textContent = 'A abrir o teu programa de email… Se não abrir, usa "Copiar sugestão" e cola-a numa mensagem para ' + EMAIL + '.';
    window.SQ.ultimoMail = 'mailto:' + EMAIL + '?subject=' + encodeURIComponent(m.assunto) + '&body=' + encodeURIComponent(m.corpo);
    location.href = window.SQ.ultimoMail;
  }
  function copiar() {
    var m = montar(); if (!m) return;
    var t = 'Para: ' + EMAIL + '\nAssunto: ' + m.assunto + '\n\n' + m.corpo;
    window.SQ.ultimaCopia = t;
    function ok() { estado.textContent = 'Sugestão copiada. Cola-a num email ou mensagem para ' + EMAIL + '.'; }
    function falha() {
      var ta = document.createElement('textarea'); ta.value = t; ta.setAttribute('readonly', ''); ta.style.cssText = 'position:fixed;top:0;left:0;opacity:0';
      document.body.appendChild(ta); ta.select(); var certo = false; try { certo = document.execCommand('copy'); } catch (e) {} document.body.removeChild(ta);
      if (certo) ok(); else estado.textContent = 'Não consegui copiar automaticamente. Seleciona a descrição e escreve para ' + EMAIL + '.';
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(ok, falha); else falha();
  }

  /* ver uma sugestão recebida (ligação #sugestao=…) */
  (function () {
    var m = /^#sugestao=(.+)$/.exec(location.hash); if (!m) return;
    var o; try { o = JSON.parse(decodeURIComponent(m[1])); } catch (e) { return; }
    if (!o || typeof o !== 'object') return;
    var ll = typeof o.g === 'string' ? descodifica(o.g) : [];
    if (!ll.length) return;
    var info = '<b>Sugestão de um visitante</b><br>' + esc((o.t === 'linha' ? 'Percurso' : o.t === 'local' ? 'Local novo' : 'Problema') + (o.k ? ' (' + String(o.k).slice(0, 60) + ')' : '')) + (o.d ? '<br>' + esc(String(o.d).slice(0, 160)) : '') + '<br><i>Ainda não faz parte do programa.</i>';
    var camada = (o.t === 'linha' && ll.length > 1) ? L.polyline(ll, { color: COR, weight: 5, dashArray: '8 7' }) : L.circleMarker(ll[0], { radius: 10, color: '#fff', weight: 2, fillColor: COR, fillOpacity: 1 });
    camada.addTo(map).bindPopup(info, { maxWidth: 260 });
    setTimeout(function () { map.fitBounds(L.latLngBounds(ll), { padding: [40, 40], maxZoom: 17 }); camada.openPopup(camada.getBounds ? camada.getBounds().getCenter() : undefined); }, 400);
  })();
})();
