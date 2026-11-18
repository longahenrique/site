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
    var s = (W - 20) / total, x = 10, svg = '', etiquetas = '', n = 0, nomesUs = [];
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
      if (w > 22 && nomesUs.indexOf(NOMES[tipo]) < 0) nomesUs.push(NOMES[tipo]);
      x += w;
    });
    return '<svg viewBox="0 0 ' + W + ' ' + (chao + 14) + '" role="img" aria-label="' + (nome || 'Perfil da rua') + '">' + svg + '</svg><p class="sq-leg-perfil">' + nomesUs.join(' · ') + '</p>';
  }
  var P = {
    mata: '<rect width="640" height="250" fill="#e6f1f4"/><path d="M0 170 Q160 140 320 160 T640 150 V250 H0Z" fill="#d7c48f"/><path d="M0 205 Q200 190 640 200 V250 H0Z" fill="#efe1b8"/>' + [60, 140, 230, 330, 420, 520, 590].map(function (x, i) { var h = 70 + (i % 3) * 18; return '<rect x="' + (x - 3) + '" y="' + (175 - h * 0.55) + '" width="6" height="' + (h * 0.55) + '" fill="#6d5a43"/><ellipse cx="' + x + '" cy="' + (175 - h * 0.6) + '" rx="' + (38 - i % 2 * 8) + '" ry="16" fill="' + (i % 2 ? '#3f7f4c' : '#4c9159') + '"/>'; }).join('') + '<circle cx="300" cy="196" r="5" fill="#c0504d"/><rect x="296" y="200" width="8" height="18" rx="3" fill="#c0504d"/><circle cx="330" cy="198" r="5" fill="#3a6ea5"/><rect x="326" y="202" width="8" height="16" rx="3" fill="#3a6ea5"/>',
    varzea: '<rect width="640" height="250" fill="#e4f0f5"/><path d="M0 150 Q160 125 320 140 T640 135 V250 H0Z" fill="#b9d7a0"/><path d="M0 190 Q320 170 640 188 V250 H0Z" fill="#9cc58a"/><path d="M-10 215 C120 170 200 225 320 192 S520 170 650 205 L650 232 C520 200 440 238 320 218 S120 200 -10 240Z" fill="#6fb2d6"/><path d="M60 200 q40 -10 80 0 M380 205 q40 -10 90 0" stroke="#e8f4fb" stroke-width="3" fill="none" stroke-linecap="round"/>' + [90, 150, 470, 540, 600].map(function (x, i) { var h = 80 + (i % 3) * 16; return '<rect x="' + (x - 2.5) + '" y="' + (170 - h * 0.6) + '" width="5" height="' + (h * 0.6) + '" fill="#6d5a43"/><ellipse cx="' + x + '" cy="' + (170 - h * 0.65) + '" rx="13" ry="' + (24 + i % 2 * 6) + '" fill="' + (i % 2 ? '#5f9a52' : '#4f8a4b') + '"/>'; }).join('') + [210, 222, 234, 246, 258, 270, 410, 422, 434, 446].map(function (x, i) { return '<line x1="' + x + '" y1="224" x2="' + (x + (i % 3 - 1) * 4) + '" y2="' + (180 - (i % 4) * 7) + '" stroke="#7a8f3f" stroke-width="3" stroke-linecap="round"/><ellipse cx="' + (x + (i % 3 - 1) * 4) + '" cy="' + (178 - (i % 4) * 7) + '" rx="3" ry="7" fill="#8c6b3a"/>'; }).join('') + '<rect x="285" y="196" width="80" height="6" rx="2" fill="#8a6a43"/><rect x="290" y="202" width="5" height="16" fill="#6d5a43"/><rect x="355" y="202" width="5" height="16" fill="#6d5a43"/><line x1="285" y1="186" x2="365" y2="186" stroke="#6d5a43" stroke-width="3"/><circle cx="325" cy="178" r="5" fill="#3a6ea5"/><rect x="321" y="183" width="8" height="14" rx="3" fill="#3a6ea5"/><path d="M520 120 q10 -12 22 0 q12 -12 22 0" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M180 100 q8 -9 17 0 q9 -9 17 0" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>',
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
  var map = L.map(el, { zoomAnimation: !RM, fadeAnimation: !RM, markerZoomAnimation: !RM, scrollWheelZoom: true, zoomSnap: 0.5, minZoom: 10, maxZoom: 18, renderer: L.canvas({ padding: 0.5, tolerance: 8 }) });
  map.setView([38.51, -9.11], 11);
  if (L.Browser.mobile) map.dragging.disable();   // no telemóvel o mapa só se arrasta em ecrã inteiro; com um dedo a página desliza
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, className: 'sq-osm', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }).addTo(map);
  // A roda normal desloca a página; pinça no touchpad e Ctrl/Cmd + roda aproximam o mapa.
  el.addEventListener('wheel', function (e) { if (!(e.ctrlKey || e.metaKey) && !el.classList.contains('sq-cheio')) e.stopImmediatePropagation(); }, true);

  map.createPane('pZonas').style.zIndex = 410; map.createPane('pLinhas').style.zIndex = 430;
  var rZonas = L.canvas({ pane: 'pZonas', padding: 0.5, tolerance: 4 }), rLinhas = L.canvas({ pane: 'pLinhas', padding: 0.5, tolerance: 10 });
  var GR = { ciclo: L.featureGroup(), faixa: L.featureGroup(), bus: L.featureGroup(), vias: L.featureGroup(), hubs: L.featureGroup() };

  // Linhas de mobilidade (do mapa da mobilidade)
  var linhasObj = [];
  DADOS.linhas.forEach(function (l) {
    var g = l.camada === 'ativos' ? GR.ciclo : l.nome === 'Faixa BUS' ? GR.faixa : (l.camada === 'autocarro' || l.nome === 'Linha Azul') ? GR.bus : GR.vias;
    if (l.nome === 'Marginal de Sesimbra') return; // aparece como zona
    var cas = null;
    if (l.camada === 'ativos' || l.peso <= 6) cas = L.polyline(l.coords, { color: '#fff', weight: Math.min(l.peso, 12) + 4, opacity: 0.85, lineCap: 'round', lineJoin: 'round', pane: 'pLinhas', renderer: rLinhas, interactive: false }).addTo(g);
    var lin = L.polyline(l.coords, { color: l.cor, weight: Math.min(l.peso, 12), opacity: l.opacidade === undefined ? 0.9 : l.opacidade, dashArray: l.tracejado || null, lineCap: 'round', lineJoin: 'round', pane: 'pLinhas', renderer: rLinhas })
      .bindPopup('<b>' + esc(l.nome) + '</b><br>' + esc(l.texto), { maxWidth: 260 }).addTo(g);
    linhasObj.push({ l: l, c: cas, p: lin, w: Math.min(l.peso, 12), o: l.opacidade === undefined ? 0.9 : l.opacidade });
  });
  var gFixos = L.featureGroup().addTo(map);   // estações que já existem: marcadas desde o início
  DADOS.interfaces.forEach(function (i) {
    L.circleMarker(i.p, { radius: 7, color: '#fff', weight: 3, fillColor: '#1b1d22', fillOpacity: 1, pane: 'pLinhas', renderer: rLinhas })
      .bindPopup('<b>' + esc(i.nome) + '</b><br>' + esc(i.texto), { maxWidth: 260 })
      .bindTooltip(esc(i.nome), { direction: 'right', offset: [10, 0] }).addTo(i.existe ? gFixos : GR.hubs);
  });


  // Locais com ícone (parques, escolas, saúde...) e legenda
  var P24 = function (d) { return '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + d + '</svg>'; };
  var CATS = [
    { id: 'parque', nome: 'Parque ou jardim', cor: '#2f8f5b', svg: P24('<path d="M12 21v-6"/><path d="M12 15a5 5 0 1 0-4-8 4 4 0 0 0 0 7 4 4 0 0 0 4 1z" fill="currentColor"/>') },
    { id: 'escola', nome: 'Escola', cor: '#8a3fb0', svg: P24('<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>') },
    { id: 'saude', nome: 'Saúde', cor: '#c2362f', svg: P24('<path d="M12 5v14M5 12h14" stroke-width="3.5"/>') },
    { id: 'bombeiros', nome: 'Bombeiros', cor: '#d9531c', svg: P24('<path d="M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 1-9z" fill="currentColor"/>') },
    { id: 'policia', nome: 'Polícia (GNR, PSP)', cor: '#1b3a8c', svg: P24('<path d="M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z"/>') },
    { id: 'igreja', nome: 'Igreja ou capela', cor: '#6b5a3a', svg: P24('<path d="M12 2v6M9.5 4.5h5"/><path d="M5 21V12l7-4 7 4v9z"/><path d="M10 21v-5h4v5"/>') },
    { id: 'cultura', nome: 'Biblioteca, auditório, cultura', cor: '#b0306f', svg: P24('<path d="M4 5a2 2 0 0 1 2-1h13v16H6a2 2 0 0 0-2 1z"/><path d="M4 5v16"/>') },
    { id: 'servicos', nome: 'Serviços públicos (junta, loja do cidadão)', cor: '#4a5560', svg: P24('<path d="M3 10l9-6 9 6M5 10v9M9.5 10v9M14.5 10v9M19 10v9M3 21h18"/>') },
    { id: 'mercado', nome: 'Mercado e supermercado', cor: '#a8650d', svg: P24('<path d="M3 4h2l2 11h11l2-8H6"/><circle cx="9" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/>') },
    { id: 'desporto', nome: 'Desporto', cor: '#1e7a8c', svg: P24('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>') },
    { id: 'obra', nome: 'Em obra ou planeado (proposta)', cor: '#c2570c', svg: P24('<path d="M3 21h18M5 21v-3a7 7 0 0 1 14 0v3M12 8v4M9 11l1.5 2M15 11l-1.5 2"/>'), tracejado: true },
    { id: 'transporte', nome: 'Estação ou terminal', cor: '#1857d6', svg: P24('<rect x="5" y="3" width="14" height="14" rx="3"/><path d="M5 11h14M8 21l2-4M16 21l-2-4"/><circle cx="9" cy="14" r=".6" fill="currentColor"/><circle cx="15" cy="14" r=".6" fill="currentColor"/>') }
  ];
  var catPorId = {}; CATS.forEach(function (c) { catPorId[c.id] = c; });
  var gPontos = {}, rotPontos = [], uiOn = {}, catOn = {};
  CATS.forEach(function (c) { catOn[c.id] = true; });
  var camadasZona = {}, atual = null, legRender = function () {}, notasRender = function () {};
  function kmDe(c) { var t = 0; for (var i = 1; i < c.length; i++) t += map.distance(c[i - 1], c[i]); return t / 1000; }
  var ciclos = linhasObj.filter(function (o) { return o.l.camada === 'ativos'; });
  var kmCiclo = Math.round(ciclos.reduce(function (a, o) { return a + kmDe(o.l.coords); }, 0));
  // Camadas que a pessoa liga e desliga (o mapa abre vazio)
  var UI = [
    { id: 'ciclo', nome: 'Rede ciclável', cor: '#d6246e', nota: 'As ' + ciclos.length + ' ligações desenhadas somam cerca de ' + kmCiclo + ' km (valor aproximado, medido sobre o traçado do mapa) e fazem parte da rede ciclável de 40 km da proposta, com bicicletas partilhadas elétricas.' },
    { id: 'faixa', nome: 'Faixa BUS', cor: '#8fb0ec', nota: 'Faixas BUS onde há filas, para o autocarro não ficar preso no trânsito: entre Fernão Ferro e o Fogueteiro, na Av. João Paulo II, no Marco do Grilo e na EN10 entre a estação de Coina e o Posto da EN10, na Quinta do Conde, onde se perdem 8 dos 10 min de atraso na hora de ponta.' },
    { id: 'bus', nome: 'Autocarros', cor: '#1857d6', nota: 'Linha Azul: autocarro elétrico de alto nível de serviço, da vila de Sesimbra à estação do Fogueteiro, com 21,7 km e 16 estações, a cada 10 min na hora de ponta (expresso já em 2027; linha completa em 2031). Mais as circulares do Castelo e da Quinta do Conde, a cada 30 min, e o eixo Quinta do Conde–Coina, a cada 10 min na hora de ponta.' },
    { id: 'vias', nome: 'Novos acessos', cor: '#6d4bc2', nota: 'EN10 urbana na Quinta do Conde (≈3 km, com travessias, ciclovia e paragens) e variante ao Porto de Abrigo, para tirar os pesados da vila (traçado a estudar, ≈15 M€).' },
    { id: 'marginal', nome: 'Marginal', cor: '#d6246e', nota: 'Pedonalização progressiva da Marginal de Sesimbra: a frente de mar volta às pessoas, com menos ruído e poluição e mais vida no comércio e na restauração.' },
    { id: 'hubs', nome: 'Estações e hubs', cor: '#1b1d22', nota: 'Os novos hubs onde o autocarro se liga ao parque de estacionamento: Moagem, em Santana, e Alfarim. As estações de Coina e do Fogueteiro já existem e estão sempre marcadas.' },
    { id: 'obra', nome: 'Serviços e outros', cor: '#c2570c', nota: 'Serviços e obras propostos ou em curso, como a Loja do Cidadão, o novo quartel da GNR, o auditório, a nova biblioteca, o palácio da justiça de Sampaio e as 90 habitações da Cotovia.' }
  ];
  UI.forEach(function (u) { uiOn[u.id] = false; }); uiOn.existe = true;   // o que já existe está sempre no mapa
  function ligar(g, q) { if (q && !map.hasLayer(g)) map.addLayer(g); else if (!q && map.hasLayer(g)) map.removeLayer(g); }
  function visibilidade() {
    ['ciclo', 'faixa', 'bus', 'vias', 'hubs'].forEach(function (k) { ligar(GR[k], uiOn[k]); });
    CATS.forEach(function (c) { ligar(gPontos[c.id], c.id === 'obra' ? uiOn.obra : (uiOn.existe && catOn[c.id])); });
    if (camadasZona.marginal) ligar(camadasZona.marginal, uiOn.marginal || atual === 'marginal');
    legRender(); notasRender();
  }
  CATS.forEach(function (c) { gPontos[c.id] = L.layerGroup(); });
  (DADOS.pontos || []).concat(DADOS.manuais || []).forEach(function (p) {
    var c = catPorId[p.cat]; if (!c) return;
    var ic = L.divIcon({ className: 'sq-ico', html: '<span class="' + (c.tracejado ? 'tr' : '') + '" style="background:' + c.cor + '">' + c.svg + '</span>', iconSize: [26, 26], iconAnchor: [13, 13] });
    var m = L.marker(p.p, { icon: ic, title: p.nome, alt: p.nome, riseOnHover: true, keyboard: false });
    m.bindTooltip(esc(p.nome), { direction: 'top', offset: [0, -12], permanent: false, className: 'sq-nome-ponto' });
    m.bindPopup('<b>' + esc(p.nome) + '</b><br>' + esc(c.nome) + (p.texto ? '<br>' + esc(p.texto) : ''), { maxWidth: 240 });
    rotPontos.push({ m: m, cat: p.cat });
  });
  var MINZ = { obra: 12.5, saude: 12.5, bombeiros: 12.5, policia: 13, transporte: 12, escola: 13.5, parque: 13.5, servicos: 14.5, cultura: 14.5, igreja: 15, mercado: 15, desporto: 15.5 };
  var PRIO = ['obra', 'saude', 'bombeiros', 'policia', 'transporte', 'escola', 'parque', 'servicos', 'cultura', 'igreja', 'mercado', 'desporto'], DIST = 38;
  function nomesParques() {
    var z = map.getZoom(), ocupados = [];
    rotPontos.slice().sort(function (a, b) { return PRIO.indexOf(a.cat) - PRIO.indexOf(b.cat); }).forEach(function (r) {
      var g = gPontos[r.cat], ver = z >= (MINZ[r.cat] || 13);
      if (ver) { var q = map.latLngToContainerPoint(r.m.getLatLng()); ver = !ocupados.some(function (o) { return Math.abs(o.x - q.x) < DIST && Math.abs(o.y - q.y) < DIST; }); if (ver) ocupados.push(q); }
      if (ver && !g.hasLayer(r.m)) g.addLayer(r.m); else if (!ver && g.hasLayer(r.m)) g.removeLayer(r.m);
    });
  }
  map.on('zoomend', nomesParques); nomesParques();


  var Leg = L.Control.extend({ options: { position: 'bottomleft' }, onAdd: function () {
    var d = L.DomUtil.create('div', 'sq-leg'), b = L.DomUtil.create('button', 'sq-leg-btn', d), p = L.DomUtil.create('div', 'sq-leg-corpo', d);
    b.type = 'button'; b.setAttribute('aria-expanded', 'true'); b.setAttribute('aria-controls', 'sq-leg-corpo'); b.textContent = 'Esconder legenda'; p.id = 'sq-leg-corpo';
    L.DomEvent.disableClickPropagation(d); L.DomEvent.disableScrollPropagation(d);
    L.DomEvent.on(b, 'click', function () { var a = b.getAttribute('aria-expanded') === 'true'; b.setAttribute('aria-expanded', a ? 'false' : 'true'); p.hidden = a; b.textContent = a ? 'Mostrar legenda' : 'Esconder legenda'; });
    legRender = function () {
      var cheio = el.classList.contains('sq-cheio'), act = UI.filter(function (u) { return cheio || uiOn[u.id]; });
      var h = '<p class="sq-leg-t">' + (cheio ? 'O que ver no mapa' : 'Legenda') + '</p><ul class="sq-leg-l">' + act.map(function (u) {
        var sw = '<i class="l" style="background:' + u.cor + '"></i>';
        return '<li>' + (cheio ? '<label><input type="checkbox" data-ui="' + u.id + '"' + (uiOn[u.id] ? ' checked' : '') + '>' + sw + esc(u.nome) + '</label>' : sw + esc(u.nome)) + '</li>';
      }).join('') + '</ul>';
      if (uiOn.existe) h += '<p class="sq-leg-t">Já existe</p><ul class="sq-leg-l">' + CATS.filter(function (c) { return c.id !== 'obra'; }).map(function (c) { return '<li><label><input type="checkbox" data-cat="' + c.id + '"' + (catOn[c.id] ? ' checked' : '') + '><span class="sq-ico-l" style="background:' + c.cor + '">' + c.svg + '</span>' + esc(c.nome) + '</label></li>'; }).join('') + '</ul>';
      p.innerHTML = h;
    };
    L.DomEvent.on(p, 'change', function (e) { var t = e.target; if (!t.getAttribute) return; var u = t.getAttribute('data-ui'); if (u) { definir(u, t.checked); return; } var id = t.getAttribute('data-cat'); if (!id) return; catOn[id] = t.checked; visibilidade(); });
    if (el.clientWidth < 600) setTimeout(function () { b.click(); }, 0);
    return d;
  } });
  map.addControl(new Leg());
  function definir(id, on) {
    uiOn[id] = on; var cx = document.querySelector('#sq-camadas input[data-ui="' + id + '"]'); if (cx) cx.checked = on;
    visibilidade();
  }


  // Zonas: só aparece o contorno da localidade do cartão escolhido
  var gZona = L.featureGroup().addTo(map);
  DADOS.zonas.forEach(function (z) {
    var cor = corCamada[z.camada], camada, estilo = { color: cor, weight: 3, opacity: 0.95, fillColor: cor, fillOpacity: 0.16, pane: 'pZonas', renderer: rZonas, interactive: false };
    if (z.geo && z.geo.linha) camada = L.polyline(z.geo.linha, { color: cor, weight: 10, opacity: 0.85, lineCap: 'round', pane: 'pZonas', renderer: rZonas, interactive: false });
    else if (z.limite) camada = L.polygon(z.limite, estilo);
    else if (z.retangulo) camada = L.rectangle(z.retangulo, estilo);
    else if (z.poligono) camada = L.polygon(z.poligono, estilo);
    else camada = L.circle(z.centro, L.extend({ radius: z.raio }, estilo));
    camadasZona[z.id] = camada;
  });
  var limites = L.latLngBounds([]);
  linhasObj.forEach(function (o) { limites.extend(o.p.getBounds()); });
  DADOS.interfaces.forEach(function (i) { limites.extend(i.p); });
  Object.keys(camadasZona).forEach(function (k) { var c = camadasZona[k]; limites.extend(c instanceof L.Circle ? c.getLatLng().toBounds(c.getRadius() * 2) : c.getBounds()); });
  function verTudo() { map.fitBounds(limites, { padding: [24, 24] }); }
  verTudo();
  var Ctl = L.Control.extend({ options: { position: 'topright' }, onAdd: function () {
    var d = L.DomUtil.create('div', 'leaflet-bar sq-ctl'), b = L.DomUtil.create('button', 'sq-vertudo', d), f = L.DomUtil.create('button', 'sq-vertudo sq-cheio-btn', d);
    b.type = 'button'; b.textContent = 'Ver tudo'; f.type = 'button'; f.textContent = 'Ecrã inteiro'; f.setAttribute('aria-pressed', 'false');
    L.DomEvent.disableClickPropagation(d); L.DomEvent.on(b, 'click', function () { map.closePopup(); verTudo(); });
    function cheio(on) {
      el.classList.toggle('sq-cheio', on); document.documentElement.classList.toggle('sq-trava', on);
      f.textContent = on ? 'Sair do ecrã inteiro' : 'Ecrã inteiro'; f.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (on) el.setAttribute('aria-modal', 'true'); else el.removeAttribute('aria-modal');
      // o resto da página fica inerte (leitores de ecrã e teclado ficam só no mapa)
      var no = el; while (no && no !== document.body) { var pai = no.parentElement; if (pai) [].forEach.call(pai.children, function (irmao) { if (irmao !== no) { if (on) irmao.setAttribute('inert', ''); else irmao.removeAttribute('inert'); } }); no = pai; }
      if (L.Browser.mobile) { if (on) map.dragging.enable(); else map.dragging.disable(); }
      legRender(); setTimeout(function () { map.invalidateSize(); if (on) verTudo(); }, 60); f.focus();
    }
    L.DomEvent.on(f, 'click', function () { cheio(!el.classList.contains('sq-cheio')); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && el.classList.contains('sq-cheio')) cheio(false); });
    return d;
  } });
  map.addControl(new Ctl());

  // Cartão pequeno para o ecrã inteiro
  var mini = L.DomUtil.create('div', 'sq-mini', el); mini.hidden = true; L.DomEvent.disableClickPropagation(mini); L.DomEvent.disableScrollPropagation(mini);
  function miniAtualizar(z, il) {
    var ilu = il.tipo === 'perfil' ? ILU.perfil(il.amanha, 'Perfil de ' + z.nome + ' com a proposta') : ILU.paisagem(il.variante, z.nome);
    mini.innerHTML = '<button type="button" class="sq-mini-x" aria-label="Fechar o resumo">×</button><div class="sq-mini-ilu">' + ilu + '</div><h3>' + esc(z.nome) + '</h3><ul>' + z.medidas.slice(0, 3).map(function (m) { return '<li>' + esc(m.t) + '</li>'; }).join('') + '</ul>';
    mini.hidden = false; mini.setAttribute('data-fechado', 'n');
    mini.querySelector('.sq-mini-x').addEventListener('click', function () { mini.hidden = true; });
  }
  // Cartões das localidades (setas para a esquerda e para a direita)
  var postal = document.getElementById('sq-postal'), nav = document.getElementById('sq-nav');
  var ORDEM = ['vila', 'marginal', 'santana', 'sampaio', 'cotovia', 'zambujal', 'alfarim', 'meco', 'lagoa', 'mata', 'azoia', 'espichel', 'arrabida', 'qconde', 'varzea'].filter(function (id) { return camadasZona[id]; });
  DADOS.zonas.forEach(function (z) { if (ORDEM.indexOf(z.id) < 0) ORDEM.push(z.id); });
  var idx = 0, contaEl = null;
  function zonaDe(id) { return DADOS.zonas.filter(function (x) { return x.id === id; })[0]; }
  function cartao(id) {
    var z = zonaDe(id); if (!z) return; idx = ORDEM.indexOf(id);
    if (contaEl) contaEl.textContent = z.nome + ', ' + (idx + 1) + ' de ' + ORDEM.length;
    var il = z.ilustracao, html = '<div class="ilustra">';
    if (il.tipo === 'perfil') {
      html += '<div class="sq-alternar" role="group" aria-label="Hoje ou proposta"><button type="button" data-v="hoje" aria-pressed="false">Hoje</button><button type="button" data-v="amanha" aria-pressed="true">Proposta</button></div><div class="desenho">' + ILU.perfil(il.amanha, 'Perfil de ' + z.nome + ' com a proposta') + '</div><p class="nota-ilu">' + esc(z.perfilNome ? 'Perfil da ' + z.perfilNome + ', ilustrativo.' : 'Perfil da rua, ilustrativo.') + '</p>';
    } else html += ILU.paisagem(il.variante, z.nome);
    html += '</div><div class="conteudo"><p class="camada">' + esc(nomeCamada[z.camada]) + '</p><h3>' + esc(z.nome) + '</h3><p class="frase">' + esc(z.frase) + '</p><ul class="sq-medidas">' +
      z.medidas.map(function (m) { return '<li>' + esc(m.t) + '</li>'; }).join('') + '</ul><button type="button" class="sq-ver-mapa" data-zona="' + id + '">Ver no mapa</button></div>';
    postal.innerHTML = html;
    [].forEach.call(postal.querySelectorAll('.sq-alternar button'), function (b) {
      b.addEventListener('click', function () {
        postal.querySelector('.desenho').innerHTML = ILU.perfil(il[b.dataset.v], 'Perfil de ' + z.nome + (b.dataset.v === 'hoje' ? ' hoje' : ' com a proposta'));
        [].forEach.call(postal.querySelectorAll('.sq-alternar button'), function (o) { o.setAttribute('aria-pressed', o === b ? 'true' : 'false'); });
      });
    });
    return z;
  }
  function escolher(id, voar) {
    var z = cartao(id); if (!z) return;
    if (atual && camadasZona[atual] && gZona.hasLayer(camadasZona[atual])) gZona.removeLayer(camadasZona[atual]);
    atual = id; var c = camadasZona[id];
    if (id === 'marginal' && map.hasLayer(c)) map.removeLayer(c);
    gZona.addLayer(c); visibilidade(); miniAtualizar(z, z.ilustracao);
    if (voar) { if (RM) map.fitBounds(c.getBounds(), { padding: [90, 90], maxZoom: 15, animate: false }); else map.flyToBounds(c.getBounds(), { padding: [90, 90], maxZoom: 15, duration: 0.6 }); }
  }
  function passo(d) { escolher(ORDEM[(idx + d + ORDEM.length) % ORDEM.length], true); }
  if (nav) {
    var seta = function (d, rot) { var b = document.createElement('button'); b.type = 'button'; b.className = 'sq-seta'; b.setAttribute('aria-label', rot); b.innerHTML = '<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="' + (d < 0 ? 'M15 5l-7 7 7 7' : 'M9 5l7 7-7 7') + '"/></svg>'; b.addEventListener('click', function () { passo(d); }); return b; };
    contaEl = document.createElement('p'); contaEl.className = 'sr'; contaEl.setAttribute('aria-live', 'polite');
    nav.appendChild(seta(-1, 'Localidade anterior')); nav.appendChild(contaEl); nav.appendChild(seta(1, 'Localidade seguinte'));
  }

  // Menu de camadas (por cima do mapa)
  var fs = document.getElementById('sq-camadas');
  UI.forEach(function (u) {
    var lab = document.createElement('label'); lab.className = 'sq-chip';
    var inp = document.createElement('input'); inp.type = 'checkbox'; inp.checked = false; inp.setAttribute('data-ui', u.id);
    inp.addEventListener('change', function () { definir(u.id, inp.checked); });
    var cor = document.createElement('span'); cor.className = 'cor'; cor.style.background = u.cor;
    lab.appendChild(inp); lab.appendChild(cor); lab.appendChild(document.createTextNode(u.nome)); fs.appendChild(lab);
  });
  [['Marcar tudo', true], ['Limpar', false]].forEach(function (x) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'sq-todos'; b.textContent = x[0];
    b.addEventListener('click', function () { UI.forEach(function (u) { uiOn[u.id] = x[1]; var cx = fs.querySelector('input[data-ui="' + u.id + '"]'); if (cx) cx.checked = x[1]; }); visibilidade(); });
    fs.appendChild(b);
  });
  var notas = document.getElementById('sq-notas');
  notasRender = function () {
    if (!notas) return; var act = UI.filter(function (u) { return uiOn[u.id]; });
    notas.innerHTML = act.map(function (u) { return '<p style="border-left-color:' + u.cor + '"><b>' + esc(u.nome) + '.</b> ' + esc(u.nota) + '</p>'; }).join('');
  };

  // Lista de locais (alternativa ao mapa)
  (function () {
    var cont = document.getElementById('sq-lista'); if (!cont) return;
    var tudo = (DADOS.pontos || []).concat(DADOS.manuais || []), h = '';
    CATS.forEach(function (c) {
      var xs = tudo.filter(function (p) { return p.cat === c.id; }); if (!xs.length) return;
      h += '<h3>' + esc(c.nome) + '</h3><ul>' + xs.map(function (p) { return '<li>' + esc(p.nome) + (p.texto ? ' — ' + esc(p.texto) : '') + '</li>'; }).join('') + '</ul>';
    });
    cont.innerHTML = h;
  })();

  // Ligações "No mapa" do programa completo
  [].forEach.call(document.querySelectorAll('[data-zonas]'), function (sp) {
    var bs = sp.getAttribute('data-zonas').split(',').map(function (id) { var z = DADOS.zonas.filter(function (x) { return x.id === id; })[0]; return z && z.botao !== false ? '<button type="button" class="sq-ver" data-zona="' + id + '" aria-label="Ver ' + esc(z.nome) + ' no mapa">' + esc(z.nome) + '</button>' : ''; }).filter(Boolean);
    if (bs.length) sp.innerHTML = 'No mapa: ' + bs.join(' · ');
  });
  document.addEventListener('click', function (e) {
    var b = e.target.closest && e.target.closest('.sq-ver'); if (!b) return;
    escolher(b.getAttribute('data-zona'), true);
    document.getElementById('sq-mapa').scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' });
    postal.setAttribute('tabindex', '-1'); postal.focus({ preventScroll: true });
  });
  // Acordeão no telemóvel (igual ao de #programa)
  (function () {
    var mq = window.matchMedia('(max-width:600px)'), hs = document.querySelectorAll('.sq-completo .area h3[data-c]');
    function corpo(h) { return document.getElementById(h.getAttribute('data-c')); }
    function alternar(b, h) { var o = b.getAttribute('aria-expanded') !== 'true'; b.setAttribute('aria-expanded', o ? 'true' : 'false'); corpo(h).hidden = !o; }
    function aplicar() { [].forEach.call(hs, function (h) {
      var t = h.querySelector('.acc-t'), b = h.querySelector('button');
      if (mq.matches) {
        if (!b) { b = document.createElement('button'); b.type = 'button'; b.className = 'acc-btn'; b.setAttribute('aria-controls', h.getAttribute('data-c')); b.addEventListener('click', function () { alternar(b, h); }); b.appendChild(t); h.appendChild(b); }
        b.setAttribute('aria-expanded', 'false'); corpo(h).hidden = true;
      } else { if (b) { h.appendChild(t); h.removeChild(b); } corpo(h).hidden = false; }
    }); }
    aplicar(); if (mq.addEventListener) mq.addEventListener('change', aplicar); else mq.addListener(aplicar);
  })();
  document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.sq-ver-mapa'); if (!b) return; escolher(b.getAttribute('data-zona'), true); el.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' }); });
  window.SQ = { escolher: escolher, mapa: map };
  cartao(ORDEM[0]); visibilidade();
})();
