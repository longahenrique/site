/* ===== Ilustrações ===== */
var ILU = (function () {
  var NOMES = { passeio: 'passeio', estac: 'estacionamento', carro: 'carros', areia: 'praia', esplanada: 'esplanada', arvores: 'árvores', peoes: 'a pé', ciclovia: 'ciclovia', bus: 'autocarro', berma: 'berma' };
  var CHAO = { passeio: '#d9d5cc', estac: '#7d828a', carro: '#6b7078', areia: '#efd9a7', esplanada: '#e3ddd0', arvores: '#9cc58a', peoes: '#e8e1d1', ciclovia: '#2f9e66', bus: '#c4473a', berma: '#cbbf9d' };
  function pessoa(x, y, s, c) { return '<circle cx="' + x + '" cy="' + (y - 1.55 * s) + '" r="' + (0.13 * s) + '" fill="' + c + '"/><rect x="' + (x - 0.16 * s) + '" y="' + (y - 1.4 * s) + '" width="' + (0.32 * s) + '" height="' + (1.4 * s) + '" rx="' + (0.12 * s) + '" fill="' + c + '"/>'; }
  function arvore(x, y, s) { return '<rect x="' + (x - 0.12 * s) + '" y="' + (y - 2.6 * s) + '" width="' + (0.24 * s) + '" height="' + (2.6 * s) + '" fill="#6d5a43"/><circle cx="' + x + '" cy="' + (y - 3.6 * s) + '" r="' + (1.5 * s) + '" fill="#4f9a5a"/><circle cx="' + (x - 0.8 * s) + '" cy="' + (y - 3.1 * s) + '" r="' + (1 * s) + '" fill="#5daa66"/><circle cx="' + (x + 0.8 * s) + '" cy="' + (y - 3.2 * s) + '" r="' + (1 * s) + '" fill="#468d50"/>'; }
  function carro(x, y, s, c) { return '<rect x="' + (x - 0.9 * s) + '" y="' + (y - 1.15 * s) + '" width="' + (1.8 * s) + '" height="' + (0.75 * s) + '" rx="' + (0.2 * s) + '" fill="' + c + '"/><rect x="' + (x - 0.65 * s) + '" y="' + (y - 1.5 * s) + '" width="' + (1.3 * s) + '" height="' + (0.45 * s) + '" rx="' + (0.15 * s) + '" fill="' + c + '" opacity=".8"/><rect x="' + (x - 0.8 * s) + '" y="' + (y - 0.42 * s) + '" width="' + (0.3 * s) + '" height="' + (0.42 * s) + '" fill="#2a2d33"/><rect x="' + (x + 0.5 * s) + '" y="' + (y - 0.42 * s) + '" width="' + (0.3 * s) + '" height="' + (0.42 * s) + '" fill="#2a2d33"/>'; }
  function autocarro(x, y, s) { return '<rect x="' + (x - 1.25 * s) + '" y="' + (y - 3.1 * s) + '" width="' + (2.5 * s) + '" height="' + (2.8 * s) + '" rx="' + (0.3 * s) + '" fill="#1857d6"/><rect x="' + (x - 1.05 * s) + '" y="' + (y - 2.8 * s) + '" width="' + (2.1 * s) + '" height="' + (1.1 * s) + '" rx="' + (0.15 * s) + '" fill="#cfe0ff"/><rect x="' + (x - 1.1 * s) + '" y="' + (y - 0.35 * s) + '" width="' + (0.4 * s) + '" height="' + (0.35 * s) + '" fill="#2a2d33"/><rect x="' + (x + 0.7 * s) + '" y="' + (y - 0.35 * s) + '" width="' + (0.4 * s) + '" height="' + (0.35 * s) + '" fill="#2a2d33"/>'; }
  function bicicleta(x, y, s) { return '<circle cx="' + x + '" cy="' + (y - 0.35 * s) + '" r="' + (0.33 * s) + '" fill="none" stroke="#1b1d22" stroke-width="' + (0.07 * s) + '"/>' + pessoa(x, y - 0.55 * s, s * 0.8, '#f2a33a'); }
  function guarda(x, y, s) { return '<line x1="' + (x - 0.6 * s) + '" y1="' + (y - 2.2 * s) + '" x2="' + x + '" y2="' + (y - 2.6 * s) + '" stroke="#e05a47" stroke-width="' + (0.5 * s) + '" stroke-linecap="round"/><line x1="' + x + '" y1="' + (y - 2.6 * s) + '" x2="' + (x + 0.6 * s) + '" y2="' + (y - 2.2 * s) + '" stroke="#f7c948" stroke-width="' + (0.5 * s) + '" stroke-linecap="round"/><line x1="' + x + '" y1="' + (y - 2.5 * s) + '" x2="' + x + '" y2="' + y + '" stroke="#6d5a43" stroke-width="' + (0.08 * s) + '"/>'; }
  var CORES_P = ['#3a6ea5', '#c0504d', '#7a5ca8', '#2e8b57', '#d98a1c', '#4a4f57'];
  function perfil(bandas, nome) {
    var W = 640, H = 250, chao = 205, total = bandas.reduce(function (a, b) { return a + b[1]; }, 0);
    var s = (W - 20) / total, x = 10, svg = '', etiquetas = '', n = 0;
    svg += '<rect x="0" y="' + chao + '" width="' + W + '" height="' + (H - chao) + '" fill="#f3efe6"/>';
    bandas.forEach(function (b) {
      var tipo = b[0], w = b[1] * s, cx = x + w / 2;
      svg += '<rect x="' + x + '" y="' + chao + '" width="' + w + '" height="12" fill="' + CHAO[tipo] + '"/>';
      if (tipo === 'carro' || tipo === 'estac') svg += carro(cx, chao, s, ['#8d949e', '#b3504a', '#4b6c9b'][n++ % 3]);
      else if (tipo === 'bus') svg += autocarro(cx, chao, s);
      else if (tipo === 'ciclovia') svg += bicicleta(cx, chao, s);
      else if (tipo === 'arvores') svg += arvore(cx, chao, s);
      else if (tipo === 'areia') { svg += guarda(x + w * 0.3, chao, s) + pessoa(x + w * 0.65, chao, s * 0.9, CORES_P[n++ % 6]); }
      else if (tipo === 'esplanada') { svg += guarda(x + w * 0.35, chao, s * 0.9) + pessoa(x + w * 0.7, chao, s * 0.85, CORES_P[n++ % 6]); }
      else if (tipo === 'peoes') { for (var k = 0; k < 3; k++) svg += pessoa(x + w * (0.2 + k * 0.3), chao, s * (0.95 - k * 0.1), CORES_P[n++ % 6]); }
      else if (tipo === 'passeio') svg += pessoa(cx, chao, s, CORES_P[n++ % 6]);
      if (w > 22) etiquetas += '<text x="' + cx + '" y="' + (chao + 30) + '" text-anchor="middle" font-size="12" fill="#5d6470" font-family="system-ui, sans-serif">' + NOMES[tipo] + '</text>';
      x += w;
    });
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + (nome || 'Perfil da rua') + '">' + svg + etiquetas + '</svg>';
  }
  var P = {
    mata: '<rect width="640" height="250" fill="#e6f1f4"/><path d="M0 170 Q160 140 320 160 T640 150 V250 H0Z" fill="#d7c48f"/><path d="M0 205 Q200 190 640 200 V250 H0Z" fill="#efe1b8"/>' + [60, 140, 230, 330, 420, 520, 590].map(function (x, i) { var h = 70 + (i % 3) * 18; return '<rect x="' + (x - 3) + '" y="' + (175 - h * 0.55) + '" width="6" height="' + (h * 0.55) + '" fill="#6d5a43"/><ellipse cx="' + x + '" cy="' + (175 - h * 0.6) + '" rx="' + (38 - i % 2 * 8) + '" ry="16" fill="' + (i % 2 ? '#3f7f4c' : '#4c9159') + '"/>'; }).join('') + '<circle cx="300" cy="196" r="5" fill="#c0504d"/><rect x="296" y="200" width="8" height="18" rx="3" fill="#c0504d"/><circle cx="330" cy="198" r="5" fill="#3a6ea5"/><rect x="326" y="202" width="8" height="16" rx="3" fill="#3a6ea5"/>',
    lagoa: '<rect width="640" height="250" fill="#e8f2f6"/><path d="M0 150 Q320 120 640 150 V250 H0Z" fill="#cfe0b8"/><ellipse cx="320" cy="190" rx="300" ry="38" fill="#7fb6d5"/><path d="M80 186 q30 -6 60 0 M380 196 q40 -6 80 0" stroke="#e8f4fb" stroke-width="3" fill="none"/>' + [[200, 80], [235, 92], [420, 70]].map(function (b) { return '<path d="M' + b[0] + ' ' + b[1] + ' q10 -10 20 0 q10 -10 20 0" stroke="#3b414c" stroke-width="2.5" fill="none"/>'; }).join('') + '<circle cx="560" cy="60" r="22" fill="#f6d77a"/>',
    espichel: '<rect width="640" height="250" fill="#20294a"/>' + Array.from({ length: 46 }, function (_, i) { return '<circle cx="' + ((i * 137) % 640) + '" cy="' + ((i * 59) % 140 + 8) + '" r="' + (i % 5 ? 1.2 : 2.2) + '" fill="#fff" opacity="' + (0.5 + (i % 3) * 0.2) + '"/>'; }).join('') + '<path d="M0 170 L360 160 L420 165 L470 250 H0Z" fill="#c8b07a"/><path d="M420 165 L470 250 H640 V215 Q560 205 470 210Z" fill="#2c4a72"/><rect x="250" y="128" width="40" height="34" fill="#ece4d0"/><path d="M246 128 L270 112 L294 128Z" fill="#b65c45"/><circle cx="120" cy="160" r="4" fill="#f2a33a"/><rect x="117" y="163" width="6" height="12" rx="2" fill="#f2a33a"/>',
    serra: '<rect width="640" height="250" fill="#e9f1f5"/><path d="M0 200 L120 110 L210 160 L330 70 L450 150 L540 100 L640 170 V250 H0Z" fill="#5d9a63"/><path d="M0 230 Q320 200 640 225 V250 H0Z" fill="#2c6e9e"/>' + [90, 160, 300, 360, 480, 560].map(function (x) { return '<circle cx="' + x + '" cy="' + (190 - (x % 70)) + '" r="14" fill="#3f7f4c"/>'; }).join('') + '<path d="M150 210 Q260 150 380 175" stroke="#f3efe6" stroke-width="3" stroke-dasharray="6 6" fill="none"/>',
    vila: '<rect width="640" height="250" fill="#e6f1f6"/><path d="M0 120 Q160 90 300 110 T640 100 V170 H0Z" fill="#9cc58a"/>' + [[90, 112], [150, 100], [205, 118], [260, 96], [330, 110], [390, 98], [450, 116], [510, 104]].map(function (h, i) { return '<rect x="' + h[0] + '" y="' + h[1] + '" width="48" height="' + (180 - h[1]) + '" fill="' + (i % 3 ? '#f7f2e6' : '#f1e3c4') + '" stroke="#d9cfb8"/><path d="M' + (h[0] - 3) + ' ' + h[1] + ' L' + (h[0] + 24) + ' ' + (h[1] - 14) + ' L' + (h[0] + 51) + ' ' + h[1] + 'Z" fill="#c4683f"/>'; }).join('') + '<rect x="0" y="178" width="640" height="18" fill="#efd9a7"/><rect x="0" y="196" width="640" height="54" fill="#5d9bc4"/><path d="M200 214 h70 l-10 14 h-50z" fill="#c0504d"/><line x1="235" y1="214" x2="235" y2="190" stroke="#4a4f57" stroke-width="2"/><path d="M420 220 h56 l-8 11 h-40z" fill="#3a6ea5"/>',
    recupera: '<rect width="640" height="250" fill="#eef4f1"/><path d="M0 180 Q320 160 640 175 V250 H0Z" fill="#c7b78a"/>' + [80, 150, 220, 300, 380, 450, 520, 590].map(function (x, i) { var s = 0.5 + (i % 4) * 0.2; return '<rect x="' + (x - 2) + '" y="' + (175 - 40 * s) + '" width="4" height="' + (40 * s) + '" fill="#6d5a43"/><circle cx="' + x + '" cy="' + (172 - 44 * s) + '" r="' + (16 * s) + '" fill="#5daa66"/>'; }).join('') + '<circle cx="320" cy="196" r="5" fill="#2e8b57"/><rect x="316" y="200" width="8" height="18" rx="3" fill="#2e8b57"/><path d="M300 222 h40" stroke="#6d5a43" stroke-width="3"/>'
  };
  function paisagem(v, nome) { return '<svg viewBox="0 0 640 250" role="img" aria-label="' + (nome ? 'Ilustração: ' + nome : 'Ilustração') + '">' + P[v] + '</svg>'; }
  return { perfil: perfil, paisagem: paisagem };
})();

/* ===== Mapa e postal ===== */
(function () {
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  var corCamada = {}; DADOS.camadas.forEach(function (c) { corCamada[c.id] = c.cor; });
  var nomeCamada = {}; DADOS.camadas.forEach(function (c) { nomeCamada[c.id] = c.nome; });
  function fontes(f) { return '<span class="sq-fontes">' + f.map(function (k) { return '<span class="sq-fonte ' + k + '">' + esc(DADOS.fontes[k]) + '</span>'; }).join('') + '</span>'; }

  var el = document.getElementById('sq-mapa');
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var map = L.map(el, { zoomAnimation: !RM, fadeAnimation: !RM, markerZoomAnimation: !RM, scrollWheelZoom: false, zoomSnap: 0.5, minZoom: 10, maxZoom: 16, renderer: L.canvas({ padding: 0.5, tolerance: 8 }) });
  map.setView([38.51, -9.11], 11);
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, className: 'sq-osm', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }).addTo(map);
  map.on('click focus', function () { map.scrollWheelZoom.enable(); });
  map.on('mouseout blur', function () { map.scrollWheelZoom.disable(); });

  var grupos = {}; DADOS.camadas.forEach(function (c) { grupos[c.id] = L.featureGroup().addTo(map); });

  // Linhas de mobilidade (do mapa da mobilidade)
  DADOS.linhas.forEach(function (l) {
    var g = l.camada === 'ativos' ? grupos.ativos : grupos.mobilidade;
    if (l.nome === 'Marginal de Sesimbra') return; // aparece como zona
    L.polyline(l.coords, { color: l.cor, weight: Math.min(l.peso, 12), opacity: l.opacidade === undefined ? 0.9 : l.opacidade, dashArray: l.tracejado || null, lineCap: 'round', lineJoin: 'round' })
      .bindPopup('<b>' + esc(l.nome) + '</b><br>' + esc(l.texto), { maxWidth: 260 }).addTo(g);
  });
  DADOS.interfaces.forEach(function (i) {
    L.circleMarker(i.p, { radius: 7, color: '#fff', weight: 3, fillColor: '#1b1d22', fillOpacity: 1 })
      .bindPopup('<b>' + esc(i.nome) + '</b><br>' + esc(i.texto), { maxWidth: 260 })
      .bindTooltip(esc(i.nome), { direction: 'right', offset: [10, 0] }).addTo(grupos.mobilidade);
  });

  // Zonas
  var camadasZona = {}, rotulos = {}, atual = null;
  DADOS.zonas.forEach(function (z) {
    var cor = corCamada[z.camada], camada, estilo = { color: cor, weight: 2, opacity: 0.9, fillColor: cor, fillOpacity: 0.16 };
    if (z.geo && z.geo.linha) camada = L.polyline(z.geo.linha, { color: cor, weight: 10, opacity: 0.85, lineCap: 'round' });
    else if (z.poligono) camada = L.polygon(z.poligono, estilo);
    else camada = L.circle(z.centro, L.extend({ radius: z.raio }, estilo));
    camada.on('click', function () { escolher(z.id, false); });
    camada.addTo(grupos[z.camada]);
    camadasZona[z.id] = camada;
    var pos = z.rotulo || (z.centro) || camada.getBounds().getCenter();
    var r = L.marker(pos, { opacity: 0, interactive: false, keyboard: false, icon: L.divIcon({ className: '', iconSize: [1, 1] }) });
    r.bindTooltip(esc(z.nome), { permanent: true, direction: z.direcao || 'center', className: 'sq-rotulo', interactive: true });
    r.addTo(grupos[z.camada]);
    r.getTooltip().on('click', function () { escolher(z.id, false); });
    rotulos[z.id] = r;
  });
  function mostrarRotulos() { var zz = map.getZoom(); DADOS.zonas.forEach(function (z) { var e = rotulos[z.id].getTooltip().getElement(); if (e) e.style.display = (!z.minZoom || zz >= z.minZoom || z.id === atual) ? '' : 'none'; }); }
  map.on('zoomend', mostrarRotulos);

  var limites = L.featureGroup(Object.keys(grupos).map(function (k) { return grupos[k]; })).getBounds();
  function verTudo() { map.fitBounds(limites, { padding: [24, 24] }); }
  verTudo();
  var Ctl = L.Control.extend({ options: { position: 'topright' }, onAdd: function () {
    var d = L.DomUtil.create('div', 'leaflet-bar'), b = L.DomUtil.create('button', 'sq-vertudo', d);
    b.type = 'button'; b.textContent = 'Ver tudo';
    L.DomEvent.disableClickPropagation(d); L.DomEvent.on(b, 'click', function () { map.closePopup(); verTudo(); });
    return d;
  } });
  map.addControl(new Ctl());

  // Botões de lugares
  var lugares = document.getElementById('sq-lugares');
  DADOS.zonas.forEach(function (z) {
    var b = document.createElement('button'); b.type = 'button'; b.textContent = z.nome; b.dataset.id = z.id;
    b.addEventListener('click', function () { escolher(z.id, true); });
    lugares.appendChild(b);
  });

  // Postal
  var postal = document.getElementById('sq-postal');
  function escolher(id, voar) {
    var z = DADOS.zonas.filter(function (x) { return x.id === id; })[0]; if (!z) return;
    atual = id;
    Object.keys(rotulos).forEach(function (k) { var t = rotulos[k].getTooltip(); if (t && t.getElement()) t.getElement().classList.toggle('ativo', k === id); });
    Object.keys(camadasZona).forEach(function (k) { var c = camadasZona[k]; if (c.setStyle) c.setStyle(k === id ? { weight: c instanceof L.Polygon || c instanceof L.Circle ? 3.5 : 14, fillOpacity: 0.3 } : { weight: c instanceof L.Polygon || c instanceof L.Circle ? 2 : 10, fillOpacity: 0.16 }); });
    [].forEach.call(lugares.children, function (b) { b.setAttribute('aria-current', b.dataset.id === id ? 'true' : 'false'); });
    var il = z.ilustracao, html = '<div class="ilustra">';
    if (il.tipo === 'perfil') {
      html += '<div class="sq-alternar" role="group" aria-label="Hoje ou amanhã"><button type="button" data-v="hoje" aria-pressed="false">Hoje</button><button type="button" data-v="amanha" aria-pressed="true">Com o programa</button></div><div class="desenho">' + ILU.perfil(il.amanha, 'Perfil de ' + z.nome + ' com o programa') + '</div><p class="nota-ilu">' + esc(z.perfilNome ? 'Perfil da ' + z.perfilNome + ', ilustrativo.' : 'Perfil da rua, ilustrativo.') + '</p>';
    } else html += ILU.paisagem(il.variante, z.nome);
    html += '</div><div class="conteudo"><p class="camada">' + esc(nomeCamada[z.camada]) + '</p><h3>' + esc(z.nome) + '</h3><p class="frase">' + esc(z.frase) + '</p><ul class="sq-medidas">' +
      z.medidas.map(function (m) { return '<li>' + esc(m.t) + '<br>' + fontes(m.f) + '</li>'; }).join('') + '</ul></div>';
    postal.innerHTML = html;
    [].forEach.call(postal.querySelectorAll('.sq-alternar button'), function (b) {
      b.addEventListener('click', function () {
        postal.querySelector('.desenho').innerHTML = ILU.perfil(il[b.dataset.v], 'Perfil de ' + z.nome + (b.dataset.v === 'hoje' ? ' hoje' : ' com o programa'));
        [].forEach.call(postal.querySelectorAll('.sq-alternar button'), function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
      });
    });
    if (voar) { var c = camadasZona[id]; if (RM) map.fitBounds(c.getBounds(), { padding: [90, 90], maxZoom: 13.5, animate: false }); else map.flyToBounds(c.getBounds(), { padding: [90, 90], maxZoom: 13.5, duration: 0.6 }); }
    mostrarRotulos();
  }

  // Camadas
  var fs = document.getElementById('sq-camadas');
  DADOS.camadas.forEach(function (c) {
    var lab = document.createElement('label'); lab.className = 'sq-chip';
    var inp = document.createElement('input'); inp.type = 'checkbox'; inp.checked = true;
    inp.addEventListener('change', function () { if (inp.checked) map.addLayer(grupos[c.id]); else map.removeLayer(grupos[c.id]); if (atual) escolher(atual, false); });
    var cor = document.createElement('span'); cor.className = 'cor'; cor.style.background = c.cor;
    lab.appendChild(inp); lab.appendChild(cor); lab.appendChild(document.createTextNode(c.nome)); fs.appendChild(lab);
  });

  // Em todos os bairros
  document.getElementById('sq-grelha').innerHTML = DADOS.bairros.map(function (b) { return '<li><b>' + esc(b.t) + '</b>' + esc(b.d) + '<br>' + fontes(b.f) + '</li>'; }).join('');
  document.getElementById('sq-legenda').innerHTML = 'De onde vem cada medida: ' + Object.keys(DADOS.fontes).map(function (k) { return '<span class="sq-fonte ' + k + '">' + esc(DADOS.fontes[k]) + '</span>'; }).join(' ');
  document.getElementById('sq-data').textContent = DADOS.atualizadoCurto;
  document.getElementById('sq-nota').textContent = 'Proposta para discussão, atualizada a ' + DADOS.atualizado + '. As zonas e os traçados são indicativos; os perfis das ruas são ilustrações, não projetos.';

  // Ligações "No mapa" do programa completo
  [].forEach.call(document.querySelectorAll('[data-zonas]'), function (sp) {
    var bs = sp.getAttribute('data-zonas').split(',').map(function (id) { var z = DADOS.zonas.filter(function (x) { return x.id === id; })[0]; return z ? '<button type="button" class="sq-ver" data-zona="' + id + '" aria-label="Ver ' + esc(z.nome) + ' no mapa">' + esc(z.nome) + '</button>' : ''; }).filter(Boolean);
    if (bs.length) sp.innerHTML = 'No mapa: ' + bs.join(' · ');
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.sq-ver'); if (!b) return;
    escolher(b.getAttribute('data-zona'), true);
    document.getElementById('sq-mapa').scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' });
    postal.setAttribute('tabindex', '-1'); postal.focus({ preventScroll: true });
  });
  window.SQ = { escolher: escolher };
  escolher('marginal', false);
})();
