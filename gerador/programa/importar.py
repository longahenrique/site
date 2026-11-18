#!/usr/bin/env python3
"""Junta ao mapa os dados do OpenStreetMap (ficheiros descarregados com descarregar-dados-mapa.html).
Uso (na raiz do repositório):  python3 gerador/programa/importar.py
Usa, se existirem na pasta gerador/programa/:  equipamentos.json  (ícones e nomes)  e  limites.json  (contornos).
Grava o resultado em mapa.json. Não precisa de rede."""
import json, os, math
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
f = PAS + 'equipamentos.json'
if os.path.exists(f):
    els = json.load(open(f, encoding='utf-8'))['elements']; pts, vistos = [], set()
    for e in els:
        t = e.get('tags', {}); c = cat(t); n = t.get('name'); p = pos(e)
        if not c or not n or not p: continue
        if c == 'desporto' and t.get('leisure') == 'pitch' and len(n) < 4: continue
        k = (c, n.lower())
        if k in vistos: continue          # um só ponto por nome e tipo
        vistos.add(k); pts.append({'cat': c, 'nome': n, 'p': p})
    # nomes de sítios para posicionar: Moagem de Sampaio, Ribeira do Marchante, Várzea
    for e in els:
        t = e.get('tags', {}); n = t.get('name', '')
        if any(x in n for x in ('Moagem', 'Marchante', 'Várzea', 'Varzea')) and pos(e): print('Sítio encontrado:', n, pos(e))
    D['pontos'] = pts; print(len(pts), 'locais com ícone')
# contornos
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
def simplifica(a, tol=0.00004):
    if len(a) < 4: return a
    out = [a[0]]
    for p in a[1:-1]:
        if math.hypot(p[0]-out[-1][0], p[1]-out[-1][1]) > tol: out.append(p)
    out.append(a[-1]); return out
# zona -> nomes no OpenStreetMap (ajustar se for preciso)
NOMES = {'qconde': ['Quinta do Conde'], 'lagoa': ['Lagoa de Albufeira'], 'arrabida': ['Parque Natural da Arrábida', 'Serra da Arrábida'], 'espichel': ['Cabo Espichel'], 'mata': ['Mata Nacional dos Medos', 'Mata de Sesimbra'], 'zambujal': ['Zambujal']}
f = PAS + 'limites.json'
if os.path.exists(f):
    els = json.load(open(f, encoding='utf-8'))['elements']
    for z in D['zonas']:
        nomes = NOMES.get(z['id']);
        if not nomes: continue
        achados = [e for e in els if e.get('tags', {}).get('name') in nomes]
        # preferir fronteiras administrativas de freguesia / áreas protegidas
        achados.sort(key=lambda e: (e['type'] != 'relation', e.get('tags', {}).get('admin_level', '9')))
        aneis = []
        for e in achados[:1]:
            if e['type'] == 'relation': aneis = anel([m for m in e['members'] if m.get('role', 'outer') == 'outer'])
            elif 'geometry' in e: aneis = [[[round(g['lat'], 5), round(g['lon'], 5)] for g in e['geometry']]]
        aneis = [simplifica(a) for a in aneis if len(a) > 3]
        if aneis:
            z['limite'] = aneis; z.pop('poligono', None); z.pop('centro', None); z.pop('raio', None)
            print('Contorno de', z['nome'], '->', len(aneis), 'anel(éis),', sum(len(a) for a in aneis), 'pontos')
        else: print('Sem contorno para', z['nome'], '(mantém o desenho atual)')
json.dump(D, open(MAPA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
