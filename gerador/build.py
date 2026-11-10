import re, os, shutil, zipfile, glob, json
H=os.getcwd()   # corre sempre a partir da raiz do repositório
src='gerador/home.html'
GOATCOUNTER='henriquelonga'   # codigo da conta GoatCounter; None = sem estatisticas
GSC_META=None      # valor do meta google-site-verification; None = nao usado
SITE='https://henriquelonga.pt'
# ---- aviso no topo (None = sem aviso) ----
NOTICE_ID='alerta-charles-2026-11'
NOTICE_UNTIL='2026-11-11T23:59:59+00:00'   # Lisboa em novembro = UTC+0
NOTICE_ON=True
NOTICE_HTML=''
NOTICE_JS=''
NOTICE_CSS=''
if NOTICE_ON:
    NOTICE_HTML="""<div class="notice" id="notice" role="region" aria-label="Aviso de alerta meteorológico" hidden>
<div class="wrap">
<div class="notice-body">
<p class="notice-t">Alerta meteorológico em Sesimbra: tempestade Charles</p>
<p>O IPMA prevê precipitação severa, forte agitação marítima e rajadas de vento entre 120 e 140 km/h. A Câmara Municipal de Sesimbra declarou a Situação de Alerta para o concelho, com as escolas e os serviços públicos não essenciais encerrados a 11 de novembro.</p>
<p>Estradas cortadas:</p>
<ul>
<li>Marginal de Sesimbra: encerrada ao público desde 10 de novembro</li>
<li>Avenida dos Combatentes, em Sesimbra: corte de trânsito</li>
<li>Avenida dos Aliados, na Quinta do Conde: corte de trânsito</li>
<li>Acesso ao Porto de Abrigo: interdito a 11 de novembro, entre as 12h e as 24h</li>
</ul>
<p>Evita deslocações desnecessárias e as zonas costeiras. Mais informação no <a href="https://www.sesimbra.pt/noticia-74/municipio-em-situacao-de-alerta-devido-ao-mau-tempo" target="_blank" rel="noopener">site da Câmara Municipal de Sesimbra</a>, no <a href="https://www.ipma.pt/pt/index.html" target="_blank" rel="noopener">IPMA</a> e na <a href="https://prociv.gov.pt/pt/home/" target="_blank" rel="noopener">Proteção Civil</a>. Informação de 10 de novembro de 2026.</p>
</div>
<button type="button" class="notice-close">Fechar aviso</button>
</div>
</div>
"""
    NOTICE_JS='<script>\n(function(){var n=document.getElementById("notice");if(!n)return;var K="hl-notice-%s";\ntry{if(localStorage.getItem(K)==="1"){n.parentNode.removeChild(n);return}}catch(e){}\nif(Date.now()>Date.parse("%s")){n.parentNode.removeChild(n);return}\nn.hidden=false;\nn.querySelector(".notice-close").addEventListener("click",function(){n.hidden=true;try{localStorage.setItem(K,"1")}catch(e){}});\n})();\n</script>\n'%(NOTICE_ID,NOTICE_UNTIL)
    NOTICE_CSS="""
.notice{background:var(--ink);color:var(--paper);padding:14px 0;font:500 16px/1.5 Archivo,"Archivo Fallback","Helvetica Neue",Arial,sans-serif}
.notice[hidden]{display:none}
.notice .wrap{display:flex;gap:20px;align-items:flex-start;justify-content:space-between}
.notice-body{max-width:62em}
.notice p{margin:0 0 6px}
.notice .notice-t{font-weight:800;font-size:18px;line-height:1.3}
.notice ul{margin:2px 0 8px;padding-left:1.2em}
.notice a{color:inherit;text-underline-offset:4px}
.notice-close{flex-shrink:0;padding:7px 13px;border:2px solid currentColor;border-radius:6px;background:transparent;color:inherit;font:700 14px Archivo,"Archivo Fallback",Arial,sans-serif;cursor:pointer}
@media(max-width:700px){.notice .wrap{flex-direction:column-reverse;align-items:stretch}.notice-close{align-self:flex-end}}
"""
s=open(src,encoding='utf-8').read()
def sub1(old,new,cnt=1):
    global s
    if s.count(old)==0 and new in s: return
    assert s.count(old)==cnt,(old[:70],s.count(old)); s=s.replace(old,new)
# ---------- 1. home page edits ----------
sub1('<div><a href="#quem-sou">Quem sou</a>','<div><a href="/biografia">Biografia</a>')
s=re.sub(r'href="/opiniao/([a-z0-9-]+)/"',r'href="/opiniao/\1"',s)
if 'Ver todos os artigos' not in s and 'discurso-de-odio-nao-e-preconceito' not in s:
    sub1('<a href="https://drive.google.com/file/d/16q92wz3G4JKZHOgJozvUaQ9RnJ9ml1iu/view?usp=sharing" target="_blank" rel="noopener">','<a href="/opiniao/discurso-de-odio-nao-e-preconceito-e-so-uma-opiniao">')
if '--pl:' not in s:
    sub1(':root{color-scheme:light;--paper:#faf6ea;',':root{--pl:max(24px,env(safe-area-inset-left,0px));--pr:max(24px,env(safe-area-inset-right,0px));color-scheme:light;--paper:#faf6ea;')
    s,n=re.subn(r'(\.wrap\{max-width:\d+px;margin:0 auto;)padding:0 24px\}',r'\1padding:0 var(--pr) 0 var(--pl)}',s); assert n==1
    s=s.replace('margin:28px -24px 0','margin:28px calc(-1*var(--pr)) 0 calc(-1*var(--pl))')
    sub1('.a11y{position:fixed;left:16px;','.a11y{position:fixed;left:max(16px,env(safe-area-inset-left,0px));')
    sub1('.skip:focus{left:12px;','.skip:focus{left:max(12px,env(safe-area-inset-left,0px));')
    sub1('@media(max-width:700px){h1 br{display:none}}','@media(max-width:700px){h1 br{display:none}}\n@media(max-width:600px){html{scroll-padding-top:calc(env(safe-area-inset-top,0px) + 52px)}}')

if 'sobre-mim' not in s:
    s=s.replace('#quem-sou','#sobre-mim').replace('id="quem-sou"','id="sobre-mim"')
    sub1('if(location.hash==="#sobre")','if(location.hash==="#sobre"||location.hash==="#quem-sou")')
    sub1('<h2>Quem sou</h2>','<h2>Sobre mim</h2>')
    sub1('href="#sobre-mim">Quem sou</a>','href="#sobre-mim">Sobre mim</a>')
if '<a href="#opiniao">Opinião</a>' in s: sub1('<a href="#opiniao">Opinião</a>','<a href="/opiniao">Opinião</a>')
if 'queremos AMar.' in s: sub1('queremos AMar.','queremos amar.')
if 'font-size:16px;line-height:1.55}' in s: sub1('.area details p{margin:.45em 0 .3em;font-size:16px;line-height:1.55}','.area details p{margin:.5em 0 .35em;font-size:18px;line-height:1.6}')
if 'Ver todos os artigos' not in s:
    m=re.search(r'<ul class="articles">(.*?)</ul>',s,flags=re.S); assert m
    lis=re.findall(r'<li>.*?</li>',m.group(1),flags=re.S); assert len(lis)==5,len(lis)
    s=s.replace(m.group(0),'<ul class="articles">'+''.join(lis[:3])+'</ul>\n<p style="margin:36px 0 0"><a class="btn" href="/opiniao">Ver todos os artigos</a></p>')
if '@media(hover:hover)' not in s:
    s,n=re.subn(r'(?m)^([^{}\n]*:hover[^{}\n]*\{[^{}]*\})$',lambda m:'@media(hover:hover){'+m.group(1)+'}',s); assert n==4,n
open(src,'w',encoding='utf-8').write(s)
if '/privacidade' not in s:
    sub1('Todos os direitos reservados.</footer>','Todos os direitos reservados. <a href="/privacidade">Privacidade</a> | <a href="/acessibilidade">Acessibilidade</a></footer>')
    open(src,'w',encoding='utf-8').write(s)
if 'data-copy-target' not in s:
    sub1('document.getElementById("year").textContent=new Date().getFullYear();','''document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest("[data-copy-target]");if(!b)return;var el=document.getElementById(b.getAttribute("data-copy-target"));if(!el)return;var u=el.innerText,t=b.textContent;
function ok(){b.textContent="Copiado";setTimeout(function(){b.textContent=t},2000)}
if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(u).then(ok,function(){window.prompt("Copia o texto:",u)})}else{window.prompt("Copia o texto:",u)}});
document.getElementById("year").textContent=new Date().getFullYear();''')
s=s.replace('href="/opiniao"','href="/opiniao/"').replace('<span class="s">Eu voto, eu opino</span>','<span class="s">Eu Voto</span>')
if 'data-copy' not in s:
    sub1('document.getElementById("year").textContent=new Date().getFullYear();','''document.addEventListener("click",function(e){var b=e.target.closest&&e.target.closest("[data-copy]");if(!b)return;var u=location.origin+location.pathname,t=b.textContent;
function ok(){b.textContent="Ligação copiada";setTimeout(function(){b.textContent=t},2000)}
if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(u).then(ok,function(){window.prompt("Copia a ligação:",u)})}else{window.prompt("Copia a ligação:",u)}});
document.getElementById("year").textContent=new Date().getFullYear();''')
open(src,'w',encoding='utf-8').write(s)
# ---------- 2. reusable pieces ----------
css=re.search(r'<style>(.*?)</style>',s,flags=re.S).group(1).strip()
header=re.search(r'<header class="top sea">.*?</header>',s,flags=re.S).group(0)
for a in ('programa',): header=header.replace('href="#%s"'%a,'href="/#%s"'%a)
contact=re.search(r'<div class="sea" id="contacto">.*?</footer>\n</div>\n</div>',s,flags=re.S).group(0)
a11y=re.search(r'<div class="a11y">.*?</div>\n</div>\n',s,flags=re.S).group(0)
fav=re.search(r'<link rel="icon"[^>]*>',s).group(0)+'\n'+re.search(r'<link rel="apple-touch-icon"[^>]*>',s).group(0)
js=re.findall(r'<script>(.*?)</script>',s,flags=re.S)[-1].strip()
img=re.search(r'<img src="(data:image/webp;base64,[^"]+)" width="(\d+)" height="(\d+)" alt="([^"]*)">',s)
article_css='''
.article{background:var(--paper);padding:56px 0 80px}
main:focus,.article:focus{outline:none}
.article .crumb{margin:0 0 30px;font:600 16px Archivo,"Helvetica Neue",Arial,sans-serif}
.article .crumb a{text-underline-offset:5px}
.article h1{font-size:clamp(34px,6.2vw,66px);line-height:1.06;margin:0 0 18px;max-width:14em}
.article .meta{margin:0 0 42px;font:500 17px Archivo,"Helvetica Neue",Arial,sans-serif;color:var(--muted)}
.article .text{max-width:36em}
.article .text p{margin:0 0 1.25em;font-size:20px;line-height:1.75}
.article .after{display:flex;flex-wrap:wrap;gap:12px 28px;align-items:center;margin-top:44px;padding-top:28px;border-top:1px solid var(--line);font:600 16px Archivo,"Helvetica Neue",Arial,sans-serif}
.article .after a{text-underline-offset:5px}
.article .text h2{font-size:clamp(24px,3.4vw,30px);line-height:1.2;margin:1.7em 0 .5em}
.article .text ul{margin:0 0 1.25em;padding-left:1.2em}
.article .text li{margin-bottom:.5em;font-size:20px;line-height:1.7}
.article .text a{text-underline-offset:4px}
.share,.more-articles{margin-top:44px}
.share h2,.more-articles h2{margin:0 0 14px;font:800 22px/1.2 Archivo,"Helvetica Neue",Arial,sans-serif}
.share ul{list-style:none;display:flex;flex-wrap:wrap;gap:10px;margin:0;padding:0}
.share a,.share button{display:inline-block;padding:9px 16px;border:2px solid var(--ink);border-radius:6px;background:transparent;color:var(--ink);font:700 15px Archivo,"Helvetica Neue",Arial,sans-serif;text-decoration:none;cursor:pointer}
@media(hover:hover){.share a:hover,.share button:hover{background:var(--ink);color:var(--paper)}}
.more-articles .articles{max-width:44em}
.rss{margin:28px 0 0;font:600 16px Archivo,"Helvetica Neue",Arial,sans-serif}
.rss a{text-underline-offset:5px}
@media(max-width:600px){.article{padding:36px 0 52px}.article .text p{font-size:19px}}
'''
bio_css='''
#bio h1{font-size:clamp(36px,6vw,60px);line-height:1.05;margin:0 0 28px;text-wrap:balance}
#bio .portrait{flex-direction:column;align-items:center;align-self:start;padding:28px 0 34px}
#bio .btn-in,#bio .btn-out{display:flex;flex-wrap:wrap;gap:12px}
#bio .btn-in{justify-content:center;margin:-10px 0 0;padding:0 16px}
#bio .btn-in .btn,#bio .btn-out .btn{margin:0}
@media(min-width:1000px){#bio .who{grid-template-rows:auto auto 1fr}#bio .who .prose{grid-row:2 / span 2}#bio .who .btn-out{grid-column:2;grid-row:3;align-self:start;margin:22px 0 0}#bio .portrait{padding-bottom:0}#bio .btn-in{display:none}}
@media(max-width:999px){#bio .btn-out{display:none}}
.results h2{margin-bottom:6px}
.results h3{margin:36px 0 12px;font:800 24px/1.2 Archivo,"Helvetica Neue",Arial,sans-serif}
.tbl{overflow-x:auto;-webkit-overflow-scrolling:touch}
.tbl:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
table.res{width:100%;min-width:600px;border-collapse:collapse;font:500 17px Archivo,"Helvetica Neue",Arial,sans-serif}
.res th,.res td{padding:13px 14px 13px 0;text-align:left;border-top:2px solid rgba(20,20,20,.3);white-space:nowrap}
.res thead th{border-top:0;border-bottom:2px solid var(--ink);font-weight:800}
.res .n{text-align:right;padding-right:24px}
.res abbr{text-decoration:none}
@media(max-width:600px){#bio h1{margin-bottom:18px}.results h3{font-size:21px}}
'''
SOCIAL_META='<meta property="og:site_name" content="Henrique Longa">\n<meta name="twitter:site" content="@henriquelonga">\n<meta name="twitter:creator" content="@henriquelonga">'
PROFILE_META='<meta property="profile:first_name" content="Henrique">\n<meta property="profile:last_name" content="Longa">'
FONTFACE='''@font-face{font-family:Archivo;font-style:normal;font-weight:500;font-display:swap;src:url(/fonts/archivo-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:Archivo;font-style:normal;font-weight:800;font-display:swap;src:url(/fonts/archivo-latin-800-normal.woff2) format("woff2")}
@font-face{font-family:"Archivo Fallback";font-weight:500;src:local("Arial"),local("ArialMT"),local("Helvetica Neue"),local("Helvetica"),local("Liberation Sans")}
@font-face{font-family:"Archivo Fallback";font-weight:800;src:local("Arial Bold"),local("Arial-BoldMT"),local("Helvetica Neue Bold"),local("Helvetica Bold"),local("Liberation Sans Bold")}
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/source-serif-4-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:600;font-display:swap;src:url(/fonts/source-serif-4-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Source Serif 4";font-style:italic;font-weight:400;font-display:swap;src:url(/fonts/source-serif-4-latin-400-italic.woff2) format("woff2")}
'''
import json
def extra_head(ld=None):
    out='<link rel="alternate" type="application/rss+xml" title="Henrique Longa: artigos de opinião" href="/feed.xml">\n'
    if GSC_META: out+='<meta name="google-site-verification" content="%s">\n'%GSC_META
    if ld: out+='<script type="application/ld+json">%s</script>\n'%json.dumps(ld,ensure_ascii=False,separators=(',',':'))
    if GOATCOUNTER: out+='<script data-goatcounter="https://%s.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>\n'%GOATCOUNTER
    return out
def head(path,title,desc,css_text,ogtype='article',ld=None,meta_extra='',image='https://henriquelonga.pt/og-image.jpg'):
    url='https://henriquelonga.pt'+path
    return f'''<!DOCTYPE html>
<html lang="pt-PT">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title} | Henrique Longa</title>
<meta name="description" content="{desc}">
<meta name="color-scheme" content="light only">
<link rel="canonical" href="{url}">
{fav}
<meta property="og:type" content="{ogtype}">
<meta property="og:locale" content="pt_PT">
<meta property="og:title" content="{title} | Henrique Longa">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{SOCIAL_META}
{meta_extra}{extra_head(ld)}<style>
{FONTFACE}{css_text.replace('Archivo,','Archivo,"Archivo Fallback",')}{NOTICE_CSS}
</style>
</head>
'''
def body(hdr,main,extra=''):
    return f'''<body>
<a class="skip" href="#conteudo">Saltar para o conteúdo principal</a>
<div id="page">
{NOTICE_HTML}{hdr}
{main}
{contact}
</div>
{a11y}<script>
{js}
</script>
{extra}{NOTICE_JS}</body>
</html>
'''
def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
# ---------- 3. artigos (ficheiros .md na pasta artigos/) ----------
MESES=['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro']
def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def inline(t): return re.sub(r'\*([^*\n]+)\*',r'<em>\1</em>',esc(t))
def erro(f,msg): raise SystemExit('ERRO no artigo %s: %s'%(f,msg))
arts={}
for f in sorted(glob.glob('artigos/*.md')):
    slug=os.path.basename(f)[:-3]
    if slug.startswith('_'): continue
    raw=open(f,encoding='utf-8').read().replace('\r\n','\n').lstrip('\ufeff')
    m=re.match(r'^---\n(.*?)\n---\n(.*)$',raw,re.S)
    if not m: erro(f,'o ficheiro tem de começar por uma linha --- e ter outra linha --- depois da informação')
    meta={}
    for line in m.group(1).split('\n'):
        if ':' in line:
            k,v=line.split(':',1); meta[k.strip().lower()]=v.strip()
    for k in ('titulo','data','meio','linha'):
        if not meta.get(k): erro(f,'falta a linha "%s:"'%k)
    if not re.match(r'^\d{4}-\d{2}-\d{2}$',meta['data']): erro(f,'a data tem de ser assim: 2026-09-16')
    y,mo,dd=[int(x) for x in meta['data'].split('-')]
    time='<time datetime="%s">%d de %s de %d</time>'%(meta['data'],dd,MESES[mo-1],y)
    paras=[p.strip().replace('\n',' ') for p in re.split(r'\n\s*\n',m.group(2).strip()) if p.strip()]
    if not paras: erro(f,'o artigo não tem texto')
    after=''
    if meta.get('link'): after+='<a href="%s" target="_blank" rel="noopener">%s</a>\n'%(esc(meta['link']),esc(meta.get('link-texto') or 'Ler o artigo original'))
    after+='<a href="/opiniao">Todos os artigos</a>\n'
    desc=meta.get('descricao') or re.sub(r'\s+',' ',paras[0])[:160]
    arts[slug]=dict(title=esc(meta['titulo']),desc=esc(desc).replace('"','&quot;'),meta=esc(meta['linha']).replace('{data}',time),text=''.join('<p>%s</p>\n'%inline(p) for p in paras),after=after,meio=meta['meio'])
if not arts: raise SystemExit('ERRO: não há artigos na pasta artigos/')
PERSON={"@type":"Person","@id":SITE+"/#pessoa","name":"Henrique Longa","alternateName":"Henrique José Longa Correia","url":SITE+"/","image":SITE+"/fotos/henrique-longa-retrato.jpg","description":"Estudante de Química Aplicada na NOVA FCT e ativista cívico, membro do LIVRE em Sesimbra.","jobTitle":"Estudante e ativista cívico","affiliation":[{"@type":"Organization","name":"LIVRE"},{"@type":"Organization","name":"Faculdade de Ciências e Tecnologia da Universidade NOVA de Lisboa"},{"@type":"Organization","name":"Associação Nacional de Estudantes de Química"}],"sameAs":["https://www.instagram.com/henriquelonga","https://www.facebook.com/henriquelongacorreia","https://x.com/henriquelonga","https://www.linkedin.com/in/henriquelonga","https://linktr.ee/henriquelonga"]}
WEBSITE={"@type":"WebSite","@id":SITE+"/#site","url":SITE+"/","name":"Henrique Longa","inLanguage":"pt-PT","publisher":{"@id":SITE+"/#pessoa"}}
# ---------- 4. write the site ----------
shutil.rmtree('_site',ignore_errors=True); os.makedirs('_site/opiniao')
import urllib.parse, html as _h
OUT={k:v['meio'] for k,v in arts.items()}
ORDER=sorted(arts,key=lambda k:re.search(r'datetime="(\d{4}-\d{2}(?:-\d{2})?)"',arts[k]['meta']).group(1),reverse=True)
enc=lambda t:urllib.parse.quote(t,safe='')
from PIL import Image, ImageDraw, ImageFont
_FD='gerador/fonts-og/'
os.makedirs('_site/og',exist_ok=True)
def og_image(slug,title,line):
    W,H=1200,630; im=Image.new('RGB',(W,H),(0xb4,0xca,0xad))
    cut=Image.open('gerador/retrato-recortado.png').convert('RGBA'); ph=int(H*0.98); pw=int(cut.width*ph/cut.height)
    pc=cut.resize((pw,ph),Image.LANCZOS); im.paste(pc,(W-pw-40,H-ph),pc)
    d=ImageDraw.Draw(im); INK=(20,20,20); colw=W-pw-40-70-30
    def wrap(text,f):
        lines,cur=[],''
        for w in text.split():
            t=(cur+' '+w).strip()
            if f.getlength(t)<=colw or not cur: cur=t
            else: lines.append(cur); cur=w
        lines.append(cur); return lines
    for size in range(76,35,-2):
        f=ImageFont.truetype(_FD+'InterDisplay-ExtraBold.otf',size); ls=wrap(title,f)
        if len(ls)<=6 and len(ls)*size*1.13<=330 and max(f.getlength(x) for x in ls)<=colw: break
    d.text((70,60),'Artigo de opinião',font=ImageFont.truetype(_FD+'Inter-SemiBold.otf',30),fill=INK)
    y=125
    for x in ls: d.text((70,y),x,font=f,fill=INK); y+=int(size*1.13)
    d.text((70,H-118),line,font=ImageFont.truetype(_FD+'Inter-SemiBold.otf',30),fill=INK)
    d.text((70,H-72),'henriquelonga.pt',font=ImageFont.truetype(_FD+'Inter-Medium.otf',28),fill=INK)
    im.save('_site/og/%s.jpg'%slug,quality=88,optimize=True)
for slug,d in arts.items():
    url=SITE+'/opiniao/'+slug; tt=_h.unescape(re.sub('<[^>]+>','',d['title']))
    _when=re.search(r'<time[^>]*>(.*?)</time>',d['meta']).group(1)
    og_image(slug,tt,OUT[slug]+', '+_when)
    ogimg=SITE+'/og/'+slug+'.jpg'
    share=f'''<div class="share">
<h2>Partilhar</h2>
<ul>
<li><button type="button" data-copy>Copiar ligação</button></li>
<li><a href="https://wa.me/?text={enc(tt+' '+url)}" target="_blank" rel="noopener">WhatsApp</a></li>
<li><a href="https://x.com/intent/post?url={enc(url)}&amp;text={enc(tt)}" target="_blank" rel="noopener">X</a></li>
<li><a href="https://www.facebook.com/sharer/sharer.php?u={enc(url)}" target="_blank" rel="noopener">Facebook</a></li>
<li><a href="https://www.linkedin.com/sharing/share-offsite/?url={enc(url)}" target="_blank" rel="noopener">LinkedIn</a></li>
<li><a href="mailto:?subject={enc(tt)}&amp;body={enc(url)}">Email</a></li>
</ul>
</div>
'''
    rel=[k for k in ORDER if k!=slug][:2]
    more='<div class="more-articles">\n<h2>Outros artigos</h2>\n<ul class="articles">\n'+''.join('<li><a href="/opiniao/%s"><span class="t">%s</span><span class="s">%s, %s</span></a></li>\n'%(r,arts[r]['title'],OUT[r],re.search(r'<time[^>]*>(.*?)</time>',arts[r]['meta']).group(1)) for r in rel)+'</ul>\n</div>\n'
    main=f'''<main class="article" id="conteudo" tabindex="-1">
<div class="wrap">
<p class="crumb"><a href="/opiniao">← Todos os artigos de opinião</a></p>
<h1>{d['title']}</h1>
<p class="meta">{d['meta']}</p>
<div class="text">
{d['text']}</div>
<div class="after">
{d['after']}</div>
{share}{more}</div>
</main>'''
    iso=re.search(r'datetime="(\d{4}-\d{2}(?:-\d{2})?)"',d['meta']).group(1)
    orig=re.search(r'href="(https?://[^"]+)"',d['after'])
    ld={"@context":"https://schema.org","@type":"Article","headline":re.sub('<[^>]+>','',d['title']),"description":d['desc'],"inLanguage":"pt-PT","datePublished":iso,"url":SITE+'/opiniao/'+slug,"mainEntityOfPage":SITE+'/opiniao/'+slug,"image":ogimg,"author":PERSON,"publisher":{"@id":SITE+"/#pessoa"}}
    if orig: ld["sameAs"]=orig.group(1)
    open(f'_site/opiniao/{slug}.html','w',encoding='utf-8').write(head(f'/opiniao/{slug}',d['title'],d['desc'],css+'\n'+article_css,'article',ld,f'<meta property="article:published_time" content="{iso}">\n<meta property="article:author" content="{SITE}/biografia">\n<meta property="article:section" content="Opinião">\n<meta property="og:image:alt" content="{esc(tt)}, artigo de opinião de Henrique Longa">\n',ogimg)+body(header,main))
# biography page
bio_paras=['Henrique José Longa Correia, nascido a 1 de abril de 2005 em Lisboa e natural de Sesimbra, é um estudante e ativista cívico associado ao partido LIVRE.',
'Henrique Longa é aluno na Faculdade de Ciências e Tecnologia da Universidade NOVA de Lisboa, onde realiza a Licenciatura em Química Aplicada. No seu percurso académico, focou a sua investigação no âmbito da Síntese Orgânica.',
'O seu percurso é fortemente marcado pelo associativismo e pelo envolvimento cívico, a começar por um percurso de cerca de doze anos no Escutismo. Integrou a Greve Climática Estudantil e o movimento internacional Fridays for Future, participando ativamente na organização de greves pelo clima e ações de sensibilização. Desta interseção entre sustentabilidade, juventude e bem-estar resultou a coautoria do <em>Teenager Climate Guide: Promover a comunicação e a saúde mental no contexto da crise climática</em>, um manual pioneiro publicado pela Ecopsi e Greve Climática Estudantil para apoiar jovens ativistas na comunicação e na preservação da saúde mental.',
'Paralelamente, assumiu responsabilidades associativas como dirigente na Associação Nacional de Estudantes de Química, exercendo atualmente funções de Vice-Presidente para as Operações, colaborou com o Conselho Nacional da Juventude e integrou a comissão pedagógica do seu curso e a estrutura da Associação de Estudantes da NOVA FCT.',
'Na política partidária, entrou para o Partido LIVRE em janeiro de 2024. Integra, desde agosto de 2024, o Grupo de Coordenação Local do Núcleo Territorial Distrital de Setúbal. Nas Eleições Legislativas de 2025 integrou a lista do partido pelo círculo eleitoral de Setúbal, e no mesmo ano assumiu o papel de cabeça-de-lista à Assembleia Municipal de Sesimbra nas Eleições Autárquicas, sendo um dos candidatos mais jovens.']
def table(tid,cols,rows):
    th=''.join('<th scope="col"%s>%s</th>'%(' class="n"' if c[1] else '',c[0]) for c in cols)
    tr=''.join('<tr>'+''.join(('<td class="n">%s</td>' if cols[i][1] else '<td>%s</td>')%v for i,v in enumerate(r))+'</tr>' for r in rows)
    return f'<div class="tbl" role="region" aria-labelledby="{tid}" tabindex="0"><table class="res"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'
cl='<abbr title="Classificação do partido">Cl.</abbr>'
t1=table('t1',[('Data',0),('Partido',0),('Círculo eleitoral',0),('Posição',0),(cl,1),('Votos',1),('%',1),('Resultado',0)],[['2025','Livre (L)','Setúbal','15.º (em 18)','5.º','28&nbsp;700','5,84','Não eleito']])
t2=table('t2',[('Data',0),('Partido',0),('Concelho',0),('Posição',0),(cl,1),('Votos',1),('%',1),('Resultado',0)],[['2025','Livre (L)','Sesimbra','1.º (em 21)','6.º','797','3,27','Não eleito']])
bio_main=f'''<main id="conteudo" tabindex="-1">
<section id="bio">
<div class="wrap who">
<h1>Biografia</h1>
<div class="prose">
{''.join('<p>%s</p>\n'%p for p in bio_paras)}</div>
<figure class="portrait"><img src="{img.group(1)}" width="{img.group(2)}" height="{img.group(3)}" alt="{img.group(4)}"><div class="btn-in"><a class="btn" href="/galeria">Galeria de fotos</a></div></figure>
<div class="btn-out"><a class="btn" href="/galeria">Galeria de fotos</a></div>
</div>
</section>
<section class="tint results" id="resultados">
<div class="wrap">
<h2>Resultados eleitorais</h2>
<h3 id="t1">Eleições legislativas</h3>
{t1}
<h3 id="t2">Eleições autárquicas: Assembleia Municipal</h3>
{t2}
</div>
</section>
</main>'''
bio_header=header.replace('<a href="/biografia">','<a href="/biografia" aria-current="page">')
bio_desc='Henrique José Longa Correia, nascido a 1 de abril de 2005 em Lisboa e natural de Sesimbra, é um estudante e ativista cívico associado ao partido LIVRE.'
open('_site/biografia.html','w',encoding='utf-8').write(head('/biografia','Biografia',bio_desc,css.replace('#sobre-mim','#bio')+'\n'+bio_css,'profile',{"@context":"https://schema.org","@type":"ProfilePage","url":SITE+"/biografia","name":"Biografia | Henrique Longa","inLanguage":"pt-PT","mainEntity":PERSON},PROFILE_META+'\n')+body(bio_header,bio_main))

import unicodedata, html as _h
def norm(t): return ''.join(c for c in unicodedata.normalize('NFD',t.lower()) if unicodedata.category(c)!='Mn')
OUT={k:v['meio'] for k,v in arts.items()}
rows=[]
for slug,d in arts.items():
    iso=re.search(r'datetime="(\d{4}-\d{2}(?:-\d{2})?)"',d['meta']).group(1); when=re.search(r'<time[^>]*>(.*?)</time>',d['meta']).group(1)
    paras=[_h.unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<p>(.*?)</p>',d['text'],flags=re.S)]
    ex=paras[0]
    if len(ex)>200: ex=ex[:200].rsplit(' ',1)[0].rstrip(' ,;:.')+'…'
    rows.append((iso,slug,d,OUT[slug],when,ex,norm(_h.unescape(re.sub('<[^>]+>','',d['title']))+' '+' '.join(paras))))
rows.sort(reverse=True)
q=lambda t:esc(t).replace('"','&quot;')
lis=''.join(f'<li data-y="{iso[:4]}" data-o="{q(o)}" data-s="{q(sx)}"><a href="/opiniao/{slug}"><span class="t">{d["title"]}</span><span class="s">{esc(o)}, {when}</span><span class="x">{esc(ex)}</span></a></li>\n' for iso,slug,d,o,when,ex,sx in rows)
years=sorted({r[0][:4] for r in rows},reverse=True); outs=sorted({r[3] for r in rows})
opts=lambda L:''.join(f'<option value="{esc(v)}">{esc(v)}</option>' for v in L)
list_css=r"""
.articles .x{display:block;margin-top:10px;font-size:17px;line-height:1.6}
.articles li[hidden]{display:none}
.ctl{display:flex;flex-wrap:wrap;gap:16px;margin:0 0 20px;max-width:44em}
.ctl .f{display:flex;flex-direction:column;gap:6px;font:600 15px Archivo,"Helvetica Neue",Arial,sans-serif}
.ctl .grow{flex:1 1 280px}
.ctl input,.ctl select{min-width:0;padding:12px 14px;font:500 17px Archivo,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--paper);border:2px solid var(--ink);border-radius:6px}
.ctl input:focus-visible,.ctl select:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.count{margin:0 0 8px;font:600 16px Archivo,"Helvetica Neue",Arial,sans-serif;color:var(--muted)}
#none{margin:24px 0;font-size:19px}
"""
list_main=f"""<main class="article" id="conteudo" tabindex="-1">
<div class="wrap">
<h1>Artigos de opinião</h1>
<form class="ctl" role="search" aria-label="Pesquisar artigos" onsubmit="return false">
<label class="f grow"><span>Pesquisar</span><input type="search" id="q" placeholder="Palavra ou título" autocomplete="off"></label>
<label class="f"><span>Ano</span><select id="y"><option value="">Todos</option>{opts(years)}</select></label>
<label class="f"><span>Publicação</span><select id="o"><option value="">Todas</option>{opts(outs)}</select></label>
</form>
<p class="count" id="count" aria-live="polite"></p>
<ul class="articles" id="list">
{lis}</ul>
<p class="rss"><a href="/feed.xml">Subscrever por RSS</a></p>
<p id="none" hidden>Não existem artigos com estes critérios</p>
</div>
</main>"""
list_js=r"""<script>
(function(){
var q=document.getElementById("q"),y=document.getElementById("y"),o=document.getElementById("o"),items=[].slice.call(document.querySelectorAll("#list li")),c=document.getElementById("count"),n=document.getElementById("none");
function norm(t){return t.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"")}
function sync(){var p=new URLSearchParams();if(q.value.trim())p.set("q",q.value.trim());if(y.value)p.set("ano",y.value);if(o.value)p.set("publicacao",o.value);var s=p.toString(),path=location.pathname.replace(/\/$/,"");history.replaceState(null,"",path+(s?"?"+s:"")+location.hash)}
function run(){var t=norm(q.value.trim()),k=0;
items.forEach(function(li){var ok=(!y.value||li.getAttribute("data-y")===y.value)&&(!o.value||li.getAttribute("data-o")===o.value)&&(!t||li.getAttribute("data-s").indexOf(t)>-1);li.hidden=!ok;if(ok)k++});
c.textContent=k===1?"1 artigo":k+" artigos";n.hidden=k>0;sync()}
function setv(el,v){if(!v)return;for(var i=0;i<el.options.length;i++)if(el.options[i].value===v){el.value=v;return}}
var sp=new URLSearchParams(location.search);q.value=sp.get("q")||"";setv(y,sp.get("ano"));setv(o,sp.get("publicacao"));
[q,y,o].forEach(function(e){e.addEventListener("input",run);e.addEventListener("change",run)});
run();
})();
</script>
"""
list_header=header.replace('<a href="/opiniao">','<a href="/opiniao" aria-current="page">')
open('_site/opiniao/index.html','w',encoding='utf-8').write(head('/opiniao/','Artigos de opinião','Artigos de opinião de Henrique Longa sobre Sesimbra, habitação, regionalização, juventude e democracia.',css+'\n'+article_css+list_css,'website')+body(list_header,list_main,list_js))

# ---------- gallery ----------
from PIL import Image, ImageOps
GAL=json.load(open('gerador/galeria.json',encoding='utf-8'))
PHOTOS=[dict(file=g['ficheiro'],src='fotos-originais/'+g['original'],title=g['titulo'],desc=g.get('legenda'),alt=g['alt'],credit=g.get('credito')) for g in GAL]
os.makedirs('_site/fotos/miniaturas',exist_ok=True)
items=''
with zipfile.ZipFile('_site/fotos/henrique-longa-fotografias.zip','w',zipfile.ZIP_STORED) as zf:
    for ph in PHOTOS:
        shutil.copy(ph['src'],'_site/fotos/'+ph['file']); zf.write(ph['src'],ph['file'])
        im=Image.open(ph['src']); full=im.size
        t=ImageOps.exif_transpose(im).convert('RGB'); t.thumbnail((900,900)); t.save('_site/fotos/miniaturas/'+ph['file'],'JPEG',quality=84,optimize=True)
        mb=('%.1f'%(os.path.getsize(ph['src'])/1e6)).replace('.',',')
        desc='<span class="gd">%s</span>'%esc(ph['desc']) if ph.get('desc') else ''
        cred='<span class="gc">Fotografia: %s</span>'%esc(ph['credit']) if ph['credit'] else ''
        items+=f'<li><figure><a href="/fotos/{ph["file"]}" target="_blank" rel="noopener"><img src="/fotos/miniaturas/{ph["file"]}" width="{t.width}" height="{t.height}" alt="{esc(ph["alt"])}" loading="lazy"></a><figcaption><span class="gt">{ph["title"]}</span>{desc}<span class="gm">JPG, {full[0]} × {full[1]} px, {mb} MB</span>{cred}<a class="dl" href="/fotos/{ph["file"]}" download>Descarregar</a></figcaption></figure></li>\n'
gal_css="""
.gal-all{margin:26px 0 8px}
.gal{list-style:none;margin:28px 0 0;padding:0;columns:300px;column-gap:32px}
.gal li{break-inside:avoid;margin:0 0 36px}
.gal figure{margin:0}
.gal img{display:block;width:100%;height:auto;border-radius:4px;background:var(--sea)}
.gal figcaption{display:flex;flex-direction:column;gap:3px;padding-top:12px;font:500 15px Archivo,"Helvetica Neue",Arial,sans-serif}
.gal .gt{font-weight:800;font-size:19px}
.gal .gd{font-size:16px}
.gal .gm,.gal .gc{color:var(--muted)}
.gal .dl{align-self:flex-start;margin-top:10px;padding:9px 16px;border:2px solid var(--ink);border-radius:6px;font-weight:800;text-decoration:none}
@media(hover:hover){.gal .dl:hover{background:var(--ink);color:var(--paper)}}
"""
GAL_BACK_JS=r'''<script>
(function(){var a=document.getElementById("gal-back");if(!a)return;try{var r=new URL(document.referrer);if(r.origin===location.origin&&r.pathname.replace(/\/$/,"")==="/imprensa"){a.href="/imprensa";a.textContent="← Imprensa"}}catch(e){}})();
</script>
'''
gal_main=f"""<main class="article" id="conteudo" tabindex="-1">
<div class="wrap">
<p class="crumb"><a href="/biografia" id="gal-back">← Biografia</a></p>
<h1>Galeria de fotos</h1>
<p class="gal-all"><a class="btn" href="/fotos/henrique-longa-fotografias.zip" download>Descarregar todas (.zip)</a></p>
<ul class="gal">
{items}</ul>
</div>
</main>"""
open('_site/galeria.html','w',encoding='utf-8').write(head('/galeria','Galeria de fotos','Fotografias de Henrique Longa para descarregar.',css+'\n'+article_css+gal_css,'website')+body(header,gal_main,GAL_BACK_JS))
# ---------- 404 (also turns /page/ into /page) ----------
nf_main="""<main class="article" id="conteudo" tabindex="-1">
<div class="wrap">
<h1>Página não encontrada</h1>
<p class="meta">O endereço que abriste não existe ou mudou.</p>
<div class="after">
<a href="/">Página inicial</a>
<a href="/opiniao">Artigos de opinião</a>
<a href="/biografia">Biografia</a>
</div>
</div>
</main>"""
nf=head('/404','Página não encontrada','Página não encontrada.',css+'\n'+article_css,'website')+body(header,nf_main)
nf=re.sub(r'<link rel="canonical"[^>]*>\n','',nf); nf=re.sub(r'<meta property="og:url"[^>]*>\n','',nf)
nf=nf.replace('<style>','<meta name="robots" content="noindex">\n<script>(function(){var p=location.pathname;if(p.length>1&&/\\/$/.test(p)){location.replace(p.replace(/\\/+$/,"")+location.search+location.hash)}})();</script>\n<style>',1)
open('_site/404.html','w',encoding='utf-8').write(nf)
shutil.copy('og-image.jpg','_site/og-image.jpg')
if os.path.isdir('fonts'): shutil.copytree('fonts','_site/fonts')
if os.path.exists('CNAME'): shutil.copy('CNAME','_site/CNAME')
open('_site/.nojekyll','w').close()

# ---------- legal pages ----------
LEGAL_DATE='novembro de 2026'
def legal_page(path,title,desc,paras_html):
    main=f"""<main class="article" id="conteudo" tabindex="-1">
<div class="wrap">
<h1>{title}</h1>
<p class="meta">Atualizada em {LEGAL_DATE}.</p>
<div class="text">
{paras_html}</div>
</div>
</main>"""
    return head(path,title,desc,css+'\n'+article_css,'website')+body(header,main)
EMAIL='geral@henriquelonga.pt'
stats = ('<h2>Estatísticas de visitas</h2>\n<p>Para perceber que páginas são lidas, este site usa o GoatCounter, um serviço de estatísticas que não usa cookies, não guarda o teu endereço IP e não identifica visitantes individuais. Recolhe apenas dados agregados, como a página visitada, o tipo de dispositivo e de navegador, o país e a origem da visita. A base legal é o interesse legítimo em saber como o site é usado. Os dados de estatísticas são conservados por um máximo de 24 meses. Para o fazer, o teu navegador faz um pedido ao serviço GoatCounter (goatcounter.com).</p>\n' if GOATCOUNTER else '')
priv=f"""<p>Esta página explica que dados pessoais este site trata e porquê. Em resumo: o site não tem contas, formulários nem comentários, não usa cookies e não tem publicidade.</p>
<h2>Quem é o responsável</h2>
<p>O responsável pelo tratamento é Henrique José Longa Correia. Para qualquer questão sobre privacidade, escreve para <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
<h2>O que acontece quando visitas o site</h2>
<ul>
<li>O site é alojado no GitHub Pages, um serviço da GitHub, Inc. Como em qualquer alojamento, este serviço pode registar dados técnicos do teu pedido, como o endereço IP, para fornecer o site e por razões de segurança. Estes dados são tratados pela GitHub, que pode tratá-los nos Estados Unidos, segundo a sua própria política de privacidade. Segundo a GitHub, as transferências de dados para fora do Espaço Económico Europeu assentam em cláusulas contratuais-tipo aprovadas pela Comissão Europeia e no Quadro de Privacidade de Dados UE–EUA (ver a <a href="https://docs.github.com/pt/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">política de privacidade da GitHub</a>).</li>
<li>Os tipos de letra do site estão guardados no próprio site, por isso a tua visita não envia pedidos ao Google Fonts nem a serviços semelhantes.</li>
<li>Se usares o menu de acessibilidade (tamanho do texto, contraste e outras opções) ou fechares um aviso no topo do site, essa escolha fica guardada apenas no teu navegador, para a lembrar na visita seguinte. Não é enviada para lado nenhum.</li>
</ul>
{stats}<h2>Se me enviares um email</h2>
<p>Se usares o botão de email ou escreveres para o endereço indicado, uso o teu nome, o teu endereço de email e o conteúdo da mensagem apenas para te responder. As mensagens passam pelo serviço de email que aloja este endereço, que as trata segundo a sua própria política de privacidade.</p>
<p>Uma mensagem dirigida a uma pessoa com atividade política pode revelar opiniões políticas, que são dados de categoria especial (artigo 9.º do RGPD). Se a tua mensagem os incluir, o seu tratamento baseia-se no consentimento que dás ao enviá-la, e podes retirá-lo a qualquer momento, pedindo-me para apagar a conversa. Não divulgo as mensagens a terceiros, salvo obrigação legal. Guardo-as pelo tempo necessário para tratar do assunto e apago-as quando deixarem de ser precisas.</p>
<h2>Ligações para outros sites</h2>
<p>O site tem ligações para as redes sociais (Instagram, Facebook, X e LinkedIn), para o Linktree e para os jornais onde publiquei artigos. Quando clicas numa ligação, passas a estar sujeito à política de privacidade desse serviço, que não controlo.</p>
<h2>Os teus direitos</h2>
<p>Tens o direito de pedir acesso aos teus dados pessoais, a sua retificação ou apagamento, a limitação ou oposição ao tratamento e a portabilidade, nos termos do Regulamento Geral sobre a Proteção de Dados (RGPD). Para exercer qualquer um destes direitos, escreve para <a href="mailto:{EMAIL}">{EMAIL}</a>. Tens ainda o direito de apresentar reclamação à Comissão Nacional de Proteção de Dados (CNPD), em <a href="https://www.cnpd.pt" target="_blank" rel="noopener">www.cnpd.pt</a>.</p>
<h2>Alterações</h2>
<p>Se esta política mudar, a data no topo da página é atualizada.</p>
"""
acc=f"""<p>Quero que este site possa ser usado por todas as pessoas. A referência que sigo são as Diretrizes de Acessibilidade para o Conteúdo Web (WCAG) 2.1, nível AA.</p>
<h2>Estado de conformidade</h2>
<p>Esta declaração é voluntária. O site não foi sujeito a uma auditoria de acessibilidade independente. Foi verificado com ferramentas automáticas, como o AccessMonitor, e os problemas encontrados foram corrigidos. Por isso, não declaro conformidade total com as WCAG 2.1, só o objetivo de as cumprir.</p>
<h2>O que o site já tem</h2>
<ul>
<li>Uma ligação “Saltar para o conteúdo principal”, que aparece quando se navega com o teclado.</li>
<li>Títulos organizados por níveis, em sequência, para facilitar a navegação com leitores de ecrã.</li>
<li>Texto alternativo nas imagens, e os ícones decorativos marcados para os leitores de ecrã os ignorarem.</li>
<li>Navegação por teclado, com indicação visível do elemento selecionado.</li>
<li>Um menu de acessibilidade, no canto inferior esquerdo, para aumentar e diminuir o texto, usar escala de cinza, aumentar o contraste, inverter as cores, usar fundo claro, sublinhar as ligações e mudar para uma letra mais legível. As escolhas ficam guardadas no teu navegador.</li>
<li>Um desenho que se adapta ao telemóvel, ao tablet e ao computador, e que suporta ampliação.</li>
<li>O idioma da página indicado (português de Portugal).</li>
</ul>
<h2>Limitações conhecidas</h2>
<ul>
<li>As tabelas de resultados eleitorais da página de biografia deslizam na horizontal em ecrãs pequenos.</li>
<li>As descrições das fotografias são curtas e descrevem a cena de forma geral.</li>
<li>As ligações para sites de terceiros (jornais, redes sociais, Linktree) levam a páginas cuja acessibilidade não controlo.</li>
</ul>
<h2>Encontraste um problema?</h2>
<p>Se alguma parte do site te for difícil de usar, ou se precisares do conteúdo noutro formato, escreve para <a href="mailto:{EMAIL}">{EMAIL}</a>. Respondo e, sempre que possível, corrijo.</p>
"""
open('_site/privacidade.html','w',encoding='utf-8').write(legal_page('/privacidade','Política de privacidade','Que dados pessoais este site trata e porquê: sem cookies, sem publicidade e com estatísticas que respeitam a privacidade.',priv))
open('_site/acessibilidade.html','w',encoding='utf-8').write(legal_page('/acessibilidade','Declaração de acessibilidade','O que este site faz para ser acessível, as limitações conhecidas e como reportar problemas.',acc))
# ---------- home: fonts self-hosted, JSON-LD, extras ----------
home=open(src,encoding='utf-8').read()
home=re.sub(r'<link rel="preconnect" href="https://fonts.googleapis.com">\n','',home)
home=home.replace('<link rel="icon"','<link rel="canonical" href="https://henriquelonga.pt/">\n<link rel="icon"',1)
home=home.replace('<meta name="twitter:card" content="summary_large_image">','<meta name="twitter:card" content="summary_large_image">\n'+SOCIAL_META,1)
home=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com/css2[^>]*>\n','',home)
home=re.sub(r'(<style>)(.*?)(</style>)',lambda m:m.group(1)+'\n'+FONTFACE+m.group(2).lstrip('\n').replace('Archivo,','Archivo,"Archivo Fallback",')+NOTICE_CSS+m.group(3),home,count=1,flags=re.S)
home=home.replace('<div id="page">\n','<div id="page">\n'+NOTICE_HTML,1)
home=home.replace('</body>',NOTICE_JS+'</body>',1)
home_lis=''.join('<li><a href="/opiniao/%s"><span class="t">%s</span><span class="s">%s</span></a></li>'%(k,arts[k]['title'],OUT[k]) for k in ORDER[:3])
home=re.sub(r'<ul class="articles">.*?</ul>',lambda m:'<ul class="articles">'+home_lis+'</ul>',home,count=1,flags=re.S)
home_ld={"@context":"https://schema.org","@graph":[PERSON,WEBSITE]}
home=home.replace('</head>',extra_head(home_ld)+'</head>',1)
open('_site/index.html','w',encoding='utf-8').write(home)

# ---------- press page ----------
BIO50='Henrique Longa, natural de Sesimbra, é estudante de Química Aplicada na NOVA FCT e ativista cívico. Integra o Grupo de Coordenação Local do LIVRE em Setúbal e foi cabeça-de-lista do partido à Assembleia Municipal de Sesimbra em 2025. Tem percurso no Escutismo e na Greve Climática Estudantil.'
BIO100='Henrique José Longa Correia, natural de Sesimbra, é estudante de Química Aplicada na Faculdade de Ciências e Tecnologia da Universidade NOVA de Lisboa, com investigação em Síntese Orgânica. Tem cerca de doze anos de Escutismo, integrou a Greve Climática Estudantil e o Fridays for Future e é coautor do Teenager Climate Guide. É Vice-Presidente para as Operações da Associação Nacional de Estudantes de Química e colaborou com o Conselho Nacional da Juventude. Membro do LIVRE desde 2024, integra o Grupo de Coordenação Local do Núcleo Territorial Distrital de Setúbal e foi cabeça-de-lista à Assembleia Municipal de Sesimbra em 2025.'
print('words',len(BIO50.split()),len(BIO100.split()))
MEDIA=[
 ('Declarações na manifestação pela habitação','Canal NOW, 27 de outubro de 2026 (Instagram)','https://www.instagram.com/p/DfCm8RLIo3c'),
 ('Autárquicas 2025: debate para a Assembleia Municipal de Sesimbra','Vídeo no YouTube, 30 de setembro de 2025','https://youtu.be/upJXiGhW1j8'),
 ('LIVRE avança com Carina Calisto à Câmara de Sesimbra e Henrique Longa para a Assembleia Municipal','O Setubalense, notícia, 31 de julho de 2025','https://osetubalense.com/local/sesimbra/livre-avanca-com-carina-calisto-a-camara-de-sesimbra-e-henrique-longa-para-a-assembleia-municipal'),
 ('Apresentação de Henrique Longa – Sesimbra | Primárias do LIVRE','Vídeo no YouTube','https://youtu.be/HQIG6Ry5ZEo'),
]
media_li=''.join('<li><a href="%s" target="_blank" rel="noopener"><span class="t">%s</span><span class="s">%s</span></a></li>\n'%(u,esc(t),esc(m)) for t,m,u in MEDIA)
op_li=''.join('<li><a href="/opiniao/%s"><span class="t">%s</span><span class="s">%s, %s</span></a></li>\n'%(k,arts[k]['title'],OUT[k],re.search(r'<time[^>]*>(.*?)</time>',arts[k]['meta']).group(1)) for k in ORDER[:3])
press_css="""
.press-sec{margin:2em 0 .5em;font:800 clamp(24px,3.4vw,30px)/1.2 Archivo,"Archivo Fallback","Helvetica Neue",Arial,sans-serif}
.press-text{max-width:36em;font-size:20px;line-height:1.7}
.press-text p{margin:0 0 1em}
.bio-short{margin:0 0 30px;max-width:36em}
.bio-short h3{margin:0 0 8px;font:800 18px/1.3 Archivo,"Archivo Fallback","Helvetica Neue",Arial,sans-serif}
.bio-short p{margin:0 0 12px;font-size:20px;line-height:1.7}
.copybtn{padding:9px 16px;border:2px solid var(--ink);border-radius:6px;background:transparent;color:var(--ink);font:700 15px Archivo,"Archivo Fallback",Arial,sans-serif;cursor:pointer}
@media(hover:hover){.copybtn:hover{background:var(--ink);color:var(--paper)}}
.press-btns{display:flex;flex-wrap:wrap;gap:12px;margin:14px 0 0}
.press-btns .btn{margin:0}
.article .articles{margin-top:6px}
"""
press_main=f"""<main class="article" id="conteudo" tabindex="-1">
<div class="wrap">
<h1>Imprensa</h1>
<h2 class="press-sec">Contacto</h2>
<div class="press-text"><p><a href="mailto:{EMAIL}">{EMAIL}</a></p></div>
<h2 class="press-sec">Fotografias</h2>
<div class="press-btns"><a class="btn" href="/galeria">Galeria de fotos</a></div>
<h2 class="press-sec">Biografias para copiar</h2>
<div class="bio-short"><h3>Versão de cerca de 50 palavras</h3><p id="bio50">{esc(BIO50)}</p><button type="button" class="copybtn" data-copy-target="bio50">Copiar</button></div>
<div class="bio-short"><h3>Versão de cerca de 100 palavras</h3><p id="bio100">{esc(BIO100)}</p><button type="button" class="copybtn" data-copy-target="bio100">Copiar</button></div>
<div class="press-btns"><a class="btn" href="/biografia">Biografia completa</a></div>
<h2 class="press-sec">Na comunicação social</h2>
<ul class="articles">
{media_li}</ul>
<h2 class="press-sec">Artigos de opinião</h2>
<ul class="articles">
{op_li}</ul>
<p class="rss"><a href="/opiniao/">Ver todos os artigos</a></p>
</div>
</main>"""
open('_site/imprensa.html','w',encoding='utf-8').write(head('/imprensa','Imprensa','Contacto de imprensa, biografias curtas para copiar, fotografias e aparições na comunicação social de Henrique Longa.',css+'\n'+article_css+press_css,'website')+body(header,press_main))
# ---------- robots, sitemap, rss ----------
open('_site/robots.txt','w',encoding='utf-8').write('User-agent: *\nAllow: /\n\nSitemap: '+SITE+'/sitemap.xml\n')
urls=['/','/biografia','/opiniao/']+['/opiniao/'+r[1] for r in rows]+['/imprensa','/galeria','/privacidade','/acessibilidade']
open('_site/sitemap.xml','w',encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join('<url><loc>%s%s</loc></url>\n'%(SITE,u if u!='/' else '/') for u in urls)+'</urlset>\n')
import datetime
def xesc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
items=''
for iso,slug,d,o,when,ex,sx in rows:
    _p=[int(x) for x in iso.split('-')]+[1]; dt=datetime.datetime(_p[0],_p[1],_p[2] if len(iso)>7 else 1,12,0,0)
    pub=dt.strftime('%a, %d %b %Y %H:%M:%S +0000')
    title=_h.unescape(re.sub('<[^>]+>','',d['title']))
    items+=f'<item>\n<title>{xesc(title)}</title>\n<link>{SITE}/opiniao/{slug}</link>\n<guid isPermaLink="true">{SITE}/opiniao/{slug}</guid>\n<pubDate>{pub}</pubDate>\n<dc:creator>Henrique Longa</dc:creator>\n<description>{xesc(ex)}</description>\n<content:encoded><![CDATA[{d["text"]}]]></content:encoded>\n</item>\n'
feed=f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom" xmlns:content="http://purl.org/rss/1.0/modules/content/" xmlns:dc="http://purl.org/dc/elements/1.1/">\n<channel>\n<title>Henrique Longa: artigos de opinião</title>\n<link>{SITE}/opiniao/</link>\n<atom:link href="{SITE}/feed.xml" rel="self" type="application/rss+xml"/>\n<description>Artigos de opinião de Henrique Longa sobre Sesimbra, habitação, regionalização, juventude e democracia.</description>\n<language>pt-PT</language>\n'+items+'</channel>\n</rss>\n'
open('_site/feed.xml','w',encoding='utf-8').write(feed)

for _f in glob.glob('_site/**/*.html',recursive=True):
    _t=open(_f,encoding='utf-8').read(); _n=_t.replace('href="/opiniao"','href="/opiniao/"')
    if _n!=_t: open(_f,'w',encoding='utf-8').write(_n)
print('Site gerado em _site/ com',sum(len(f) for _,_,f in os.walk('_site')),'ficheiros e',len(arts),'artigos.')
