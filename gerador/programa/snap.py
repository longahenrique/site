#!/usr/bin/env python3
"""Alinha as linhas de mapa.json com as ruas reais (dados do OpenStreetMap).
Uso (na raiz do repositório):  python3 gerador/programa/snap.py gerador/programa/ruas.json
Lê 'pontos' (ou, na primeira vez, 'coords') de cada linha, encontra o caminho pelas ruas entre
pontos consecutivos e grava o resultado em 'coords'. Não precisa de rede."""
import json, math, heapq, sys
from collections import defaultdict
src = sys.argv[1] if len(sys.argv) > 1 else 'gerador/programa/ruas.json'
MAPA = 'gerador/programa/mapa.json'
RUA = {'motorway','motorway_link','trunk','trunk_link','primary','primary_link','secondary','secondary_link','tertiary','tertiary_link','unclassified','residential','living_street','service'}
CUSTO_RUA = {'motorway':9,'motorway_link':9,'trunk':2.5,'trunk_link':2.5,'primary':1.2,'primary_link':1.2,'secondary':1,'secondary_link':1,'tertiary':1,'tertiary_link':1,'unclassified':1.1,'residential':1.15,'living_street':1.3,'service':2.5}
CUSTO_ATIVO = {'cycleway':0.55,'path':0.9,'footway':1.0,'pedestrian':0.9,'track':1.2,'trunk':3,'trunk_link':3,'primary':1.5,'primary_link':1.5,'secondary':1.1,'secondary_link':1.1,'tertiary':1,'tertiary_link':1,'unclassified':1,'residential':0.9,'living_street':0.85,'service':1.6}
def dist(a, b):
    k = math.pi/180; dy = (b[0]-a[0])*111320; dx = (b[1]-a[1])*111320*math.cos(a[0]*k); return math.hypot(dx, dy)
def construir(ways, custos, aceitar):
    pos, adj = {}, defaultdict(list)
    for w in ways:
        h = w.get('tags', {}).get('highway')
        if h not in custos or not aceitar(w): continue
        ids, g = w['nodes'], w['geometry']
        sentido = w['tags'].get('oneway') in ('yes', 'true', '1') and h not in ('cycleway',)
        for i in range(len(ids)-1):
            a, b = ids[i], ids[i+1]; pa, pb = (g[i]['lat'], g[i]['lon']), (g[i+1]['lat'], g[i+1]['lon'])
            pos[a], pos[b] = pa, pb; c = dist(pa, pb)*custos[h]
            adj[a].append((b, c));
            if not sentido or True: adj[b].append((a, c))   # sentido único ignorado: é um traçado indicativo
    # maior componente ligada
    vis, melhor = set(), set()
    for s in list(adj):
        if s in vis: continue
        comp, pil = {s}, [s]; vis.add(s)
        while pil:
            u = pil.pop()
            for v, _ in adj[u]:
                if v not in vis: vis.add(v); comp.add(v); pil.append(v)
        if len(comp) > len(melhor): melhor = comp
    return {n: pos[n] for n in melhor}, {n: [(v, c) for v, c in adj[n] if v in melhor] for n in melhor}
def mais_perto(pos, p):
    return min(pos, key=lambda n: dist(pos[n], p))
def caminho(pos, adj, a, b):
    d, ant, h = {a: 0}, {}, [(0, a)]
    while h:
        c, u = heapq.heappop(h)
        if u == b: break
        if c > d.get(u, 1e18): continue
        for v, w in adj[u]:
            if c+w < d.get(v, 1e18): d[v] = c+w; ant[v] = u; heapq.heappush(h, (c+w, v))
    if b not in d: return None
    r = [b]
    while r[-1] != a: r.append(ant[r[-1]])
    return r[::-1]
def simplificar(pts, tol=2.5):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dm, im = 0, 0
    for i in range(1, len(pts)-1):
        d = dist_seg(pts[i], a, b)
        if d > dm: dm, im = d, i
    if dm > tol: return simplificar(pts[:im+1], tol)[:-1] + simplificar(pts[im:], tol)
    return [a, b]
def dist_seg(p, a, b):
    k = math.cos(a[0]*math.pi/180); ax, ay, bx, by, px, py = a[1]*k, a[0], b[1]*k, b[0], p[1]*k, p[0]
    dx, dy = bx-ax, by-ay; t = 0 if dx == dy == 0 else max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/(dx*dx+dy*dy)))
    return math.hypot(px-(ax+t*dx), py-(ay+t*dy))*111320
ways = [e for e in json.load(open(src, encoding='utf-8'))['elements'] if e.get('type') == 'way' and 'geometry' in e]
print(len(ways), 'ruas lidas')
G_rua = construir(ways, CUSTO_RUA, lambda w: w['tags'].get('access') not in ('no', 'private'))
G_ativo = construir(ways, CUSTO_ATIVO, lambda w: w['tags'].get('access') not in ('no', 'private'))
D = json.load(open(MAPA, encoding='utf-8'))
for l in D['linhas']:
    if l['nome'] == 'Marginal de Sesimbra': continue
    pts = l.setdefault('pontos', l['coords'])
    pos, adj = G_ativo if l['camada'] == 'ativos' else G_rua
    ns = []
    for p in pts:
        n = mais_perto(pos, p)
        if dist(pos[n], p) > 500: print('AVISO', l['nome'], 'ponto a mais de 500 m de uma rua:', p)
        if not ns or ns[-1] != n: ns.append(n)
    out = []
    for a, b in zip(ns, ns[1:]):
        c = caminho(pos, adj, a, b)
        if not c: print('AVISO', l['nome'], 'sem ligação entre dois pontos'); c = [a, b]
        seg = [pos[x] for x in c]
        if sum(dist(seg[i], seg[i+1]) for i in range(len(seg)-1)) > 3*max(dist(seg[0], seg[-1]), 50): print('AVISO', l['nome'], 'desvio grande entre', seg[0], 'e', seg[-1])
        out += seg if not out else seg[1:]
    l['coords'] = [[round(a, 5), round(b, 5)] for a, b in simplificar(out)] if out else pts
    print(l['nome'], len(pts), '->', len(l['coords']), 'pontos')
json.dump(D, open(MAPA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
