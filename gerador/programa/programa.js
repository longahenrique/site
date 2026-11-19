/* ===== Ilustrações ===== */
var ILU = (function () {
  var NOMES = { passeio: 'passeio', estac: 'estacionamento', carro: 'carros', areia: 'praia', esplanada: 'esplanada', esplanada0: 'esplanada', arvores: 'árvores', peoes: 'passeio', ciclovia: 'ciclovia', bus: 'autocarro', busciclo: 'autocarro e bicicletas', berma: 'berma', terra: 'terra batida', bermaerva: 'berma', bermaarv: 'berma' };
  var CHAO = { passeio: '#d9d5cc', estac: '#7d828a', carro: '#6b7078', areia: '#efd9a7', esplanada: '#e3ddd0', esplanada0: '#e3ddd0', arvores: '#9cc58a', peoes: '#e8e1d1', ciclovia: '#2f9e66', bus: '#c4473a', busciclo: '#c4473a', berma: '#cbbf9d', terra: '#b08d5b', bermaerva: '#cbbf9d', bermaarv: '#cbbf9d' };
  function espinha(x, y, s, c) {   // carro estacionado de lado (visto de perfil), a entrar na espinha
    var L = 2.1 * s;
    return '<path d="M' + (x - L) + ' ' + (y - 0.35 * s) + ' L' + (x - L) + ' ' + (y - 0.85 * s) + ' Q' + (x - L) + ' ' + (y - 1.05 * s) + ' ' + (x - 1.7 * s) + ' ' + (y - 1.05 * s) + ' L' + (x - 1.05 * s) + ' ' + (y - 1.1 * s) + ' L' + (x - 0.55 * s) + ' ' + (y - 1.65 * s) + ' L' + (x + 0.7 * s) + ' ' + (y - 1.65 * s) + ' L' + (x + 1.3 * s) + ' ' + (y - 1.1 * s) + ' L' + (x + 1.8 * s) + ' ' + (y - 1.02 * s) + ' Q' + (x + L) + ' ' + (y - 0.95 * s) + ' ' + (x + L) + ' ' + (y - 0.7 * s) + ' L' + (x + L) + ' ' + (y - 0.35 * s) + ' Z" fill="' + c + '"/>' +
      '<path d="M' + (x - 0.4 * s) + ' ' + (y - 1.1 * s) + ' L' + (x - 0.05 * s) + ' ' + (y - 1.5 * s) + ' L' + (x + 0.6 * s) + ' ' + (y - 1.5 * s) + ' L' + (x + 1.05 * s) + ' ' + (y - 1.1 * s) + ' Z" fill="#dfeaf2" opacity=".85"/>' +
      '<circle cx="' + (x - 1.3 * s) + '" cy="' + (y - 0.35 * s) + '" r="' + (0.38 * s) + '" fill="#2b2f36"/><circle cx="' + (x + 1.3 * s) + '" cy="' + (y - 0.35 * s) + '" r="' + (0.38 * s) + '" fill="#2b2f36"/>' +
      '<circle cx="' + (x - 1.3 * s) + '" cy="' + (y - 0.35 * s) + '" r="' + (0.16 * s) + '" fill="#aab1ba"/><circle cx="' + (x + 1.3 * s) + '" cy="' + (y - 0.35 * s) + '" r="' + (0.16 * s) + '" fill="#aab1ba"/>';
  }
  function erva(x, y, s) { s *= 0.5; var d = ''; [-0.35, 0, 0.35].forEach(function (k, i) { d += '<path d="M' + (x + k * s) + ' ' + y + ' q' + ((k - 0.1) * s * 0.6) + ' ' + (-0.5 * s) + ' ' + (k * s * 0.8 - 0.1 * s) + ' ' + (-(0.8 + 0.2 * i) * s) + '" fill="none" stroke="#6f8f4a" stroke-width="' + (0.1 * s) + '" stroke-linecap="round"/>'; }); return d; }
  function pessoa(x, y, s, c) { return '<circle cx="' + x + '" cy="' + (y - 1.55 * s) + '" r="' + (0.13 * s) + '" fill="' + c + '"/><rect x="' + (x - 0.16 * s) + '" y="' + (y - 1.4 * s) + '" width="' + (0.32 * s) + '" height="' + (1.4 * s) + '" rx="' + (0.12 * s) + '" fill="' + c + '"/>'; }
  function arvore(x, y, s) { return '<rect x="' + (x - 0.12 * s) + '" y="' + (y - 2.6 * s) + '" width="' + (0.24 * s) + '" height="' + (2.6 * s) + '" fill="#6d5a43"/><circle cx="' + x + '" cy="' + (y - 3.6 * s) + '" r="' + (1.5 * s) + '" fill="#4f9a5a"/><circle cx="' + (x - 0.8 * s) + '" cy="' + (y - 3.1 * s) + '" r="' + (1 * s) + '" fill="#5daa66"/><circle cx="' + (x + 0.8 * s) + '" cy="' + (y - 3.2 * s) + '" r="' + (1 * s) + '" fill="#468d50"/>'; }
  function carro(x, y, s, c) { return '<rect x="' + (x - 0.9 * s) + '" y="' + (y - 1.15 * s) + '" width="' + (1.8 * s) + '" height="' + (0.75 * s) + '" rx="' + (0.2 * s) + '" fill="' + c + '"/><rect x="' + (x - 0.65 * s) + '" y="' + (y - 1.5 * s) + '" width="' + (1.3 * s) + '" height="' + (0.45 * s) + '" rx="' + (0.15 * s) + '" fill="' + c + '" opacity=".8"/><rect x="' + (x - 0.8 * s) + '" y="' + (y - 0.42 * s) + '" width="' + (0.3 * s) + '" height="' + (0.42 * s) + '" fill="#2a2d33"/><rect x="' + (x + 0.5 * s) + '" y="' + (y - 0.42 * s) + '" width="' + (0.3 * s) + '" height="' + (0.42 * s) + '" fill="#2a2d33"/>'; }
  function autocarro(x, y, s) { return '<rect x="' + (x - 1.25 * s) + '" y="' + (y - 3.1 * s) + '" width="' + (2.5 * s) + '" height="' + (2.8 * s) + '" rx="' + (0.3 * s) + '" fill="#1857d6"/><rect x="' + (x - 1.05 * s) + '" y="' + (y - 2.8 * s) + '" width="' + (2.1 * s) + '" height="' + (1.1 * s) + '" rx="' + (0.15 * s) + '" fill="#cfe0ff"/><rect x="' + (x - 1.1 * s) + '" y="' + (y - 0.35 * s) + '" width="' + (0.4 * s) + '" height="' + (0.35 * s) + '" fill="#2a2d33"/><rect x="' + (x + 0.7 * s) + '" y="' + (y - 0.35 * s) + '" width="' + (0.4 * s) + '" height="' + (0.35 * s) + '" fill="#2a2d33"/>'; }
  function bicicleta(x, y, s) { return '<circle cx="' + x + '" cy="' + (y - 0.35 * s) + '" r="' + (0.33 * s) + '" fill="none" stroke="#1b1d22" stroke-width="' + (0.07 * s) + '"/>' + pessoa(x, y - 0.55 * s, s * 0.8, '#f2a33a'); }
  function guarda(x, y, s) { return '<line x1="' + (x - 0.6 * s) + '" y1="' + (y - 2.2 * s) + '" x2="' + x + '" y2="' + (y - 2.6 * s) + '" stroke="#e05a47" stroke-width="' + (0.5 * s) + '" stroke-linecap="round"/><line x1="' + x + '" y1="' + (y - 2.6 * s) + '" x2="' + (x + 0.6 * s) + '" y2="' + (y - 2.2 * s) + '" stroke="#f7c948" stroke-width="' + (0.5 * s) + '" stroke-linecap="round"/><line x1="' + x + '" y1="' + (y - 2.5 * s) + '" x2="' + x + '" y2="' + y + '" stroke="#6d5a43" stroke-width="' + (0.08 * s) + '"/>'; }
  var CORES_P = ['#3a6ea5', '#c0504d', '#7a5ca8', '#2e8b57', '#d98a1c', '#4a4f57'];
  function perfil(bandas, nome) {
    var W = 640, H = 250, chao = 205, total = bandas.reduce(function (a, b) { return a + b[1]; }, 0);
    var s = (W - 20) / total, x = 10, svg = '', etiquetas = '', n = 0, nomesUs = [], runs = [];
    svg += '<rect x="0" y="' + chao + '" width="' + W + '" height="' + (H - chao) + '" fill="#f3efe6"/>';
    bandas.forEach(function (b) {
      var tipo = b[0], w = b[1] * s, cx = x + w / 2;
      svg += '<rect x="' + x + '" y="' + chao + '" width="' + w + '" height="12" fill="' + CHAO[tipo] + '"/>';
      if (tipo === 'carro') svg += carro(cx, chao, s, ['#8d949e', '#b3504a', '#4b6c9b'][n++ % 3]);
      else if (tipo === 'estac') svg += espinha(cx, chao, s, ['#8d949e', '#b3504a', '#4b6c9b'][n++ % 3]);
      else if (tipo === 'bus') svg += autocarro(cx, chao, s);
      else if (tipo === 'terra') svg += erva(x + w * 0.22, chao, s) + erva(x + w * 0.78, chao, s * 0.9);
      else if (tipo === 'bermaarv') svg += arvore(cx, chao, s * 0.9);
      else if (tipo === 'bermaerva') svg += erva(cx, chao, s * 0.8);
      else if (tipo === 'busciclo') svg += autocarro(x + w * 0.32, chao, s * 0.85) + bicicleta(x + w * 0.78, chao, s);
      else if (tipo === 'ciclovia') svg += bicicleta(cx, chao, s);
      else if (tipo === 'arvores') svg += arvore(cx, chao, s);
      else if (tipo === 'areia') { svg += guarda(x + w * 0.3, chao, s) + pessoa(x + w * 0.65, chao, s * 0.9, CORES_P[n++ % 6]); }
      else if (tipo === 'esplanada') { svg += guarda(x + w * 0.35, chao, s * 0.9) + pessoa(x + w * 0.7, chao, s * 0.85, CORES_P[n++ % 6]); }
      else if (tipo === 'esplanada0') svg += guarda(cx, chao, s * 0.9);   // só esplanada, sem gente: o passeio é tão estreito que não passa ninguém
      else if (tipo === 'peoes') { for (var k = 0; k < 3; k++) svg += pessoa(x + w * (0.2 + k * 0.3), chao, s * (0.95 - k * 0.1), CORES_P[n++ % 6]); }
      else if (tipo === 'passeio') svg += pessoa(cx, chao, s, CORES_P[n++ % 6]);
      if (w > 22 && nomesUs.indexOf(NOMES[tipo]) < 0) nomesUs.push(NOMES[tipo]);
      if (runs.length && runs[runs.length - 1].t === NOMES[tipo]) runs[runs.length - 1].w += w; else runs.push({ t: NOMES[tipo], x: x, w: w });
      x += w;
    });
    var CURTO = { estacionamento: 'estac.', 'autocarro e bicicletas': 'autocarro/bici' }, FS = 16, larg = function (t, f) { return t.length * 0.56 * f; };
    runs.forEach(function (r) { r.e = r.t; if (larg(r.e, FS) > r.w * 0.96 && CURTO[r.e]) r.e = CURTO[r.e]; });
    runs.forEach(function (r) { var f = Math.min(FS, r.w * 0.96 / (r.e.length * 0.56)); if (f >= 12 && f < FS) FS = f; });   // um só tamanho de letra em todo o perfil
    runs.forEach(function (r) {
      if (larg(r.e, FS) <= r.w * 0.98) etiquetas += '<text x="' + (r.x + r.w / 2) + '" y="' + (chao + 34) + '" text-anchor="middle" font-size="' + FS.toFixed(1) + '" font-weight="700" fill="#2b3128" font-family="Archivo,Arial,sans-serif">' + r.e + '</text>';
    });
    var topo = Math.max(0, Math.floor(chao - 5.4 * s - 12));
    return '<svg viewBox="0 ' + topo + ' ' + W + ' ' + (chao + 46 - topo) + '" role="img" aria-label="' + (nome || 'Perfil da rua') + ': ' + nomesUs.join(', ') + '">' + svg + etiquetas + '</svg>';
  }
  var P = {
    mata: '<rect width="640" height="250" fill="#f6ecd2"/><circle cx="520" cy="70" r="28" fill="#f6d77a"/><path d="M0 150 Q160 120 320 145 T640 130 V250 H0Z" fill="#6f9a62"/><path d="M0 185 Q200 170 640 180 V250 H0Z" fill="#4f8a55"/>' + [30, 95, 170, 250, 390, 470, 560, 620].map(function (x, i) { return pinheiro(x, 105 + (i % 3) * 12, 1.5 - (i % 2) * 0.3); }).join('') + '<path d="M250 250 Q300 215 330 195 Q360 178 420 172" stroke="#e7d3a0" stroke-width="30" fill="none" stroke-linecap="round"/><circle cx="318" cy="200" r="5" fill="#c0504d"/><rect x="314" y="204" width="8" height="18" rx="3" fill="#c0504d"/><circle cx="346" cy="192" r="5" fill="#3a6ea5"/><rect x="342" y="196" width="8" height="16" rx="3" fill="#3a6ea5"/>',
    varzea: '<rect width="640" height="250" fill="#e4f0f5"/><path d="M0 150 Q160 125 320 140 T640 135 V250 H0Z" fill="#b9d7a0"/><path d="M0 190 Q320 170 640 188 V250 H0Z" fill="#9cc58a"/><path d="M-10 215 C120 170 200 225 320 192 S520 170 650 205 L650 232 C520 200 440 238 320 218 S120 200 -10 240Z" fill="#6fb2d6"/><path d="M60 200 q40 -10 80 0 M380 205 q40 -10 90 0" stroke="#e8f4fb" stroke-width="3" fill="none" stroke-linecap="round"/>' + [90, 150, 470, 540, 600].map(function (x, i) { var h = 80 + (i % 3) * 16; return '<rect x="' + (x - 2.5) + '" y="' + (170 - h * 0.6) + '" width="5" height="' + (h * 0.6) + '" fill="#6d5a43"/><ellipse cx="' + x + '" cy="' + (170 - h * 0.65) + '" rx="13" ry="' + (24 + i % 2 * 6) + '" fill="' + (i % 2 ? '#5f9a52' : '#4f8a4b') + '"/>'; }).join('') + [210, 222, 234, 246, 258, 270, 410, 422, 434, 446].map(function (x, i) { return '<line x1="' + x + '" y1="224" x2="' + (x + (i % 3 - 1) * 4) + '" y2="' + (180 - (i % 4) * 7) + '" stroke="#7a8f3f" stroke-width="3" stroke-linecap="round"/><ellipse cx="' + (x + (i % 3 - 1) * 4) + '" cy="' + (178 - (i % 4) * 7) + '" rx="3" ry="7" fill="#8c6b3a"/>'; }).join('') + '<rect x="285" y="196" width="80" height="6" rx="2" fill="#8a6a43"/><rect x="290" y="202" width="5" height="16" fill="#6d5a43"/><rect x="355" y="202" width="5" height="16" fill="#6d5a43"/><line x1="285" y1="186" x2="365" y2="186" stroke="#6d5a43" stroke-width="3"/><circle cx="325" cy="178" r="5" fill="#3a6ea5"/><rect x="321" y="183" width="8" height="14" rx="3" fill="#3a6ea5"/><path d="M520 120 q10 -12 22 0 q12 -12 22 0" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/><path d="M180 100 q8 -9 17 0 q9 -9 17 0" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>',
    lagoa: '<rect width="640" height="250" fill="#e8f2f6"/><path d="M0 150 Q320 120 640 150 V250 H0Z" fill="#efd9a7"/><ellipse cx="320" cy="190" rx="300" ry="38" fill="#7fb6d5"/><path d="M80 186 q30 -6 60 0 M380 196 q40 -6 80 0" stroke="#e8f4fb" stroke-width="3" fill="none"/>' + [[200, 80], [235, 92], [420, 70]].map(function (b) { return '<path d="M' + b[0] + ' ' + b[1] + ' q10 -10 20 0 q10 -10 20 0" stroke="#3b414c" stroke-width="2.5" fill="none"/>'; }).join('') + '<circle cx="560" cy="60" r="22" fill="#f6d77a"/>',
    espichel: '<rect width="640" height="250" fill="#20294a"/>' + Array.from({ length: 46 }, function (_, i) { return '<circle cx="' + ((i * 137) % 640) + '" cy="' + ((i * 59) % 140 + 8) + '" r="' + (i % 5 ? 1.2 : 2.2) + '" fill="#fff" opacity="' + (0.5 + (i % 3) * 0.2) + '"/>'; }).join('') + '<path d="M0 170 L360 160 L420 165 L470 250 H0Z" fill="#c8b07a"/><path d="M420 165 L470 250 H640 V215 Q560 205 470 210Z" fill="#2c4a72"/><rect x="250" y="128" width="40" height="34" fill="#ece4d0"/><path d="M246 128 L270 112 L294 128Z" fill="#b65c45"/><circle cx="120" cy="160" r="4" fill="#f2a33a"/><rect x="117" y="163" width="6" height="12" rx="2" fill="#f2a33a"/>',
    serra: '<rect width="640" height="250" fill="#e9f1f5"/><path d="M0 200 L120 110 L210 160 L330 70 L450 150 L540 100 L640 170 V250 H0Z" fill="#5d9a63"/><path d="M0 230 Q320 200 640 225 V250 H0Z" fill="#2c6e9e"/>' + [90, 160, 300, 360, 480, 560].map(function (x) { return '<circle cx="' + x + '" cy="' + (190 - (x % 70)) + '" r="14" fill="#3f7f4c"/>'; }).join('') + '<path d="M150 210 Q260 150 380 175" stroke="#f3efe6" stroke-width="3" stroke-dasharray="6 6" fill="none"/>',
    vila: '<rect width="640" height="250" fill="#e6f1f6"/><path d="M0 120 Q160 90 300 110 T640 100 V170 H0Z" fill="#9cc58a"/>' + [[90, 112], [150, 100], [205, 118], [260, 96], [330, 110], [390, 98], [450, 116], [510, 104]].map(function (h, i) { return '<rect x="' + h[0] + '" y="' + h[1] + '" width="48" height="' + (180 - h[1]) + '" fill="' + (i % 3 ? '#f7f2e6' : '#f1e3c4') + '" stroke="#d9cfb8"/><path d="M' + (h[0] - 3) + ' ' + h[1] + ' L' + (h[0] + 24) + ' ' + (h[1] - 14) + ' L' + (h[0] + 51) + ' ' + h[1] + 'Z" fill="#c4683f"/>'; }).join('') + '<rect x="0" y="178" width="640" height="18" fill="#efd9a7"/><rect x="0" y="196" width="640" height="54" fill="#5d9bc4"/><path d="M200 214 h70 l-10 14 h-50z" fill="#c0504d"/><line x1="235" y1="214" x2="235" y2="190" stroke="#4a4f57" stroke-width="2"/><path d="M420 220 h56 l-8 11 h-40z" fill="#3a6ea5"/>',
    recupera: '<rect width="640" height="250" fill="#eef4f1"/><path d="M0 180 Q320 160 640 175 V250 H0Z" fill="#c7b78a"/>' + [80, 150, 220, 300, 380, 450, 520, 590].map(function (x, i) { var s = 0.5 + (i % 4) * 0.2; return '<rect x="' + (x - 2) + '" y="' + (175 - 40 * s) + '" width="4" height="' + (40 * s) + '" fill="#6d5a43"/><circle cx="' + x + '" cy="' + (172 - 44 * s) + '" r="' + (16 * s) + '" fill="#5daa66"/>'; }).join('') + '<circle cx="320" cy="196" r="5" fill="#2e8b57"/><rect x="316" y="200" width="8" height="18" rx="3" fill="#2e8b57"/><path d="M300 222 h40" stroke="#6d5a43" stroke-width="3"/>'
  };
  function casa(x, y, w, h, cor, tel) { return '<rect x="' + x + '" y="' + y + '" width="' + w + '" height="' + h + '" fill="' + cor + '"/>' + (tel ? '<path d="M' + (x - 3) + ' ' + y + ' L' + (x + w / 2) + ' ' + (y - w * 0.32) + ' L' + (x + w + 3) + ' ' + y + 'Z" fill="' + tel + '"/>' : '') + '<rect x="' + (x + w * 0.18) + '" y="' + (y + h * 0.3) + '" width="' + (w * 0.18) + '" height="' + (h * 0.22) + '" fill="#7aa7c7"/><rect x="' + (x + w * 0.6) + '" y="' + (y + h * 0.55) + '" width="' + (w * 0.2) + '" height="' + (h * 0.45) + '" fill="#8a6a4a"/>'; }
  function pinheiro(x, y, k) { return '<rect x="' + (x - 2) + '" y="' + y + '" width="4" height="' + (38 * k) + '" fill="#6d5a43"/><ellipse cx="' + x + '" cy="' + (y - 2) + '" rx="' + (24 * k) + '" ry="' + (12 * k) + '" fill="#4f8a55"/>'; }
  function janelas(x, y, w, h, c, l) { var o = ''; for (var i = 0; i < c; i++) for (var j = 0; j < l; j++) o += '<rect x="' + (x + 6 + i * (w - 12) / c) + '" y="' + (y + 8 + j * (h - 14) / l) + '" width="' + ((w - 12) / c - 5) + '" height="' + ((h - 14) / l - 6) + '" fill="#9cc3dc"/>'; return o; }
  var P2 = {
    variante: '<rect width="640" height="250" fill="#e6f1f6"/><path d="M0 120 Q120 100 220 118 T400 96 T640 84 V250 H0Z" fill="#b9d7a0"/><path d="M0 205 Q320 192 640 200 V250 H0Z" fill="#9cc58a"/><rect x="0" y="158" width="150" height="92" fill="#8fc0dc"/><path d="M20 190 q18 -6 36 0 M80 214 q18 -6 36 0" stroke="#e8f4fb" stroke-width="3" fill="none"/><path d="M60 170 l22 0 l-4 12 h-14z" fill="#b8693f"/><rect x="68" y="150" width="3" height="20" fill="#555"/>' +
      '<path d="M150 214 C240 200 300 160 380 150 S520 120 650 96" stroke="#7b7f86" stroke-width="26" fill="none" stroke-linecap="round"/><path d="M150 214 C240 200 300 160 380 150 S520 120 650 96" stroke="#fff" stroke-width="2" stroke-dasharray="10 9" fill="none"/>' +
      '<rect x="330" y="108" width="62" height="30" rx="3" fill="#e8e2d2" stroke="#8f8a7a"/><rect x="392" y="116" width="24" height="22" rx="3" fill="#c4473a"/><circle cx="346" cy="141" r="6" fill="#222"/><circle cx="372" cy="141" r="6" fill="#222"/><circle cx="404" cy="141" r="6" fill="#222"/>' + pinheiro(250, 128, 0.9) + pinheiro(560, 70, 0.8) + pinheiro(600, 78, 0.7) + casa(190, 150, 50, 36, '#f7f2e6', '#b8693f'),
    acessocoina: '<rect width="640" height="250" fill="#e6f1f6"/><path d="M0 120 Q160 95 330 110 T640 100 V250 H0Z" fill="#b9d7a0"/><path d="M0 232 Q320 222 640 228 V250 H0Z" fill="#9cc58a"/>' +
      '<path d="M0 214 C200 206 400 190 640 166" stroke="#7b7f86" stroke-width="22" fill="none" stroke-linecap="round"/><path d="M0 214 C200 206 400 190 640 166" stroke="#fff" stroke-width="2" stroke-dasharray="10 9" fill="none"/>' +
      casa(40, 118, 46, 30, '#f7f2e6', '#b8693f') + casa(110, 122, 42, 28, '#f3ead6', '#a85a3a') + pinheiro(585, 92, 0.8) + pinheiro(625, 96, 0.65) +
      '<rect x="260" y="102" width="70" height="28" rx="3" fill="#e8e2d2" stroke="#8f8a7a"/><rect x="268" y="110" width="12" height="12" fill="#8fc0dc"/><rect x="288" y="110" width="12" height="12" fill="#8fc0dc"/><rect x="308" y="110" width="12" height="12" fill="#8fc0dc"/>' +
      autocarro(300, 214, 15) + bicicleta(430, 196, 15),
    santana: '<rect width="640" height="250" fill="#e6f1f6"/><path d="M0 160 Q200 130 420 150 T640 140 V250 H0Z" fill="#b9d7a0"/><path d="M0 208 Q320 194 640 205 V250 H0Z" fill="#9cc58a"/>' +
      '<rect x="60" y="80" width="150" height="112" fill="#e9d6b0"/><path d="M52 80 L135 46 L218 80Z" fill="#b8693f"/>' + janelas(60, 84, 150, 80, 5, 2) + '<rect x="115" y="150" width="40" height="42" fill="#8a6a4a"/><rect x="218" y="40" width="22" height="152" fill="#d9c49a"/><rect x="214" y="34" width="30" height="10" fill="#b8693f"/><path d="M229 34 q10 -14 -2 -26" stroke="#9aa3ad" stroke-width="5" fill="none" stroke-linecap="round"/>' +
      '<rect x="300" y="170" width="190" height="34" fill="#cfcabb"/><path d="M310 187 H480" stroke="#fff" stroke-width="2" stroke-dasharray="10 8"/><rect x="420" y="110" width="4" height="62" fill="#555"/><rect x="404" y="92" width="36" height="22" rx="3" fill="#1857d6"/><text x="422" y="108" font-size="14" font-weight="700" text-anchor="middle" fill="#fff" font-family="sans-serif">P</text>' + autocarro(350, 204, 12) +
      pinheiro(520, 120, 0.9) + '<rect x="540" y="196" width="60" height="5" rx="2" fill="#8a6a4a"/>' + bicicleta(580, 232, 12) + bicicleta(520, 232, 12) + '<path d="M0 234 Q320 220 640 232" stroke="#d6246e" stroke-width="5" stroke-dasharray="2 9" stroke-linecap="round" fill="none"/>',
    qconde: '<rect width="640" height="250" fill="#e6f1f6"/><path d="M0 150 Q200 120 400 140 T640 130 V250 H0Z" fill="#b9d7a0"/><path d="M0 205 Q320 190 640 202 V250 H0Z" fill="#9cc58a"/>' +
      '<rect x="60" y="92" width="230" height="100" fill="#f1e3c6"/><rect x="54" y="84" width="242" height="10" fill="#b8693f"/>' + janelas(60, 92, 230, 100, 9, 2) + '<rect x="156" y="150" width="38" height="42" fill="#8a6a4a"/><rect x="96" y="60" width="158" height="22" rx="3" fill="#1857d6"/><text x="175" y="76" font-size="13" font-weight="700" text-anchor="middle" fill="#fff" font-family="sans-serif">Escola</text>' +
      casa(330, 138, 62, 54, '#f4e9d2', '#c0694a') + casa(405, 146, 54, 46, '#ecd5b0', '#b8693f') + casa(475, 136, 66, 56, '#fbf6ea', '#c0694a') + casa(556, 148, 56, 44, '#f4e9d2', '#b8693f') +
      pinheiro(318, 150, 0.8) + '<rect x="0" y="206" width="640" height="14" fill="#d9d3c4"/>' + autocarro(120, 224, 11) + '<path d="M0 238 H640" stroke="#d6246e" stroke-width="5" stroke-dasharray="2 9" stroke-linecap="round" fill="none"/>',
    cotovia: '<rect width="640" height="250" fill="#e6f1f6"/><path d="M0 200 Q320 186 640 198 V250 H0Z" fill="#cfe0b8"/>' +
      [[40, 90], [190, 70], [340, 100]].map(function (b, i) { return '<rect x="' + b[0] + '" y="' + b[1] + '" width="120" height="' + (205 - b[1]) + '" fill="' + ['#f1e3c6', '#ecd5b0', '#f4e9d2'][i] + '"/><rect x="' + (b[0] - 4) + '" y="' + (b[1] - 8) + '" width="128" height="8" fill="#b8693f"/>' + janelas(b[0], b[1], 120, 205 - b[1], 4, Math.round((205 - b[1]) / 30)); }).join('') +
      '<rect x="500" y="40" width="6" height="165" fill="#f2b632"/><path d="M440 48 H590 M500 48 L470 82 M500 48 L540 82" stroke="#f2b632" stroke-width="5" fill="none"/><path d="M560 48 V90" stroke="#555" stroke-width="2"/><rect x="552" y="90" width="16" height="12" fill="#e05a47"/><rect x="470" y="130" width="90" height="75" fill="#e9dcc0"/>' + janelas(470, 130, 90, 75, 3, 2) +
      [[620, 175]].map(function () { return ''; }).join('') + '<rect x="0" y="205" width="640" height="14" fill="#d9d3c4"/>',
    sampaio: '<rect width="640" height="250" fill="#e6f1f6"/><path d="M0 190 Q160 110 330 120 T640 170 V250 H0Z" fill="#a9cf94"/><path d="M0 215 Q320 195 640 212 V250 H0Z" fill="#8cbb7a"/>' +
      '<rect x="60" y="120" width="170" height="60" fill="#f1e3c6"/><rect x="56" y="112" width="178" height="9" fill="#c0504d"/>' + janelas(60, 120, 170, 60, 7, 1) + '<rect x="140" y="150" width="20" height="30" fill="#8a6a4a"/><path d="M245 120 V84" stroke="#555" stroke-width="3"/><path d="M245 84 h28 v16 h-28z" fill="#1857d6"/>' +
      '<path d="M360 118 L430 92 L500 118Z" fill="#e9dcc0"/><rect x="368" y="118" width="124" height="52" fill="#f4ecd8"/>' + [376, 396, 416, 436, 456, 476].map(function (x) { return '<rect x="' + x + '" y="120" width="8" height="50" fill="#fffaf0"/>'; }).join('') + '<rect x="360" y="170" width="140" height="8" fill="#d7ccb0"/>' +
      casa(540, 150, 44, 36, '#f4e9d2', '#c0694a') + casa(590, 160, 38, 30, '#ecd5b0', '#b8693f') + pinheiro(310, 150, 0.9) + '<path d="M0 232 Q300 214 640 230" stroke="#d6246e" stroke-width="5" stroke-dasharray="2 9" stroke-linecap="round" fill="none"/>',
    alfarim: '<rect width="640" height="250" fill="#e6f1f6"/><path d="M0 150 Q320 130 640 148 V250 H0Z" fill="#b9d7a0"/><path d="M0 200 Q320 185 640 198 V250 H0Z" fill="#9cc58a"/>' +
      [[70, 150, 1], [150, 156, 0.85], [230, 148, 1.05], [300, 158, 0.8]].map(function (t) { return '<rect x="' + (t[0] - 3) + '" y="' + t[1] + '" width="6" height="' + (40 * t[2]) + '" fill="#6d5a43"/><circle cx="' + t[0] + '" cy="' + (t[1] - 6) + '" r="' + (26 * t[2]) + '" fill="#4f9560"/>'; }).join('') +
      '<rect x="110" y="196" width="46" height="6" rx="2" fill="#8a6a4a"/>' + casa(400, 138, 60, 50, '#f4e9d2', '#c0694a') + casa(470, 146, 50, 42, '#ecd5b0', '#b8693f') +
      '<rect x="560" y="120" width="4" height="86" fill="#555"/><rect x="544" y="104" width="36" height="22" rx="3" fill="#1857d6"/><text x="562" y="120" font-size="14" font-weight="700" text-anchor="middle" fill="#fff" font-family="sans-serif">P</text>' + autocarro(500, 214, 11) + '<path d="M0 226 Q320 212 640 226" stroke="#d6246e" stroke-width="5" stroke-dasharray="2 9" stroke-linecap="round" fill="none"/>',
    meco: '<rect width="640" height="250" fill="#eaf4f8"/><rect y="112" width="640" height="60" fill="#7fb6d5"/><path d="M0 130 q40 -6 80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0 t80 0" stroke="#e8f4fb" stroke-width="3" fill="none"/><path d="M0 172 Q160 150 330 166 T640 160 V250 H0Z" fill="#efdcaa"/><path d="M0 215 Q320 196 640 212 V250 H0Z" fill="#e3c98a"/>' +
      pinheiro(70, 62, 1.1) + pinheiro(150, 76, 0.9) + pinheiro(540, 60, 1.15) + pinheiro(600, 78, 0.85) +
      '<path d="M300 196 V156" stroke="#6d5a43" stroke-width="3"/><path d="M270 156 q30 -30 60 0z" fill="#e05a47"/><path d="M420 200 V164" stroke="#6d5a43" stroke-width="3"/><path d="M394 164 q26 -26 52 0z" fill="#f7c948"/>',
    azoia: '<rect width="640" height="250" fill="#e8f2f7"/><circle cx="540" cy="52" r="24" fill="#f7d36b"/><path d="M0 120 Q200 96 400 112 T640 104 V160 H0Z" fill="#bcd9a4"/><rect y="150" width="640" height="26" fill="#7fb6d5" opacity=".55"/><path d="M0 170 Q200 146 400 164 T640 158 V250 H0Z" fill="#a9cf94"/><path d="M0 214 Q320 196 640 210 V250 H0Z" fill="#92bf7e"/>' +
      casa(60, 142, 62, 42, '#fbf6ea', '#c0694a') + casa(140, 150, 54, 38, '#f4e9d2', '#b8693f') + casa(250, 140, 66, 46, '#fbf6ea', '#c0694a') + casa(440, 148, 56, 40, '#f4e9d2', '#c0694a') + casa(510, 142, 62, 44, '#fbf6ea', '#b8693f') +
      '<rect x="336" y="136" width="62" height="50" fill="#fbf6ea"/><path d="M332 136 L367 112 L402 136Z" fill="#c0694a"/><rect x="361" y="150" width="12" height="36" fill="#8a6a4a"/><rect x="354" y="124" width="26" height="9" fill="#fff"/><path d="M367 118 v14 M360 125 h14" stroke="#c2362f" stroke-width="4"/>' +
      pinheiro(30, 150, 0.8) + pinheiro(610, 156, 0.75) + '<path d="M0 232 Q320 216 640 230" stroke="#cfc6b0" stroke-width="8" fill="none"/>'
  };
  Object.keys(P2).forEach(function (k) { P[k] = P2[k]; });
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
  var posBusca = function () {}, corpo = document.querySelector('.sq-corpo');
  var RM = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var map = L.map(el, { zoomAnimation: !RM, fadeAnimation: !RM, markerZoomAnimation: !RM, scrollWheelZoom: true, zoomControl: false, zoomSnap: 0.5, minZoom: 10, maxZoom: 18, renderer: L.canvas({ padding: 0.5, tolerance: 8 }) });
  L.control.zoom({ zoomInTitle: 'Aproximar o mapa', zoomOutTitle: 'Afastar o mapa' }).addTo(map);
  map.on('popupopen', function (e) { var x = e.popup.getElement(); x = x && x.querySelector('.leaflet-popup-close-button'); if (x) { x.setAttribute('aria-label', 'Fechar'); x.setAttribute('title', 'Fechar'); } });
  map.setView([38.51, -9.11], 11);
  if (L.Browser.mobile) map.dragging.disable();   // no telemóvel o mapa só se arrasta em ecrã inteiro; com um dedo a página desliza
  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, className: 'sq-osm', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>' }).addTo(map);
  // A roda normal desloca a página; pinça no touchpad e Ctrl/Cmd + roda aproximam o mapa.
  // a roda do rato aproxima e afasta o mapa quando o cursor está sobre ele (a página rola fora do mapa)

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
      .addTo(g);
    var uiId = l.camada === 'ativos' ? 'ciclo' : l.nome === 'Faixa BUS' ? 'faixa' : (l.camada === 'autocarro' || l.nome === 'Linha Azul') ? 'bus' : 'vias';
    lin.bindPopup('<b>' + esc(l.nome) + '</b><br>' + esc(l.texto) + ligNota(uiId), { maxWidth: 260 });
    linhasObj.push({ l: l, c: cas, p: lin, w: Math.min(l.peso, 12), o: l.opacidade === undefined ? 0.9 : l.opacidade });
  });
  var gFixos = L.featureGroup().addTo(map);   // estações que já existem: marcadas desde o início
  var ifaceObj = [];
  DADOS.interfaces.forEach(function (i) {
    var cm = L.circleMarker(i.p, { radius: 7, color: '#fff', weight: 3, fillColor: '#1b1d22', fillOpacity: 1, pane: 'pLinhas', renderer: rLinhas })
      .bindPopup('<b>' + esc(i.nome) + '</b><br>' + esc(i.texto) + (i.existe ? '' : ligNota('hubs')), { maxWidth: 260 })
      .bindTooltip(esc(i.nome), { direction: 'right', offset: [10, 0] }).addTo(i.existe ? gFixos : GR.hubs);
    ifaceObj.push({ i: i, m: cm });
  });


  // Locais com ícone (parques, escolas, saúde...) e legenda
  var P24 = function (d) { return '<svg viewBox="0 0 24 24" width="16" height="16" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + d + '</svg>'; };
  var CATS = [
    { id: 'parque', nome: 'Parque ou jardim', cor: '#2f8f5b', svg: P24('<path d="M12 21v-6"/><path d="M12 15a5 5 0 1 0-4-8 4 4 0 0 0 0 7 4 4 0 0 0 4 1z" fill="currentColor"/>') },
    { id: 'escola', nome: 'Escola', cor: '#8a3fb0', svg: P24('<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>') },
    { id: 'saude', nome: 'Saúde', cor: '#c2362f', svg: P24('<path d="M12 5v14M5 12h14" stroke-width="3.5"/>') },
    { id: 'bombeiros', nome: 'Bombeiros', cor: '#d9531c', svg: P24('<path d="M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 1-9z" fill="currentColor"/>') },
    { id: 'policia', nome: 'Polícia', cor: '#1b3a8c', svg: P24('<path d="M12 3l7 3v6c0 4-3 7-7 9-4-2-7-5-7-9V6z"/>') },
    { id: 'igreja', nome: 'Igreja ou capela', cor: '#6b5a3a', svg: P24('<path d="M12 2v6M9.5 4.5h5"/><path d="M5 21V12l7-4 7 4v9z"/><path d="M10 21v-5h4v5"/>') },
    { id: 'cultura', nome: 'Biblioteca, auditório, cultura', cor: '#b0306f', svg: P24('<path d="M4 5a2 2 0 0 1 2-1h13v16H6a2 2 0 0 0-2 1z"/><path d="M4 5v16"/>') },
    { id: 'servicos', nome: 'Serviços públicos', cor: '#4a5560', svg: P24('<path d="M3 10l9-6 9 6M5 10v9M9.5 10v9M14.5 10v9M19 10v9M3 21h18"/>') },
    { id: 'mercado', nome: 'Mercado e supermercado', cor: '#a8650d', svg: P24('<path d="M3 4h2l2 11h11l2-8H6"/><circle cx="9" cy="19" r="1.5"/><circle cx="17" cy="19" r="1.5"/>') },
    { id: 'desporto', nome: 'Desporto', cor: '#1e7a8c', svg: P24('<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>') },
    { id: 'obra', nome: 'Em obra ou planeado', cor: '#c2570c', svg: P24('<path d="M3 21h18M5 21v-3a7 7 0 0 1 14 0v3M12 8v4M9 11l1.5 2M15 11l-1.5 2"/>'), tracejado: true },
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
    { id: 'ciclo', nome: 'Rede ciclável', cor: '#d6246e', nota: 'As ' + ciclos.length + ' ligações desenhadas somam cerca de ' + kmCiclo + ' km (valor aproximado, medido sobre o traçado do mapa) e fazem parte da rede ciclável de 40 km da proposta, com bicicletas e trotinetes partilhadas.' },
    { id: 'faixa', nome: 'Faixa BUS', cor: '#b87a00', nota: 'Faixas BUS onde há filas, para o autocarro não ficar preso no trânsito: entre Fernão Ferro e o Fogueteiro, na Av. João Paulo II, no Marco do Grilo e na EN10, desde a estação de Coina até ao fim da EN10 urbana, na Quinta do Conde, onde se perdem 8 dos 10 min de atraso na hora de ponta.' },
    { id: 'bus', nome: 'Autocarros', cor: '#1857d6', nota: 'Linha Azul: autocarro elétrico de alto nível de serviço, da vila de Sesimbra à estação do Fogueteiro, com 21,7 km e 16 estações, a cada 10 min na hora de ponta (expresso já em 2027; linha completa em 2031). Mais a circular do Castelo, a cada 30 min, e a ligação Casal do Sapo–Coina, prevista no Plano de Mobilidade Urbana Sustentável (PMUS). As linhas que já existem, como a circular da Quinta do Conde e o eixo Quinta do Conde–Coina, não estão desenhadas.' },
    { id: 'vias', nome: 'Novos acessos', cor: '#6d4bc2', nota: 'EN10 urbana na Quinta do Conde (≈3 km, com travessias, faixas de autocarro e bicicletas, e paragens), o acesso da rotunda de Coina à Rua Luís de Camões (traçado indicativo, sem projeto aprovado), a Estrada dos Almocreves, com ciclovia, e a variante ao Porto de Abrigo, para tirar os pesados da vila (traçado a estudar, ≈15 M€).' },
    { id: 'marginal', nome: 'Marginal', cor: '#0e7c7b', nota: 'Pedonalização progressiva da Marginal de Sesimbra: a frente de mar volta às pessoas, com menos ruído e poluição e mais vida no comércio e na restauração.' },
    { id: 'hubs', nome: 'Estações e hubs', cor: '#1b1d22', nota: 'Os novos hubs onde o autocarro se liga ao parque de estacionamento: Moagem, em Santana, e Alfarim. As estações de Coina e do Fogueteiro já existem e estão sempre marcadas.' },
    { id: 'obra', nome: 'Serviços e outros', cor: '#c2570c', nota: 'Serviços e obras propostos ou em curso, como a Loja do Cidadão, o novo quartel da GNR, o auditório, a nova escola secundária da Quinta do Conde, o Spot Jovem no Parque da Vila, a nova biblioteca e o palácio da justiça de Sampaio.' }
  ];
  UI.forEach(function (u) { uiOn[u.id] = false; }); uiOn.existe = true;   // o que já existe está sempre no mapa
  function irNota(id) {   // só quando a pessoa pede (ligação no balão): leva até à frase explicativa
    var n = document.getElementById('sq-notas'); if (!n) return;
    var x = n.querySelector('p[data-ui="' + id + '"]'); if (x) x.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'center' });
  }
  function ligNota(id) { return '<br><button type="button" class="sq-pop-ir" data-ui="' + id + '">Saber mais</button>'; }
  document.addEventListener('click', function (e) { var b = e.target.closest && e.target.closest('.sq-pop-ir'); if (b) irNota(b.getAttribute('data-ui')); });
  function ligar(g, q) { if (q && !map.hasLayer(g)) map.addLayer(g); else if (!q && map.hasLayer(g)) map.removeLayer(g); }
  function aplicarFiltro() {
    linhasObj.forEach(function (o) {
      var uiId = o.l.camada === 'ativos' ? 'ciclo' : o.l.nome === 'Faixa BUS' ? 'faixa' : (o.l.camada === 'autocarro' || o.l.nome === 'Linha Azul') ? 'bus' : 'vias', g = GR[uiId];
      var ver = !filtro || (filtro.solo ? filtro.solo.indexOf(o.l.nome) >= 0 : o.l.coords.some(function (q) { return filtro.b.contains(q); }));
      var seg = o.l.coords;
      if (false) {   // as linhas que passam pela zona mostram-se completas, sem corte   // só o troço que passa pela zona (com um ponto de folga de cada lado)
        seg = []; var cur = null, cs = o.l.coords;
        cs.forEach(function (q, k) {
          var dentro = filtro.b.contains(q) || (k > 0 && filtro.b.contains(cs[k - 1])) || (k < cs.length - 1 && filtro.b.contains(cs[k + 1]));
          if (dentro) { if (!cur) { cur = []; seg.push(cur); } cur.push(q); } else cur = null;
        });
      }
      [o.c, o.p].forEach(function (x) { if (!x) return; if (ver) x.setLatLngs(seg); if (ver && !g.hasLayer(x)) g.addLayer(x); else if (!ver && g.hasLayer(x)) g.removeLayer(x); });
    });
    ifaceObj.forEach(function (o) {
      if (o.i.existe) return;
      var ver = !filtro || (!filtro.solo && filtro.b.contains(o.i.p));
      if (ver && !GR.hubs.hasLayer(o.m)) GR.hubs.addLayer(o.m); else if (!ver && GR.hubs.hasLayer(o.m)) GR.hubs.removeLayer(o.m);
    });
    nomesParques();
  }
  function visibilidade() {
    aplicarFiltro();
    ['ciclo', 'faixa', 'bus', 'vias', 'hubs'].forEach(function (k) { ligar(GR[k], uiOn[k]); });
    CATS.forEach(function (c) { ligar(gPontos[c.id], c.id === 'obra' ? uiOn.obra : (uiOn.existe && catOn[c.id])); });
    ligar(gFixos, map.getZoom() >= 13);
    if (camadasZona.marginal) ligar(camadasZona.marginal, uiOn.marginal || atual === 'marginal');
    legRender(); notasRender();
  }
  CATS.forEach(function (c) { gPontos[c.id] = L.layerGroup(); });
  (DADOS.pontos || []).concat(DADOS.manuais || []).forEach(function (p) {
    var c = catPorId[p.cat]; if (!c) return;
    var ic = L.divIcon({ className: 'sq-ico', html: '<span class="' + (c.tracejado ? 'tr' : '') + '" style="background:' + c.cor + '">' + c.svg + '</span>', iconSize: [26, 26], iconAnchor: [13, 13] });
    var m = L.marker(p.p, { icon: ic, title: p.nome, alt: p.nome, riseOnHover: true, keyboard: false });
    m.bindTooltip(esc(p.nome), { direction: 'top', offset: [0, -12], permanent: false, className: 'sq-nome-ponto' });
    m.bindPopup('<b>' + esc(p.nome) + '</b><br>' + esc(c.nome) + (p.texto && p.cat !== 'obra' ? '<br>' + esc(p.texto) : '') + (p.cat === 'obra' ? ligNota('obra') : ''), { maxWidth: 240 });
    rotPontos.push({ m: m, cat: p.cat, nome: p.nome, p: p.p, texto: p.texto });
  });
  var MINZ = { obra: 0, saude: 14.5, bombeiros: 14.5, policia: 16, transporte: 14, escola: 14.5, parque: 14.5, servicos: 15, cultura: 15, igreja: 15.5, mercado: 15.5, desporto: 16 };
  var PRIO = ['obra', 'saude', 'bombeiros', 'policia', 'transporte', 'escola', 'parque', 'servicos', 'cultura', 'igreja', 'mercado', 'desporto'], DIST = 38;
  var filtro = null;   // com um cartão escolhido, só se mostra o que é dessa zona: {b: limites} ou {solo: nome da linha}
  function nofiltro(r) { return !filtro || (!filtro.solo && !filtro.semObra && filtro.b.contains(r.p)); }
  var forcado = null;   // marcador aberto pela pesquisa: não é escondido pelo desaglomerar
  map.on('popupclose', function () { forcado = null; });
  function nomesParques() {
    var z = map.getZoom(), ocupados = [];
    rotPontos.slice().sort(function (a, b) { return PRIO.indexOf(a.cat) - PRIO.indexOf(b.cat); }).forEach(function (r) {
      var g = gPontos[r.cat], ver = r.m === forcado || (z >= (MINZ[r.cat] != null ? MINZ[r.cat] : 13) && (r.cat !== 'obra' || nofiltro(r)));
      if (ver && r.cat === 'obra') ocupados.push(map.latLngToContainerPoint(r.m.getLatLng()));
      else if (ver && r.m !== forcado) { var q = map.latLngToContainerPoint(r.m.getLatLng()); ver = !ocupados.some(function (o) { return Math.abs(o.x - q.x) < DIST && Math.abs(o.y - q.y) < DIST; }); if (ver) ocupados.push(q); }
      if (ver && !g.hasLayer(r.m)) g.addLayer(r.m); else if (!ver && g.hasLayer(r.m)) g.removeLayer(r.m);
    });
  }
  map.on('zoomend', function () { nomesParques(); ligar(gFixos, map.getZoom() >= 13); }); nomesParques();


  var Leg = L.Control.extend({ options: { position: 'bottomleft' }, onAdd: function () {
    var d = L.DomUtil.create('div', 'sq-leg'), b = L.DomUtil.create('button', 'sq-leg-btn', d), p = L.DomUtil.create('div', 'sq-leg-corpo', d);
    b.type = 'button'; b.setAttribute('aria-expanded', 'true'); b.setAttribute('aria-controls', 'sq-leg-corpo'); b.textContent = 'Esconder legenda'; p.id = 'sq-leg-corpo';
    L.DomEvent.disableClickPropagation(d); L.DomEvent.disableScrollPropagation(d);
    L.DomEvent.on(b, 'click', function () { var a = b.getAttribute('aria-expanded') === 'true'; b.setAttribute('aria-expanded', a ? 'false' : 'true'); p.hidden = a; b.textContent = a ? 'Mostrar legenda' : 'Esconder legenda'; });
    legRender = function () {
      var cheio = el.classList.contains('sq-cheio'), act = UI.filter(function (u) { return cheio || uiOn[u.id]; });   // o menu de camadas só aparece em ecrã inteiro
      var h = '<p class="sq-leg-t">' + (cheio ? 'O que ver no mapa' : 'Legenda') + '</p><ul class="sq-leg-l">' + act.map(function (u) {
        var sw = '<i class="l" style="background:' + u.cor + '"></i>';
        return '<li>' + (cheio ? '<label><input type="checkbox" data-ui="' + u.id + '"' + (uiOn[u.id] ? ' checked' : '') + '>' + sw + esc(u.nome) + '</label>' : sw + esc(u.nome)) + '</li>';
      }).join('') + '</ul>';
      if (uiOn.existe) h += '<p class="sq-leg-t">Já existe</p><ul class="sq-leg-l">' + CATS.filter(function (c) { return c.id !== 'obra'; }).map(function (c) { return '<li><label><input type="checkbox" data-cat="' + c.id + '"' + (catOn[c.id] ? ' checked' : '') + '><span class="sq-ico-l" style="background:' + c.cor + '">' + c.svg + '</span>' + esc(c.nome) + '</label></li>'; }).join('') + '</ul>';
      p.innerHTML = h;
    };
    L.DomEvent.on(p, 'change', function (e) { var t = e.target; if (!t.getAttribute) return; filtro = null;   // ao mexer na legenda, as camadas aparecem no mapa todo, mesmo com um cartão aberto
      var u = t.getAttribute('data-ui'); if (u) { definir(u, t.checked); return; } var id = t.getAttribute('data-cat'); if (!id) return; catOn[id] = t.checked; visibilidade(); });
    if (el.clientWidth < 600) setTimeout(function () { b.click(); }, 0);
    return d;
  } });
  map.addControl(new Leg());
  function definir(id, on) {
    uiOn[id] = on; var cx = document.querySelector('#sq-camadas input[data-ui="' + id + '"]'); if (cx) cx.checked = on;
    visibilidade();
  }


  // Zonas: só aparece o contorno da localidade do cartão escolhido
  var CONTORNO = false;   // true volta a desenhar o contorno da localidade escolhida
  var gZona = L.featureGroup().addTo(map);
  DADOS.zonas.forEach(function (z) {
    var cor = z.cor || corCamada[z.camada], camada, estilo = { color: cor, weight: 3, opacity: 0.95, fillColor: cor, fillOpacity: 0.16, pane: 'pZonas', renderer: rZonas, interactive: false };
    if (z.camada === 'natureza') { estilo.weight = 1; estilo.opacity = 0.7; estilo.fillOpacity = 0.4; }   // áreas, não contornos
    if (z.geo && z.geo.linha) { camada = L.polyline(z.geo.linha, { color: cor, weight: 10, opacity: 0.85, lineCap: 'round', pane: 'pZonas', renderer: rZonas, interactive: z.id === 'marginal' }); if (z.id === 'marginal') camada.bindPopup('<b>' + esc(z.nome) + '</b><br>' + esc(z.frase) + ligNota('marginal'), { maxWidth: 260 }); }
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
    var colC = document.querySelector('.sq-col-cartao'), alca = document.createElement('button'), ultimaAlt = null;
    alca.type = 'button'; alca.className = 'sq-alca'; alca.setAttribute('aria-label', 'Ajustar a altura dos cartões: arrasta, ou toca para esconder e mostrar'); alca.innerHTML = '<span aria-hidden="true"></span>';
    if (colC) colC.insertBefore(alca, colC.firstChild);
    function altura(px) { corpo.style.setProperty('--cart', px == null ? '' : px + 'px'); }
    var arr = null;
    alca.addEventListener('pointerdown', function (e) { arr = { y: e.clientY, h: colC.getBoundingClientRect().height, mov: false }; alca.setPointerCapture(e.pointerId); });
    alca.addEventListener('pointermove', function (e) {
      if (!arr) return; var d = e.clientY - arr.y; if (Math.abs(d) > 5) arr.mov = true; if (!arr.mov) return;
      altura(Math.max(46, Math.min(window.innerHeight - 110, arr.h - d))); map.invalidateSize();
    });
    function fim() {
      if (!arr) return; var m = arr.mov; arr = null;
      if (!m) { var min = colC.getBoundingClientRect().height <= 60; if (min) altura(ultimaAlt); else { ultimaAlt = colC.getBoundingClientRect().height; altura(46); } }
      setTimeout(function () { map.invalidateSize(); }, 60);
    }
    alca.addEventListener('pointerup', fim); alca.addEventListener('pointercancel', fim);
    alca.addEventListener('keydown', function (e) { if (e.key === 'ArrowUp' || e.key === 'ArrowDown') { e.preventDefault(); altura(Math.max(46, Math.min(window.innerHeight - 110, colC.getBoundingClientRect().height + (e.key === 'ArrowUp' ? 60 : -60)))); map.invalidateSize(); } });
    function cheio(on) {
      if (!on) { altura(null); ultimaAlt = null; }
      el.classList.toggle('sq-cheio', on); corpo.classList.toggle('sq-cheio-corpo', on); document.documentElement.classList.toggle('sq-trava', on); posBusca();
      f.textContent = on ? 'Sair do ecrã inteiro' : 'Ecrã inteiro'; f.setAttribute('aria-pressed', on ? 'true' : 'false');
      if (on) { corpo.setAttribute('role', 'dialog'); corpo.setAttribute('aria-modal', 'true'); corpo.setAttribute('aria-label', 'Mapa e cartões em ecrã inteiro'); } else { corpo.removeAttribute('role'); corpo.removeAttribute('aria-modal'); corpo.removeAttribute('aria-label'); }
      // o resto da página fica inerte (leitores de ecrã e teclado ficam só no mapa)
      var no = corpo; while (no && no !== document.body) { var pai = no.parentElement; if (pai) [].forEach.call(pai.children, function (irmao) { if (irmao !== no) { if (on) irmao.setAttribute('inert', ''); else irmao.removeAttribute('inert'); } }); no = pai; }
      if (L.Browser.mobile) { if (on) map.dragging.enable(); else map.dragging.disable(); }
      legRender(); setTimeout(function () { map.invalidateSize(); if (atual) escolher(atual, true); else verTudo(); }, 60); f.focus();
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
    mini.innerHTML = '<button type="button" class="sq-mini-x" aria-label="Fechar e limpar a localidade do mapa">×</button><div class="sq-mini-ilu">' + ilu + '</div><div class="sq-mini-nav"><button type="button" data-d="-1" aria-label="Localidade anterior">‹</button><h3>' + esc(z.nome) + '</h3><button type="button" data-d="1" aria-label="Localidade seguinte">›</button></div><ul>' + z.medidas.slice(0, 3).map(function (m) { return '<li>' + esc(m.t) + '</li>'; }).join('') + '</ul>';
    mini.hidden = false; mini.setAttribute('data-fechado', 'n');
  }
  mini.addEventListener('click', function (e) {
    if (e.target.closest('.sq-mini-x')) { escolher(null, false); return; }
    var sb = e.target.closest('.sq-mini-nav button'); if (!sb) return;
    escolher(vizinho(+sb.getAttribute('data-d')), true);
    var n = mini.querySelector('.sq-mini-nav button[data-d="' + sb.getAttribute('data-d') + '"]'); if (n) n.focus();
  });
  // Cartões das localidades: setas dentro do cartão; o primeiro estado é "nada escolhido"
  var postal = document.getElementById('sq-postal');
  var ORDEM = ['vila', 'santana', 'sampaio', 'cotovia', 'zambujal', 'alfarim', 'meco', 'lagoa', 'qconde', 'mata', 'espichel', 'arrabida', 'varzea', 'en10', 'variante', 'almocreves', 'marginal'].filter(function (id) { return camadasZona[id]; });
  DADOS.zonas.forEach(function (z) { if (ORDEM.indexOf(z.id) < 0) ORDEM.push(z.id); });
  // Três grupos de cartões: localidades, estradas, espaços verdes
  var GRUPOS_C = [
    { id: 'loc', nome: 'Localidades', ids: ['vila', 'santana', 'sampaio', 'cotovia', 'zambujal', 'alfarim', 'meco', 'lagoa', 'qconde'] },
    { id: 'est', nome: 'Estradas', ids: ['marginal', 'variante', 'en10', 'acessocoina', 'almocreves'] },
    { id: 'ver', nome: 'Natureza', ids: ['arrabida', 'mata', 'espichel', 'varzea'] }
  ];
  GRUPOS_C.forEach(function (g) { g.ids = g.ids.filter(function (id) { return camadasZona[id]; }); });
  ORDEM.forEach(function (id) { if (!GRUPOS_C.some(function (g) { return g.ids.indexOf(id) >= 0; })) GRUPOS_C[0].ids.push(id); });
  var grupoAtual = GRUPOS_C[0], idx = -1;
  function grupoDe(id) { return GRUPOS_C.filter(function (g) { return g.ids.indexOf(id) >= 0; })[0] || GRUPOS_C[0]; }
  function vizinho(d) {   // cartão seguinte ou anterior, dentro do grupo
    var g = grupoAtual.ids, n = g.length; if (!n) return null;
    if (idx < 0) return d > 0 ? g[0] : g[n - 1];
    return g[(idx + d + n) % n];
  }
  var live = document.createElement('p'); live.className = 'sr'; live.setAttribute('aria-live', 'polite'); postal.parentNode.insertBefore(live, postal);
  function zonaDe(id) { return DADOS.zonas.filter(function (x) { return x.id === id; })[0]; }
  function barra(aberto) {
    var chev = function (d) { return '<svg viewBox="0 0 24 24" width="26" height="26" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="' + (d < 0 ? 'M15 5l-7 7 7 7' : 'M9 5l7 7-7 7') + '"/></svg>'; };
    var pontos = grupoAtual.ids.map(function (_, k) { return '<i class="' + (k === idx ? 'on' : '') + '"></i>'; }).join('');
    var tabs = '<div class="sq-grupos" role="group" aria-label="Tipo de cartão">' + GRUPOS_C.filter(function (g) { return g.ids.length; }).map(function (g) { return '<button type="button" data-g="' + g.id + '" aria-pressed="' + (g === grupoAtual ? 'true' : 'false') + '">' + g.nome + '</button>'; }).join('') + '</div>';
    var chips = false ? '<div class="sq-escolhas sq-chips" role="group" aria-label="' + grupoAtual.nome + '">' + grupoAtual.ids.map(function (k) { return '<button type="button" data-zona="' + k + '"' + (k === aberto ? ' aria-current="true"' : '') + '>' + esc(zonaDe(k).nome) + '</button>'; }).join('') + '</div>' : '';
    if (!aberto) return '';   // cartão inicial: só os três botões, sem setas
    return tabs + '<div class="sq-cnav"><button type="button" class="sq-seta" data-d="-1" aria-label="Cartão anterior">' + chev(-1) + '</button><span class="sq-dots" aria-hidden="true">' + pontos + '</span><button type="button" class="sq-seta" data-d="1" aria-label="Cartão seguinte">' + chev(1) + '</button></div>' + chips;
  }
  function cartao(id) {
    if (id) grupoAtual = grupoDe(id);
    idx = id ? grupoAtual.ids.indexOf(id) : -1; var z = id ? zonaDe(id) : null;
    if (!z) {
      live.textContent = 'Nenhum cartão escolhido';
      postal.innerHTML = '<div class="conteudo sq-intro"><h3 class="sr">Escolhe o que queres ver</h3><div class="sq-grupos sq-grupos-intro" role="group" aria-label="Tipo de cartão">' + GRUPOS_C.filter(function (g) { return g.ids.length; }).map(function (g) { return '<button type="button" data-g="' + g.id + '">' + g.nome + '</button>'; }).join('') + '</div></div>';
      return null;
    }
    live.textContent = z.nome + ', ' + (idx + 1) + ' de ' + grupoAtual.ids.length;
    var il = z.ilustracao, html = barra(id) + '<div class="ilustra">';
    if (il.tipo === 'perfil') {
      html += '<div class="sq-alternar" role="group" aria-label="Hoje ou proposta"><button type="button" data-v="hoje" aria-pressed="false">Hoje</button><button type="button" data-v="amanha" aria-pressed="true">Proposta</button></div><div class="desenho">' + ILU.perfil(il.amanha, 'Perfil de ' + z.nome + ' com a proposta') + '</div><p class="nota-ilu">' + esc(z.perfilNome ? 'Perfil da ' + z.perfilNome + ', ilustrativo.' : 'Perfil da rua, ilustrativo.') + '</p>';
    } else html += ILU.paisagem(il.variante, z.nome);
    html += '</div><div class="conteudo"><p class="camada">' + esc(z.etiqueta || nomeCamada[z.camada]) + '</p><h3>' + esc(z.nome) + '</h3><p class="frase">' + esc(z.frase) + '</p><ul class="sq-medidas">' +
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
  // Ao escolher uma localidade, ligam-se as camadas que têm algo dentro dela (autocarros, ciclovias, serviços…); a pessoa pode desligar
  function ligarDaZona(c, z) {
    function lig(id) { uiOn[id] = true; var cx = document.querySelector('#sq-camadas input[data-ui="' + id + '"]'); if (cx) cx.checked = true; }
    UI.forEach(function (u) { uiOn[u.id] = false; var cx = document.querySelector('#sq-camadas input[data-ui="' + u.id + '"]'); if (cx) cx.checked = false; });
    if (z.camada === 'natureza') { filtro = null; return; }   // áreas naturais: nada de camadas
    var solo = z.id === 'variante' ? [z.nome] : z.id === 'almocreves' ? ['Estrada dos Almocreves', 'Ciclovia da Estrada dos Almocreves'] : z.id === 'acessocoina' ? [z.nome] : null;   // mostram-se sozinhas
    if (solo) { filtro = { solo: solo }; lig('vias'); if (z.id === 'almocreves') lig('ciclo'); return; }
    var b = (c instanceof L.Circle ? c.getLatLng().toBounds(c.getRadius() * 2) : c.getBounds()).pad(0.1);
    filtro = { b: b, semObra: !!(z.geo && z.geo.linha) };   // nos cartões de estradas não aparecem os serviços propostos à volta
    linhasObj.forEach(function (o) {
      var uiId = o.l.camada === 'ativos' ? 'ciclo' : o.l.nome === 'Faixa BUS' ? 'faixa' : (o.l.camada === 'autocarro' || o.l.nome === 'Linha Azul') ? 'bus' : 'vias';
      if (o.l.coords.some(function (q) { return b.contains(q); })) lig(uiId);
    });
    ifaceObj.forEach(function (o) { if (!o.i.existe && b.contains(o.i.p)) lig('hubs'); });
    rotPontos.forEach(function (r) { if (r.cat === 'obra' && !filtro.semObra && b.contains(r.p)) lig('obra'); });
    if (camadasZona.marginal && camadasZona.marginal.getBounds && b.intersects(camadasZona.marginal.getBounds())) lig('marginal');
  }
  function escolher(id, voar) {
    var z = cartao(id);
    if (atual && camadasZona[atual] && gZona.hasLayer(camadasZona[atual])) gZona.removeLayer(camadasZona[atual]);
    atual = id || null;
    if (!z) { filtro = null; mini.hidden = true; if (voar) UI.forEach(function (u) { uiOn[u.id] = true; var cx = document.querySelector('#sq-camadas input[data-ui="' + u.id + '"]'); if (cx) cx.checked = true; }); visibilidade(); if (voar) verTudo(); return; }
    var c = camadasZona[id];
    if (CONTORNO || (DADOS.zonas.filter(function (q) { return q.id === id; })[0] || {}).geo) gZona.addLayer(c);   // sem contorno: só zoom e foco (a Marginal é uma linha e mantém-se)
    ligarDaZona(c, z);
    visibilidade(); miniAtualizar(z, z.ilustracao);
    if (voar) { if (RM) map.fitBounds(c.getBounds(), { padding: [90, 90], maxZoom: 15, animate: false }); else map.flyToBounds(c.getBounds(), { padding: [90, 90], maxZoom: 15, duration: 0.6 }); }
  }
  postal.addEventListener('click', function (e) {
    var sb = e.target.closest('.sq-seta'), eb = e.target.closest('.sq-escolhas button'), gb = e.target.closest('.sq-grupos button');
    if (gb && gb.getAttribute('aria-pressed') === 'true') { escolher(null, true); var ti = postal.querySelector('.sq-grupos button'); if (ti) ti.focus(); }
    else if (gb) { grupoAtual = GRUPOS_C.filter(function (g) { return g.id === gb.getAttribute('data-g'); })[0]; escolher(grupoAtual.ids[0], true); var t = postal.querySelector('.sq-grupos button[data-g="' + grupoAtual.id + '"]'); if (t) t.focus(); }
    else if (sb) { var d = +sb.getAttribute('data-d'); escolher(vizinho(d), true); var n = postal.querySelector('.sq-seta[data-d="' + d + '"]'); if (n) n.focus(); }
    else if (eb) { escolher(eb.getAttribute('data-zona'), true); var f = postal.querySelector('.sq-chips button[aria-current]') || postal.querySelector('.sq-seta[data-d="1"]'); if (f) f.focus(); }
  });

  // Menu de camadas (por cima do mapa)
  var fs = document.getElementById('sq-camadas') || document.createElement('fieldset');   // o menu de camadas vive na legenda do mapa
  UI.forEach(function (u) {
    var lab = document.createElement('label'); lab.className = 'sq-chip';
    var inp = document.createElement('input'); inp.type = 'checkbox'; inp.checked = false; inp.setAttribute('data-ui', u.id);
    inp.addEventListener('change', function () { definir(u.id, inp.checked); });
    var cor = document.createElement('span'); cor.className = 'cor'; cor.style.background = u.cor;
    lab.appendChild(inp); lab.appendChild(cor); lab.appendChild(document.createTextNode(u.nome)); fs.appendChild(lab);
  });
  [['Marcar tudo', true], ['Limpar', false]].forEach(function (x) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'sq-todos'; b.textContent = x[0];
    b.addEventListener('click', function () {
      if (atual) escolher(null, false);   // sem cartão: mostra-se o mapa todo, sem filtro de zona
      UI.forEach(function (u) { uiOn[u.id] = x[1]; var cx = fs.querySelector('input[data-ui="' + u.id + '"]'); if (cx) cx.checked = x[1]; }); visibilidade(); verTudo();
      el.scrollIntoView({ behavior: RM ? 'auto' : 'smooth', block: 'start' });   // o menu fica por baixo do mapa: leva-se a pessoa ao resultado
      live.textContent = x[1] ? 'Todas as camadas ligadas.' : 'Todas as camadas desligadas.';
    });
    fs.appendChild(b);
  });
  var notas = document.getElementById('sq-notas');
  notasRender = function () {
    if (!notas) return; var act = UI.filter(function (u) { return uiOn[u.id]; });
    notas.innerHTML = act.map(function (u) { return '<p data-ui="' + u.id + '" style="border-left-color:' + u.cor + '"><b>' + esc(u.nome) + '.</b> ' + esc(u.nota) + '</p>'; }).join('');
  };


  // ===== Pesquisa =====
  (function () {
    var inp = document.getElementById('sq-q'), lista = document.getElementById('sq-res'), nlive = document.getElementById('sq-res-n'); if (!inp || !lista) return;
    function norm(t) { return String(t || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase(); }
    var IDX = [];
    function add(grupo, tipo, titulo, extra, acao) { IDX.push({ g: grupo, tipo: tipo, t: titulo, n: norm(titulo), x: norm(extra || ''), a: acao }); }
    DADOS.zonas.forEach(function (z) {
      var tipo = z.etiqueta || nomeCamada[z.camada] || 'Zona';
      add(0, tipo, z.nome, z.frase, function () { escolher(z.id, true); });
      (z.medidas || []).forEach(function (m) { add(5, 'Medida em ' + z.nome, m.t, '', function () { escolher(z.id, true); }); });
    });
    rotPontos.forEach(function (r) {
      var c = catPorId[r.cat];
      add(r.cat === 'obra' ? 2 : 3, r.cat === 'obra' ? 'Proposta de serviço' : (c ? c.nome : 'Local'), r.nome, r.texto, function () {
        if (r.cat === 'obra') definir('obra', true);
        forcado = r.m; var g = gPontos[r.cat]; if (!g.hasLayer(r.m)) g.addLayer(r.m);
        var abrir = function () { r.m.openPopup(); };
        if (RM) { map.setView(r.p, 16, { animate: false }); abrir(); } else { map.once('moveend', abrir); map.flyTo(r.p, 16, { duration: 0.6 }); }
      });
    });
    linhasObj.forEach(function (o) {
      var uiId = o.l.camada === 'ativos' ? 'ciclo' : o.l.nome === 'Faixa BUS' ? 'faixa' : (o.l.camada === 'autocarro' || o.l.nome === 'Linha Azul') ? 'bus' : 'vias';
      var tipo = { ciclo: 'Rede ciclável', faixa: 'Faixa BUS', bus: 'Autocarro', vias: 'Novo acesso' }[uiId];
      add(4, tipo, o.l.nome, o.l.texto, function () {
        definir(uiId, true); var b = o.p.getBounds();
        if (RM) map.fitBounds(b, { padding: [60, 60], animate: false }); else map.flyToBounds(b, { padding: [60, 60], duration: 0.6 });
        o.p.openPopup(b.getCenter());
      });
    });
    ifaceObj.forEach(function (o) {
      add(4, o.i.existe ? 'Estação (já existe)' : 'Novo hub', o.i.nome, o.i.texto, function () {
        if (!o.i.existe) definir('hubs', true);
        var ver = function () { o.m.openPopup(); };
        if (RM) { map.setView(o.i.p, 15, { animate: false }); ver(); } else { map.once('moveend', ver); map.flyTo(o.i.p, 15, { duration: 0.6 }); }
      });
    });
    (DADOS.localidades || []).forEach(function (l) {
      if (IDX.some(function (x) { return x.g === 0 && x.n === norm(l.nome); })) return;
      add(1, 'Localidade sem cartão próprio', l.nome, '', function () {
        var p = L.popup({ maxWidth: 220 }).setLatLng(l.p).setContent('<b>' + esc(l.nome) + '</b><br>Sem cartão próprio neste mapa.');
        var abrir = function () { p.openOn(map); };
        if (RM) { map.setView(l.p, 15, { animate: false }); abrir(); } else { map.once('moveend', abrir); map.flyTo(l.p, 15, { duration: 0.6 }); }
      });
    });
    var GRUPOS = ['Localidades e estradas', 'Outras localidades', 'Propostas de serviços', 'Locais que já existem', 'Linhas e estações', 'Medidas'];
    var res = [], ativo = -1;
    function fechar() { lista.hidden = true; inp.setAttribute('aria-expanded', 'false'); inp.removeAttribute('aria-activedescendant'); ativo = -1; }
    function marcar(i) {
      ativo = i; [].forEach.call(lista.querySelectorAll('[role=option]'), function (o, k) { o.setAttribute('aria-selected', k === i ? 'true' : 'false'); o.classList.toggle('on', k === i); });
      if (i >= 0) { var o = lista.querySelectorAll('[role=option]')[i]; inp.setAttribute('aria-activedescendant', o.id); o.scrollIntoView({ block: 'nearest' }); } else inp.removeAttribute('aria-activedescendant');
    }
    function escolhe(i) { var r = res[i]; if (!r) return; fechar(); inp.value = ''; filtro = null; r.a(); nlive.textContent = r.t + ': aberto no mapa.'; }
    function procurar() {
      var q = norm(inp.value).trim(); if (q.length < 2) { res = []; fechar(); nlive.textContent = ''; return; }
      var tk = q.split(/\s+/);
      res = IDX.map(function (it) {
        var h = it.n + ' ' + it.x; if (!tk.every(function (t) { return h.indexOf(t) >= 0; })) return null;
        var sc = it.n.indexOf(q) === 0 ? 0 : it.n.indexOf(q) > 0 ? 1 : tk.every(function (t) { return it.n.indexOf(t) >= 0; }) ? 2 : 3;
        return { it: it, sc: sc };
      }).filter(Boolean).sort(function (a, b) { return (a.sc > 2) - (b.sc > 2) || a.it.g - b.it.g || a.sc - b.sc || a.it.n.length - b.it.n.length; }).slice(0, 10).map(function (r) { return r.it; });
      var h = '', ult = -1;
      res.forEach(function (r, i) {
        if (r.g !== ult) { h += '<li role="presentation" class="grp">' + GRUPOS[r.g] + '</li>'; ult = r.g; }
        h += '<li role="option" id="sq-res-' + i + '" aria-selected="false" data-i="' + i + '"><span class="t">' + esc(r.t.length > 90 ? r.t.slice(0, 88) + '…' : r.t) + '</span><span class="k">' + esc(r.tipo) + '</span></li>';
      });
      lista.innerHTML = h || '<li role="presentation" class="vazio">Nada encontrado. Experimenta outra palavra.</li>';
      lista.hidden = false; inp.setAttribute('aria-expanded', 'true'); ativo = -1;
      nlive.textContent = res.length ? res.length + (res.length === 1 ? ' resultado.' : ' resultados.') + ' Usa as setas para escolher.' : 'Nada encontrado.';
    }
    inp.addEventListener('input', procurar);
    inp.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowDown') { if (!res.length) return; e.preventDefault(); if (lista.hidden) { lista.hidden = false; inp.setAttribute('aria-expanded', 'true'); } marcar(Math.min(res.length - 1, ativo + 1)); }
      else if (e.key === 'ArrowUp') { if (!res.length) return; e.preventDefault(); marcar(Math.max(0, ativo - 1)); }
      else if (e.key === 'Enter') { if (ativo >= 0) { e.preventDefault(); escolhe(ativo); } else if (res.length) { e.preventDefault(); escolhe(0); } }
      else if (e.key === 'Escape') { if (!lista.hidden) { e.stopPropagation(); fechar(); } else if (inp.value) inp.value = ''; }
    });
    lista.addEventListener('mousedown', function (e) { e.preventDefault(); });
    lista.addEventListener('click', function (e) { var o = e.target.closest('[role=option]'); if (o) escolhe(+o.getAttribute('data-i')); });
    inp.addEventListener('blur', function () { setTimeout(fechar, 120); });
  })();


  // A pesquisa fica no topo da coluna dos cartões no computador e por cima do menu no telemóvel
  (function () {
    var bx = document.querySelector('.sq-busca'), col = document.querySelector('.sq-col-cartao'); if (!bx || !col || !window.matchMedia) return;
    var mq = window.matchMedia('(min-width: 980px)');
    var cp = col.parentNode;
    function pos() { if (mq.matches || (corpo && corpo.classList.contains('sq-cheio-corpo'))) { if (bx.parentNode !== col) col.insertBefore(bx, col.querySelector('.sq-alca') ? col.querySelector('.sq-alca').nextSibling : col.firstChild); } else if (bx.nextElementSibling !== cp) cp.parentNode.insertBefore(bx, cp); }
    posBusca = pos; pos(); if (mq.addEventListener) mq.addEventListener('change', pos); else mq.addListener(pos);
  })();
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
  cartao(null); visibilidade();
})();
