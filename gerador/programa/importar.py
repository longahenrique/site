#!/usr/bin/env python3
"""Junta ao mapa os dados do OpenStreetMap (ficheiros descarregados com descarregar-dados-mapa.html).
Uso (na raiz do repositório):  python3 gerador/programa/importar.py
Usa, se existirem na pasta gerador/programa/:  equipamentos.json  (ícones e nomes)  e  limites.json  (contornos).
Grava o resultado em mapa.json. Não precisa de rede."""
import json, os, math, re
PAS = 'gerador/programa/'; MAPA = PAS + 'mapa.json'
D = json.load(open(MAPA, encoding='utf-8'))
def pos(e):
    if 'lat' in e: return [round(e['lat'], 5), round(e['lon'], 5)]
    c = e.get('center'); return [round(c['lat'], 5), round(c['lon'], 5)] if c else None
def cat(t):
    a, l, s, r, h = t.get('amenity'), t.get('leisure'), t.get('shop'), t.get('railway'), t.get('highway')
    if l in ('park', 'garden'): return 'parque'
    if a in ('school', 'college', 'university'): return 'escola'
    if a in ('clinic', 'doctors', 'hospital'): return 'saude'
    if a == 'fire_station': return 'bombeiros'
    if a == 'police': return 'policia'
    if a == 'place_of_worship' and t.get('religion', 'christian') == 'christian': return 'igreja'
    if a in ('library', 'arts_centre', 'theatre', 'cinema', 'community_centre'): return 'cultura'
    if a in ('townhall', 'post_office', 'social_facility'): return 'servicos'
    if a == 'marketplace' or s == 'supermarket': return 'mercado'
    if l in ('sports_centre', 'pitch', 'swimming_pool') or a == 'sports_hall': return 'desporto'
    if r in ('station', 'halt') or a in ('bus_station', 'ferry_terminal'): return 'transporte'
    return None
def anel(membros):
    segs = [[(g['lat'], g['lon']) for g in m['geometry']] for m in membros if m.get('geometry')]
    aneis = []
    while segs:
        a = segs.pop(0)
        mudou = True
        while mudou and a[0] != a[-1]:
            mudou = False
            for i, s in enumerate(segs):
                if s[0] == a[-1]: a += s[1:]; segs.pop(i); mudou = True; break
                if s[-1] == a[-1]: a += s[::-1][1:]; segs.pop(i); mudou = True; break
                if s[-1] == a[0]: a = s[:-1] + a; segs.pop(i); mudou = True; break
                if s[0] == a[0]: a = s[::-1][:-1] + a; segs.pop(i); mudou = True; break
        aneis.append([[round(x, 5), round(y, 5)] for x, y in a])
    return aneis
def dentro(p, aneis):
    x, y, c = p[1], p[0], False
    for a in aneis:
        for i in range(len(a)):
            (y1, x1), (y2, x2) = a[i-1], a[i]
            if (y1 > y) != (y2 > y) and x < (x2-x1)*(y-y1)/(y2-y1)+x1: c = not c
    return c
CONC = None
if os.path.exists(PAS + 'limites.json'):
    for e in json.load(open(PAS + 'limites.json', encoding='utf-8'))['elements']:
        if e['type'] == 'relation' and e.get('tags', {}).get('name') == 'Sesimbra' and e['tags'].get('admin_level') == '7':
            CONC = anel([m for m in e['members'] if m.get('role', 'outer') == 'outer'])
f = PAS + 'equipamentos.json'
if os.path.exists(f):
    els = json.load(open(f, encoding='utf-8'))['elements']; pts, vistos = [], set()
    for e in els:
        t = e.get('tags', {}); c = cat(t); n = t.get('name'); p = pos(e)
        if not c or not n or not p: continue
        if CONC and not dentro(p, CONC): continue   # só dentro do concelho de Sesimbra
        if c == 'desporto' and t.get('leisure') == 'pitch' and len(n) < 4: continue
        if c == 'saude' and not re.search(r'USF|UCSP|URAP|Centro de Saúde|Unidade|Hospital|SAP|Extensão|Posto', n): continue
        if c == 'escola' and not re.search(r'Escola|Agrupamento|Colégio|Universidade', n): continue
        if c == 'servicos' and not re.search(r'Câmara|Junta|Loja do Cidadão|Balcão|CTT|Finanças|Segurança Social|Tribunal|Espaço Cidadão|Tesouraria', n): continue
        if c == 'cultura' and not re.search(r'Biblioteca|Cine|Teatro|Auditório|Museu|Centro Cultural|Casa da|Galeria', n): continue
        if c == 'desporto' and not re.search(r'Pavilhão|Piscina|Estádio|Complexo|Campo|Polidesportivo', n): continue
        if c == 'mercado' and not re.search(r'Mercado|Pingo Doce|Continente|Lidl|Intermarché|Aldi|Minipreço|Mini Preço|Auchan|Meu Super|Recheio', n): continue
        if c == 'igreja' and not re.search(r'^(Igreja|Capela|Ermida|Santuário|Convento|Matriz)', n): continue
        if any(q['cat'] == c and q['nome'].lower() == n.lower() and math.hypot((q['p'][0]-p[0])*111320, (q['p'][1]-p[1])*87000) < 300 for q in pts): continue   # mesmo nome e tipo a menos de 300 m
        pts.append({'cat': c, 'nome': n, 'p': p})
    # nomes de sítios para posicionar: Moagem de Sampaio, Ribeira do Marchante, Várzea
    for e in els:
        t = e.get('tags', {}); n = t.get('name', '')
        if any(x in n for x in ('Moagem', 'Marchante', 'Várzea', 'Varzea')) and pos(e): print('Sítio encontrado:', n, pos(e))
    # saúde: várias unidades no mesmo edifício/sítio ficam num só ícone
    def prio(n): return 0 if 'UCSP' in n else 1 if 'USF' in n else 2
    saude = sorted([p for p in pts if p['cat'] == 'saude'], key=lambda p: prio(p['nome']))
    grupos = []
    for p in saude:
        for g in grupos:
            if math.hypot((g[0]['p'][0]-p['p'][0])*111320, (g[0]['p'][1]-p['p'][1])*87000) < 250: g.append(p); break
        else: grupos.append([p])
    pts = [p for p in pts if p['cat'] != 'saude']
    for g in grupos:
        p = dict(g[0])
        if len(g) > 1: p['texto'] = 'No mesmo local: ' + '; '.join(x['nome'] for x in g[1:])
        pts.append(p)
    # nomes de aldeias e bairros (só texto, sem forma)
    zn = {'sesimbra', 'castelo', 'santana', 'zambujal', 'zambujal de cima', 'zambujal de baixo', 'quinta do conde', 'alfarim', 'cotovia', 'sampaio', 'aldeia do meco', 'azóia', 'lagoa de albufeira', 'vila e porto'}
    loc, vistos2 = [], set()
    for e in els:
        t = e.get('tags', {}); n = t.get('name'); p = pos(e)
        if t.get('place') not in ('hamlet', 'village', 'neighbourhood') or not n or not p or n.lower() in zn or n.lower() in vistos2 or n.startswith('Urbanização'): continue
        if CONC and not dentro(p, CONC): continue
        vistos2.add(n.lower()); loc.append({'nome': n, 'p': p})
    D['localidades'] = loc; print(len(loc), 'nomes de localidades')
    D['pontos'] = pts; print(len(pts), 'locais com ícone')
# contornos
def simplifica(a, tol=0.00004):
    if len(a) < 4: return a
    out = [a[0]]
    for p in a[1:-1]:
        if math.hypot(p[0]-out[-1][0], p[1]-out[-1][1]) > tol: out.append(p)
    out.append(a[-1]); return out
# zona -> nomes no OpenStreetMap (ajustar se for preciso)
NOMES = {'qconde': ['Quinta do Conde'], 'arrabida': ['Parque Natural da Arrábida', 'Serra da Arrábida'], 'espichel': ['ZPE Cabo Espichel', 'Cabo Espichel']}
f = PAS + 'limites.json'
if os.path.exists(f):
    els = json.load(open(f, encoding='utf-8'))['elements']
    for z in D['zonas']:
        nomes = NOMES.get(z['id']);
        if not nomes: continue
        achados = [e for e in els if e.get('tags', {}).get('name') in nomes]
        # preferir fronteiras administrativas de freguesia / áreas protegidas
        achados.sort(key=lambda e: (e['type'] != 'relation', e.get('tags', {}).get('admin_level', '9'), -len(e.get('geometry', []))))
        aneis = []
        for e in achados[:1]:
            if e['type'] == 'relation': aneis = anel([m for m in e['members'] if m.get('role', 'outer') == 'outer'])
            elif 'geometry' in e: aneis = [[[round(g['lat'], 5), round(g['lon'], 5)] for g in e['geometry']]]
        aneis = [simplifica(a) for a in aneis if len(a) > 3]
        if aneis:
            z['limite'] = aneis; z.pop('poligono', None); z.pop('centro', None); z.pop('raio', None)
            print('Contorno de', z['nome'], '->', len(aneis), 'anel(éis),', sum(len(a) for a in aneis), 'pontos')
        else: print('Sem contorno para', z['nome'], '(mantém o desenho atual)')
# Zambujal (zonas urbanas junto aos núcleos) e Mata (matas dentro da zona) a partir de areas.json
def aneis_de(e):
    if e['type'] == 'way': return [[[round(g['lat'], 5), round(g['lon'], 5)] for g in e['geometry']]]
    return anel([m for m in e['members'] if m.get('role', 'outer') == 'outer'])
def centro(a): return [sum(p[0] for p in a)/len(a), sum(p[1] for p in a)/len(a)]
def uso(e): t = e.get('tags', {}); return t.get('landuse') or t.get('natural')
def so_terra(aneis, costa):
    """Recorta os anéis (lat, lon) à parte em terra, usando a linha de costa do OpenStreetMap (terra à esquerda do sentido da linha)."""
    import numpy as np, cv2
    pts = [p for a in aneis for p in a]
    la0, la1 = min(p[0] for p in pts)-0.003, max(p[0] for p in pts)+0.003; lo0, lo1 = min(p[1] for p in pts)-0.003, max(p[1] for p in pts)+0.003
    px = 12.0; ky = 111320.0; kx = ky*math.cos(math.radians((la0+la1)/2))
    W, H = int((lo1-lo0)*kx/px)+3, int((la1-la0)*ky/px)+3
    def xy(la, lo): return ((lo-lo0)*kx/px+1, (la1-la)*ky/px+1)
    # lado da costa pelo segmento mais próximo (terra à esquerda do sentido): não depende de a linha estar fechada
    from scipy.spatial import cKDTree
    P, Dv = [], []
    for w in costa:
        g = [((x['lon']-lo0)*kx, (x['lat']-la1)*ky) for x in w['geometry']]
        for (x1, y1), (x2, y2) in zip(g, g[1:]):
            L = math.hypot(x2-x1, y2-y1) or 1e-9; n = max(1, int(L/8))
            for k in range(n): P.append((x1+(x2-x1)*k/n, y1+(y2-y1)*k/n)); Dv.append(((x2-x1)/L, (y2-y1)/L))
    P = np.array(P); Dv = np.array(Dv); arv = cKDTree(P)
    ys, xs = np.mgrid[0:H, 0:W]; gx = (xs-1)*px; gy = -(ys-1)*px
    _, ix = arv.query(np.c_[gx.ravel(), gy.ravel()])
    vx = gx.ravel()-P[ix, 0]; vy = gy.ravel()-P[ix, 1]
    terra_lado = (Dv[ix, 0]*vy - Dv[ix, 1]*vx > 0).reshape(H, W)
    mar = ~terra_lado
    zona = np.zeros((H, W), np.uint8)
    for a in aneis: cv2.fillPoly(zona, [np.array([xy(p[0], p[1]) for p in a], np.int32)], 255)
    terra = ((zona > 0) & ~mar).astype(np.uint8)*255
    terra = cv2.medianBlur(terra, 9)   # tira as cunhas finas que aparecem onde a linha de costa tem falhas
    terra = cv2.morphologyEx(terra, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    cs, _ = cv2.findContours(terra, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); out = []
    for c in cs:
        if cv2.contourArea(c) < 60: continue
        c = cv2.approxPolyDP(c, 1.0, True)[:, 0, :]
        out.append([[round(la1-(y-1)*px/ky, 5), round(lo0+(x-1)*px/kx, 5)] for x, y in c])
    return out
# Centros das localidades: cada edifício, rua ou zona residencial fica na localidade com o centro mais perto (células de Voronoi),
# em vez de caixas retangulares, que davam contornos quadrados. O segundo número é o fecho morfológico, em metros.
CENTROS = {'vila': (38.4445, -9.1005), 'santana': (38.4595, -9.1030), 'sampaio': (38.4700, -9.0930), 'cotovia': (38.4720, -9.1016),
           'zambujal': (38.4550, -9.1260), 'lagoa': (38.5030, -9.1650), 'meco': (38.4720, -9.1700), 'azoia': (38.4320, -9.1870), 'alfarim': (38.4768, -9.1605)}
FECHO = {'vila': 60, 'santana': 55, 'sampaio': 55, 'cotovia': 45, 'zambujal': 45, 'lagoa': 40, 'meco': 45, 'azoia': 50}
URB = {k: ((c[0]-0.016, c[0]+0.016, c[1]-0.022, c[1]+0.022), FECHO[k]) for k, c in CENTROS.items() if k in FECHO}
def contorno_urbano(A, caixa, fecho_m, ruas=None, raio_rua=14, edif=None, raio_edif=22, ctr=None, eu=None):
    """Junta as zonas residenciais da caixa (lat0, lat1, lon0, lon1) num contorno único (fecho morfológico)."""
    import numpy as np, cv2
    la0, la1, lo0, lo1 = caixa; px = 4.0                      # metros por pixel
    ky, kx = 111320.0, 111320.0*math.cos(math.radians((la0+la1)/2))
    W, H = int((lo1-lo0)*kx/px)+1, int((la1-la0)*ky/px)+1
    img = np.zeros((H, W), np.uint8); n = 0
    for e in A:
        if uso(e) not in ('residential', 'retail'): continue
        for a in aneis_de(e):
            if len(a) < 4: continue
            c = centro(a)
            if not (la0 <= c[0] <= la1 and lo0 <= c[1] <= lo1): continue
            pts = np.array([[(p[1]-lo0)*kx/px, (la1-p[0])*ky/px] for p in a], np.int32)
            cv2.fillPoly(img, [pts], 255); n += 1
    # ruas residenciais (com casas mas sem 'landuse=residential' no OSM): entram como faixas largas
    if ruas:
        for w in ruas:
            g = w['geometry']
            if not any(la0 <= q['lat'] <= la1 and lo0 <= q['lon'] <= lo1 for q in g): continue
            pts = np.array([[(q['lon']-lo0)*kx/px, (la1-q['lat'])*ky/px] for q in g], np.int32)
            cv2.polylines(img, [pts], False, 255, max(1, int(raio_rua*2/px))); n += 1
    # edifícios (centro de cada um, descarregados no botão 8): cada casa conta, mesmo sem 'landuse' nem rua marcada
    if edif:
        for la, lo in edif:
            if la0 <= la <= la1 and lo0 <= lo <= lo1:
                cv2.circle(img, (int((lo-lo0)*kx/px), int((la1-la)*ky/px)), int(raio_edif/px), 255, -1); n += 1
    if not n: return []
    if eu:   # só a célula desta localidade
        la_g = la1-(np.arange(H)+0.5)*px/ky; lo_g = lo0+(np.arange(W)+0.5)*px/kx
        d_eu = None; melhor = None
        for k, (a, b) in CENTROS.items():
            dd = ((la_g[:, None]-a)*ky)**2+((lo_g[None, :]-b)*kx)**2
            melhor = dd if melhor is None else np.minimum(melhor, dd)
            if k == eu: d_eu = dd
        celula = (d_eu <= melhor).astype(np.uint8)*255
        img = cv2.bitwise_and(img, celula)
    # fecho morfológico; se ficar em várias manchas, vai alargando até a localidade ser uma zona contínua (máx. 3x)
    base = img.copy(); f = fecho_m
    while True:
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(f/px)*2+1,)*2)
        img = cv2.morphologyEx(base, cv2.MORPH_CLOSE, k)
        if eu: img = cv2.bitwise_and(img, celula)
        cs, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        grandes = [c for c in cs if cv2.contourArea(c) >= (150/px)**2]
        if len(grandes) <= 1 or f >= fecho_m*3: break
        f += 15
    if len(grandes) > 1:                                        # ainda separadas: fica só a maior
        if ctr:
            cx, cy = (ctr[1]-lo0)*kx/px, (la1-ctr[0])*ky/px
            grandes = [max(grandes, key=lambda c: cv2.pointPolygonTest(c, (cx, cy), True))]   # a mancha que contém (ou está mais perto de) o centro da localidade
        else: grandes = [max(grandes, key=cv2.contourArea)]
    out = []
    for c in grandes:
        c = cv2.approxPolyDP(c, 1.2, True)[:, 0, :]
        out.append([[round(la1-y*px/ky, 5), round(lo0+x*px/kx, 5)] for x, y in c])
    return out
RUAS_RES = []
if os.path.exists(PAS + 'ruas.json'):
    RUAS_RES = [e for e in json.load(open(PAS + 'ruas.json', encoding='utf-8'))['elements'] if e.get('type') == 'way' and e.get('geometry') and e.get('tags', {}).get('highway') in ('residential', 'living_street', 'pedestrian')]
EDIF = []
if os.path.exists(PAS + 'edificios.json'):
    for e in json.load(open(PAS + 'edificios.json', encoding='utf-8'))['elements']:
        c = e.get('center') or ({'lat': e['lat'], 'lon': e['lon']} if 'lat' in e else None)
        if c: EDIF.append((c['lat'], c['lon']))
    print(len(EDIF), 'edifícios lidos')
f = PAS + 'areas.json'
if os.path.exists(f):
    A = [e for e in json.load(open(f, encoding='utf-8'))['elements'] if e.get('geometry') or e.get('members')]
    for z in D['zonas']:
        if z['id'] in URB and not z.get('manual'):
            caixa, fecho = URB[z['id']]
            ring = contorno_urbano(A, caixa, fecho, RUAS_RES, edif=EDIF, ctr=CENTROS.get(z['id']), eu=z['id'])
            if ring: z['limite'] = ring; z.pop('centro', None); z.pop('raio', None); print('Contorno de', z['nome'], '->', len(ring), 'forma(s)', sum(len(r) for r in ring), 'pontos')
            else: print('Sem zona urbana para', z['nome'])
        if z['id'] == 'mata':
            sel = []; poly = z.get('poligono')
            if not poly: continue
            for e in A:
                if uso(e) not in ('forest', 'wood'): continue
                for a in aneis_de(e):
                    if len(a) > 3 and dentro(centro(a), [poly]): sel.append(simplifica(a))
            if sel: z['limite'] = sel; z.pop('poligono', None); print('Contorno da Mata ->', len(sel), 'mancha(s) de mata')
            else: print('Sem matas encontradas dentro da zona')
# Mata de Sesimbra: todas as matas e bosques do concelho a sul da Quinta do Conde (mata.json, botão 7 do descarregador)
f = PAS + 'mata.json'
if os.path.exists(f):
    MT = [e for e in json.load(open(f, encoding='utf-8'))['elements'] if e.get('geometry') or e.get('members')]
    sel = []
    for e in MT:
        if uso(e) not in ('forest', 'wood'): continue
        for a in aneis_de(e):
            if len(a) < 4: continue
            c = centro(a)
            if c[0] > 38.53 or (CONC and not dentro(c, CONC)): continue
            la = [p[0] for p in a]; lo = [p[1] for p in a]
            if (max(la)-min(la))*111320 * (max(lo)-min(lo))*88000 < 15000: continue   # < 1,5 ha
            sel.append(simplifica(a))
    for z in D['zonas']:
        if z['id'] == 'mata' and sel:
            z['limite'] = sel; z.pop('poligono', None); print('Mata de Sesimbra ->', len(sel), 'manchas de mata (mata.json)')
# Alfarim: sem zona residencial no OpenStreetMap, o contorno sai da malha de ruas da povoação (ruas.json)
f = PAS + 'ruas.json'
if os.path.exists(f):
    import numpy as np, cv2
    R = [e for e in json.load(open(f, encoding='utf-8'))['elements'] if e.get('geometry') and e.get('tags', {}).get('highway') in ('residential', 'unclassified', 'living_street', 'tertiary', 'pedestrian')]
    for z in D['zonas']:
        if z['id'] != 'alfarim' or z.get('manual'): continue
        c0 = z.get('centro') or [38.4785, -9.1605]; z['_c'] = c0
        la0, la1, lo0, lo1 = c0[0]-0.0075, c0[0]+0.0075, c0[1]-0.010, c0[1]+0.010; px = 3.0
        ky, kx = 111320.0, 111320.0*math.cos(math.radians(c0[0]))
        W, H = int((lo1-lo0)*kx/px)+1, int((la1-la0)*ky/px)+1; img = np.zeros((H, W), np.uint8)
        for e in R:
            g = [(p['lat'], p['lon']) for p in e['geometry']]
            if not any(la0 <= p[0] <= la1 and lo0 <= p[1] <= lo1 for p in g): continue
            cv2.polylines(img, [np.array([[(p[1]-lo0)*kx/px, (la1-p[0])*ky/px] for p in g], np.int32)], False, 255, 1)
        k = lambda m: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(m/px)*2+1,)*2)
        img = cv2.dilate(img, k(30)); img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, k(50)); img = cv2.morphologyEx(img, cv2.MORPH_OPEN, k(70))
        n, lab, st, cen = cv2.connectedComponentsWithStats(img)
        # fica só a mancha que contém (ou está mais perto de) o centro da povoação
        cx, cy = int((c0[1]-lo0)*kx/px), int((la1-c0[0])*ky/px); alvo = lab[min(max(cy, 0), H-1), min(max(cx, 0), W-1)]
        if alvo == 0 and n > 1: alvo = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA]))
        if alvo:
            m1 = (lab == alvo).astype(np.uint8)*255
            cs, _ = cv2.findContours(m1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); c = max(cs, key=cv2.contourArea)
            c = cv2.approxPolyDP(c, 1.5, True)[:, 0, :]
            z['limite'] = [[[round(la1-y*px/ky, 5), round(lo0+x*px/kx, 5)] for x, y in c]]; print('Contorno de Alfarim (ruas) ->', len(c), 'pontos, área ≈', int(cv2.countNonZero(m1)*px*px/10000), 'ha')
        z.pop('_c', None)
# Parque da Várzea: contorno real (precisa de varzea.json, botão 6 do descarregador)
f = PAS + 'varzea.json'
if os.path.exists(f):
    VZ = [e for e in json.load(open(f, encoding='utf-8'))['elements'] if e.get('geometry') or e.get('members')]
    sel = [e for e in VZ if re.search(r'Parque Ecol', e.get('tags', {}).get('name', ''))] or []
    if sel:
        import numpy as np, cv2
        todos = [a for e in sel for a in aneis_de(e) if len(a) > 3]
        la = [p[0] for a in todos for p in a]; lo = [p[1] for a in todos for p in a]
        la0, la1, lo0, lo1 = min(la)-0.002, max(la)+0.002, min(lo)-0.002, max(lo)+0.002; px = 2.0
        ky, kx = 111320.0, 111320.0*math.cos(math.radians((la0+la1)/2))
        W, H = int((lo1-lo0)*kx/px)+1, int((la1-la0)*ky/px)+1; img = np.zeros((H, W), np.uint8)
        for a in todos: cv2.fillPoly(img, [np.array([[(p[1]-lo0)*kx/px, (la1-p[0])*ky/px] for p in a], np.int32)], 255)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(25/px)*2+1,)*2))
        cs, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        ring = [[[round(la1-y*px/ky, 5), round(lo0+x*px/kx, 5)] for x, y in cv2.approxPolyDP(c, 1.0, True)[:, 0, :]] for c in cs if cv2.contourArea(c) > (30/px)**2]
        for z in D['zonas']:
            if z['id'] == 'varzea' and ring and not z.get('retangulo') and not z.get('manual'):   # se o contorno foi marcado à mão (retângulo), não o substitui
                z['limite'] = ring; z.pop('centro', None); z.pop('raio', None); z['rotulo'] = centro(max(ring, key=len)); print('Contorno do Parque da Várzea ->', len(ring), 'forma(s)')
    else: print('varzea.json sem o Parque Ecológico da Várzea')
# recortar à terra (precisa de costa.json) as zonas de natureza que invadem o mar
f = PAS + 'costa.json'
if os.path.exists(f):
    costa = [e for e in json.load(open(f, encoding='utf-8'))['elements'] if e['type'] == 'way' and e.get('geometry')]
    for z in D['zonas']:
        if z.get('manual'): continue
        if z['id'] == 'espichel':   # o cabo é a península: terra dentro de uma caixa à volta do santuário e do farol
            caixa = [[38.405, -9.228], [38.405, -9.196], [38.432, -9.196], [38.432, -9.228], [38.405, -9.228]]
            novo = so_terra([caixa], costa)
            novo = [r for r in novo if len(r) >= 15]   # sem lascas soltas
            if novo: z['limite'] = novo; print('Cabo Espichel (península):', sum(len(a) for a in novo), 'pontos em', len(novo), 'forma(s)')
            continue
        if z['id'] in ('espichel', 'arrabida') and z.get('limite'):
            antes = sum(len(a) for a in z['limite']); novo = so_terra(z['limite'], costa)
            if novo: z['limite'] = novo; print('Só terra:', z['nome'], antes, '->', sum(len(a) for a in novo), 'pontos em', len(novo), 'forma(s)')
            else: print('Sem resultado ao recortar', z['nome'])
json.dump(D, open(MAPA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
