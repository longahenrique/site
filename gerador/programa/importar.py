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
        k = (c, n.lower())
        if k in vistos: continue          # um só ponto por nome e tipo
        vistos.add(k); pts.append({'cat': c, 'nome': n, 'p': p})
    # nomes de sítios para posicionar: Moagem de Sampaio, Ribeira do Marchante, Várzea
    for e in els:
        t = e.get('tags', {}); n = t.get('name', '')
        if any(x in n for x in ('Moagem', 'Marchante', 'Várzea', 'Varzea')) and pos(e): print('Sítio encontrado:', n, pos(e))
    D['pontos'] = pts; print(len(pts), 'locais com ícone')
# contornos
def simplifica(a, tol=0.00004):
    if len(a) < 4: return a
    out = [a[0]]
    for p in a[1:-1]:
        if math.hypot(p[0]-out[-1][0], p[1]-out[-1][1]) > tol: out.append(p)
    out.append(a[-1]); return out
# zona -> nomes no OpenStreetMap (ajustar se for preciso)
NOMES = {'qconde': ['Quinta do Conde'], 'lagoa': ['Lagoa de Albufeira'], 'arrabida': ['Parque Natural da Arrábida', 'Serra da Arrábida'], 'espichel': ['ZPE Cabo Espichel', 'Cabo Espichel'], 'zambujal': ['Zambujal']}
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
f = PAS + 'areas.json'
if os.path.exists(f):
    A = [e for e in json.load(open(f, encoding='utf-8'))['elements'] if e.get('geometry') or e.get('members')]
    def aneis_de(e):
        if e['type'] == 'way': return [[[round(g['lat'], 5), round(g['lon'], 5)] for g in e['geometry']]]
        return anel([m for m in e['members'] if m.get('role', 'outer') == 'outer'])
    def centro(a): return [sum(p[0] for p in a)/len(a), sum(p[1] for p in a)/len(a)]
    def uso(e): t = e.get('tags', {}); return t.get('landuse') or t.get('natural')
    def pertence(e, nome):
        for z in D['zonas']:
            if z['id'] != nome: continue
    for z in D['zonas']:
        if z['id'] == 'zambujal':
            nucleos = [[38.4546, -9.1196], [38.4501, -9.1274], [38.4592, -9.1246]]
            sel = []
            for e in A:
                if uso(e) not in ('residential', 'retail'): continue
                for a in aneis_de(e):
                    if len(a) > 3 and min(math.hypot(centro(a)[0]-n[0], (centro(a)[1]-n[1])*0.78) for n in nucleos) < 0.0045: sel.append(simplifica(a))
            if sel: z['limite'] = sel; z.pop('centro', None); z.pop('raio', None); z['rotulo'] = [38.4546, -9.1196]; print('Contorno de Zambujal ->', len(sel), 'zona(s) urbana(s)')
            else: print('Sem zonas urbanas para o Zambujal')
        if z['id'] == 'mata':
            sel = []; poly = z.get('poligono')
            if not poly: continue
            for e in A:
                if uso(e) not in ('forest', 'wood'): continue
                for a in aneis_de(e):
                    if len(a) > 3 and dentro(centro(a), [poly]): sel.append(simplifica(a))
            if sel: z['limite'] = sel; z.pop('poligono', None); print('Contorno da Mata ->', len(sel), 'mancha(s) de mata')
            else: print('Sem matas encontradas dentro da zona')
json.dump(D, open(MAPA, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
