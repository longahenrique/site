import re, os, shutil, zipfile, glob, json
H=os.getcwd()   # corre sempre a partir da raiz do repositório
src='gerador/home.html'
GOATCOUNTER='henriquelonga'   # codigo da conta GoatCounter; None = sem estatisticas
GSC_META=None      # valor do meta google-site-verification; None = nao usado
SITE='https://henriquelonga.pt'
# ---- aviso no topo (None = sem aviso) ----
MOTION_CSS='\n@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto!important}*,*::before,*::after{transition:none!important;animation:none!important}}\n'
NOTICE_ID='alerta-charles-2026-11'
NOTICE_UNTIL='2026-11-11T23:59:59+00:00'   # Lisboa em novembro = UTC+0
NOTICE_ON=False   # True liga o aviso no topo; False desliga-o
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
s,_n=re.subn(r'(\.contact\{display:flex[^}]*?)padding:\d+px 0 20px',r'\1padding:76px 0 20px',s); assert _n==1
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
def NAVFIX(s):
    if 'aria-label="Principal"' in s: return s
    def _navlist(m):
        links=re.findall(r'<a\b.*?</a>',m.group(2),flags=re.S)
        return m.group(1).replace('<nav>','<nav aria-label="Principal">')+'<ul>'+''.join('<li>%s</li>'%l for l in links)+'</ul>'+m.group(3)
    s,_n=re.subn(r'(<nav>\s*<a class="brand"[^>]*>[^<]*</a>\s*)<div>(.*?)</div>(\s*</nav>)',_navlist,s,count=1,flags=re.S); assert _n==1
    s=s.replace('nav>div{','nav>ul{').replace('nav a{text-decoration:none;','nav ul{display:flex;align-items:baseline;list-style:none;margin:0;padding:0}\nnav li{margin:0;padding:0}\nnav a{text-decoration:none;',1)
    return s
s=NAVFIX(s)
# ---------- 2. reusable pieces ----------
css=re.search(r'<style>(.*?)</style>',s,flags=re.S).group(1).strip()
header=re.search(r'<header class="top sea">.*?</header>',s,flags=re.S).group(0)
art_header=header.replace('<a href="/opiniao/">','<a href="/opiniao/" aria-current="true">')
gal_header=header.replace('<a href="/biografia">','<a href="/biografia" aria-current="true">')
pass
contact=re.search(r'<div class="sea" id="contacto">.*?</footer>\n</div>\n</div>',s,flags=re.S).group(0)
a11y=re.search(r'<div class="a11y">.*?</div>\n</div>\n',s,flags=re.S).group(0)
fav='<link rel="icon" href="/favicon.ico" sizes="any">\n<link rel="icon" type="image/png" sizes="48x48" href="/icon-48.png">\n<link rel="icon" type="image/png" sizes="192x192" href="/icon-192.png">\n<link rel="apple-touch-icon" href="/apple-touch-icon.png">'
js=re.findall(r'<script>(.*?)</script>',s,flags=re.S)[-1].strip()
img=re.search(r'<img src="(data:image/webp;base64,[^"]+)" width="(\d+)" height="(\d+)" alt="([^"]*)">',s)
article_css='''
.gl{margin:0}
.gl dt{margin:1.4em 0 0;font-weight:800}
.gl dd{margin:.3em 0 0;max-width:36em}
abbr[title]{text-decoration:none}
.article{background:var(--paper);padding:56px 0 80px}
.article .wrap :last-child{margin-bottom:0}
.article:has(.more-articles){padding-bottom:58px}
.article .nf-more{margin-top:76px}
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
:where(html:not(.sem-rato)) .share a:hover,:where(html:not(.sem-rato)) .share button:hover{background:var(--ink);color:var(--paper)}
.more-articles .articles{max-width:44em}
.rss{margin:28px 0 0;font:600 16px Archivo,"Helvetica Neue",Arial,sans-serif}
.rss a{text-underline-offset:5px}
@media(max-width:600px){.article{padding:36px 0 52px}.article:has(.more-articles){padding-bottom:36px}.article .nf-more{margin-top:56px}.article .text p{font-size:19px}}
'''
bio_css='''
#bio h1{font-size:clamp(36px,6vw,60px);line-height:1.05;margin:0 0 28px;text-wrap:balance}
#bio .portrait{flex-direction:column;align-items:center;align-self:start;padding:28px 0 34px}
#bio .btn-in,#bio .btn-out{display:flex;flex-wrap:wrap;gap:12px}
#bio .btn-in{justify-content:center;margin:-10px 0 0;padding:0 16px}
#bio .btn-in .btn,#bio .btn-out .btn{margin:0}
@media(min-width:1000px){#bio .who{grid-template-rows:auto auto 1fr}#bio .who .prose{grid-row:2 / span 2}#bio .who .btn-out{grid-column:2;grid-row:3;align-self:start;margin:22px 0 0}#bio .portrait{padding-bottom:0}#bio .btn-in{display:none}}
@media(max-width:999px){#bio .btn-out{display:none}}
.results h2{margin-bottom:6px;font-size:clamp(24px,3.4vw,30px);line-height:1.2}
.results{padding-bottom:10px}
.results .res-dl+h3{margin-top:64px}
.results h3{margin:36px 0 12px;font:800 21px/1.2 Archivo,"Helvetica Neue",Arial,sans-serif}
.res-dl{display:grid;grid-template-rows:auto auto;grid-auto-flow:column;grid-template-columns:10% 13.5% 20% 16% 8.5% 12% 9.5% 10.5%;margin:0 0 10px;padding:0;font:500 17px/1.35 Archivo,"Helvetica Neue",Arial,sans-serif}
.res-dl dt{margin:0;padding:0 10px 12px 0;border-bottom:2px solid var(--ink);font-weight:800;white-space:nowrap}
.res-dl dd{white-space:nowrap}
.res-dl dt.ab .sr{position:absolute;width:1px;height:1px;margin:-1px;padding:0;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.res-dl dt.ab::before{content:attr(data-short);content:attr(data-short) / ""}
.res-dl dd{margin:0;padding:13px 10px 0 0}
@media(max-width:980px){.res-dl dt.ab .sr{position:static;width:auto;height:auto;margin:0;overflow:visible;clip:auto}.res-dl dt.ab::before{content:none}.res-dl dt,.res-dl dd{white-space:normal}.res-dl{grid-template-rows:none;grid-auto-flow:row;grid-template-columns:minmax(0,1fr) 9em;column-gap:0}.res-dl dt,.res-dl dd{padding:11px 0;border:0;border-top:2px solid rgba(20,20,20,.3)}.res-dl dt:first-of-type,.res-dl dt:first-of-type+dd{border-top-color:var(--ink)}.res-dl dt{font-weight:500;font-size:16px;text-align:left;padding-right:18px}.res-dl dd{text-align:right;font-weight:800}}
@media(max-width:600px){#bio h1{margin-bottom:18px}.results h3{font-size:21px}}
'''
SOCIAL_META='<meta property="og:site_name" content="Henrique Longa">\n<meta name="twitter:site" content="@henriquelonga">\n<meta name="twitter:creator" content="@henriquelonga">'
PROFILE_META='<meta property="profile:first_name" content="Henrique">\n<meta property="profile:last_name" content="Longa">'
FONTFACE='''@font-face{font-family:Archivo;font-style:normal;font-weight:500;font-display:swap;src:url(/fonts/archivo-latin-500-normal.woff2) format("woff2")}
@font-face{font-family:Archivo;font-style:normal;font-weight:800;font-display:swap;src:url(/fonts/archivo-latin-800-normal.woff2) format("woff2")}
@font-face{font-family:"Archivo Fallback";font-weight:500;src:local("Arial"),local("ArialMT"),local("Helvetica Neue"),local("Helvetica"),local("Liberation Sans");size-adjust:100.3%;ascent-override:87.5%;descent-override:20.9%;line-gap-override:0%}
@font-face{font-family:"Archivo Fallback";font-weight:800;src:local("Arial Bold"),local("Arial-BoldMT"),local("Helvetica Neue Bold"),local("Helvetica Bold"),local("Liberation Sans Bold");size-adjust:103.6%;ascent-override:84.8%;descent-override:20.3%;line-gap-override:0%}
@font-face{font-family:"Source Serif Fallback";font-weight:400;src:local("Times New Roman"),local("TimesNewRomanPSMT"),local("Liberation Serif"),local("Times");size-adjust:117%;ascent-override:88.6%;descent-override:28.6%;line-gap-override:0%}
@font-face{font-family:"Source Serif Fallback";font-weight:600;src:local("Times New Roman Bold"),local("TimesNewRomanPS-BoldMT"),local("Liberation Serif Bold"),local("Times-Bold");size-adjust:111.5%;ascent-override:92.9%;descent-override:30%;line-gap-override:0%}
@font-face{font-family:"Source Serif Fallback";font-style:italic;font-weight:400;src:local("Times New Roman Italic"),local("TimesNewRomanPS-ItalicMT"),local("Liberation Serif Italic"),local("Times-Italic");size-adjust:106.4%;ascent-override:97.4%;descent-override:31.5%;line-gap-override:0%}
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:400;font-display:swap;src:url(/fonts/source-serif-4-latin-400-normal.woff2) format("woff2")}
@font-face{font-family:"Source Serif 4";font-style:normal;font-weight:600;font-display:swap;src:url(/fonts/source-serif-4-latin-600-normal.woff2) format("woff2")}
@font-face{font-family:"Source Serif 4";font-style:italic;font-weight:400;font-display:swap;src:url(/fonts/source-serif-4-latin-400-italic.woff2) format("woff2")}
'''
import json
def FX(c): return c.replace('Archivo,','Archivo,"Archivo Fallback",').replace('"Source Serif 4",Georgia','"Source Serif 4","Source Serif Fallback",Georgia')
def extra_head(ld=None):
    out='<link rel="preload" href="/fonts/archivo-latin-500-normal.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="/fonts/archivo-latin-800-normal.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="/fonts/source-serif-4-latin-400-normal.woff2" as="font" type="font/woff2" crossorigin>\n<link rel="preload" href="/fonts/source-serif-4-latin-600-normal.woff2" as="font" type="font/woff2" crossorigin>\n'+'<link rel="alternate" type="application/rss+xml" title="Henrique Longa: artigos de opinião" href="/feed.xml">\n'
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
{FONTFACE}{FX(css_text)}{NOTICE_CSS}{MOTION_CSS}
</style>
</head>
'''
UX_JS=r"""<script>
(function(){var d=document.documentElement;function pt(e){if(e.pointerType==="mouse"||e.pointerType==="pen")d.classList.remove("sem-rato");else if(e.pointerType==="touch")d.classList.add("sem-rato")}addEventListener("pointerdown",pt,{passive:true});addEventListener("pointermove",pt,{passive:true})})();
(function(){
var c=navigator.connection;if(c&&(c.saveData||/2g/.test(c.effectiveType||"")))c=null;else c=1;
var done={};
function pf(e){if(!c)return;var a=e.target.closest&&e.target.closest("a[href]");if(!a||a.target==="_blank"||a.hasAttribute("download"))return;
if(a.origin!==location.origin||a.pathname===location.pathname||/^\/(feed|sitemap|robots)/.test(a.pathname)||/\.(jpe?g|png|webp|pdf|xml|txt)$/i.test(a.pathname))return;
if(done[a.pathname])return;done[a.pathname]=1;var l=document.createElement("link");l.rel="prefetch";l.href=a.pathname;document.head.appendChild(l)}
document.addEventListener("mouseover",pf,{passive:true});document.addEventListener("touchstart",pf,{passive:true});
})();
</script>
"""
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
{extra}{UX_JS}{NOTICE_JS}</body>
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
    arts[slug]=dict(titulo_img=meta.get('titulo-imagem',''),title=esc(meta['titulo']),desc=esc(desc).replace('"','&quot;'),meta=esc(meta['linha']).replace('{data}',time),text=''.join('<p>%s</p>\n'%inline(p) for p in paras),after=after,meio=meta['meio'])
if not arts: raise SystemExit('ERRO: não há artigos na pasta artigos/')
PERSON={"@type":"Person","@id":SITE+"/#pessoa","name":"Henrique Longa","alternateName":"Henrique José Longa Correia","url":SITE+"/","image":SITE+"/fotos/henrique-longa-retrato.jpg","description":"Estudante de Química Aplicada na NOVA FCT e ativista cívico, membro do LIVRE em Sesimbra.","jobTitle":"Estudante e ativista cívico","affiliation":[{"@type":"Organization","name":"LIVRE"},{"@type":"Organization","name":"Faculdade de Ciências e Tecnologia da Universidade NOVA de Lisboa"},{"@type":"Organization","name":"Associação Nacional de Estudantes de Química"}],"sameAs":["https://www.instagram.com/henriquelonga","https://www.facebook.com/henriquelongacorreia","https://x.com/henriquelonga","https://www.linkedin.com/in/henriquelonga"]}
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
def og_image(slug,title,line,kicker='Artigo de opinião'):
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
    else:   # não cabe nem no tamanho mínimo: encurta com "…" para não sair da imagem
        f=ImageFont.truetype(_FD+'InterDisplay-ExtraBold.otf',36); size=36; words=title.split()
        while len(words)>1:
            ls=wrap(' '.join(words)+'…',f)
            if len(ls)*size*1.13<=330 and max(f.getlength(x) for x in ls)<=colw: break
            words.pop()
    d.text((70,60),kicker,font=ImageFont.truetype(_FD+'Inter-SemiBold.otf',30),fill=INK)
    y=125
    for x in ls: d.text((70,y),x,font=f,fill=INK); y+=int(size*1.13)
    d.text((70,H-118),line,font=ImageFont.truetype(_FD+'Inter-SemiBold.otf',30),fill=INK)
    d.text((70,H-72),'henriquelonga.pt',font=ImageFont.truetype(_FD+'Inter-Medium.otf',28),fill=INK)
    im.save('_site/og/%s.jpg'%slug,quality=88,optimize=True)
for slug,d in arts.items():
    url=SITE+'/opiniao/'+slug; tt=_h.unescape(re.sub('<[^>]+>','',d['title']))
    _when=re.search(r'<time[^>]*>(.*?)</time>',d['meta']).group(1)
    og_image(slug,(arts[slug].get('titulo_img') or tt),OUT[slug]+', '+_when)
    ogimg=SITE+'/og/'+slug+'.jpg'
    wa_text=tt+'\n\n'+url   # título, linha em branco, endereço
    share=f'''<div class="share">
<h2>Partilhar</h2>
<ul>
<li><button type="button" data-copy>Copiar ligação</button></li>
<li><a href="https://wa.me/?text={enc(wa_text)}" target="_blank" rel="noopener">WhatsApp</a></li>
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
    bc={"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Início","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Opinião","item":SITE+"/opiniao/"},{"@type":"ListItem","position":3,"name":re.sub('<[^>]+>','',d['title'])}]}
    ld=[ld,bc]
    open(f'_site/opiniao/{slug}.html','w',encoding='utf-8').write(head(f'/opiniao/{slug}',d['title'],d['desc'],css+'\n'+article_css,'article',ld,f'<meta property="article:published_time" content="{iso}">\n<meta property="article:author" content="{SITE}/biografia">\n<meta property="article:section" content="Opinião">\n<meta property="og:image:alt" content="{esc(tt)}, artigo de opinião de Henrique Longa">\n',ogimg)+body(art_header,main))
# ---------- entrevista (O Sesimbrense, edição em papel) ----------
ENT_TITLE='Henrique Longa: LIVRE quer “Sesimbra de 15 minutos” e “Plano de ação climática”'
ENT_LINE='O Sesimbrense, 31 de agosto de 2025'
def _inl2(t): return re.sub(r'\*([^*\n]+)\*',r'<em>\1</em>',re.sub(r'\*\*([^*\n]+)\*\*',r'<strong>\1</strong>',esc(t)))
_ent=[x.strip().replace('\n',' ') for x in re.split(r'\n\s*\n',open('gerador/entrevista.md',encoding='utf-8').read().strip()) if x.strip()]
ent_text=''.join('<p>%s</p>\n'%_inl2(x) for x in _ent)
ENT_SLUG='livre-quer-sesimbra-de-15-minutos-e-plano-de-acao-climatica'
ent_url=SITE+'/entrevista/'+ENT_SLUG
os.makedirs('_site/entrevista',exist_ok=True)
og_image('entrevista-'+ENT_SLUG,ENT_TITLE,ENT_LINE,'Entrevista')
ent_share=f'''<div class="share">
<h2>Partilhar</h2>
<ul>
<li><button type="button" data-copy>Copiar ligação</button></li>
<li><a href="https://wa.me/?text={enc(ENT_TITLE+chr(10)+chr(10)+ent_url)}" target="_blank" rel="noopener">WhatsApp</a></li>
<li><a href="https://x.com/intent/post?url={enc(ent_url)}&amp;text={enc(ENT_TITLE)}" target="_blank" rel="noopener">X</a></li>
<li><a href="https://www.facebook.com/sharer/sharer.php?u={enc(ent_url)}" target="_blank" rel="noopener">Facebook</a></li>
<li><a href="https://www.linkedin.com/sharing/share-offsite/?url={enc(ent_url)}" target="_blank" rel="noopener">LinkedIn</a></li>
<li><a href="mailto:?subject={enc(ENT_TITLE)}&amp;body={enc(ent_url)}">Email</a></li>
</ul>
</div>
'''
ent_main=f'''<main class="article" id="conteudo" tabindex="-1">
<div class="wrap">
<p class="crumb"><a href="/imprensa">← Imprensa</a></p>
<h1>{esc(ENT_TITLE)}</h1>
<p class="meta">Entrevista a <em>O Sesimbrense</em>, <time datetime="2025-08-31">31 de agosto de 2025</time>. Texto de João Pinhal.</p>
<div class="text">
{ent_text}</div>
<div class="after">
<a href="/imprensa">Imprensa</a>
<a href="/opiniao">Artigos de opinião</a>
</div>
{ent_share}</div>
</main>'''
ent_desc='Entrevista de Henrique Longa a O Sesimbrense, publicada em papel a 31 de agosto de 2025, sobre a Sesimbra de 15 minutos, o plano de ação climática, a habitação e a cultura.'
ent_ld=[{"@context":"https://schema.org","@type":"NewsArticle","headline":ENT_TITLE,"description":ent_desc,"inLanguage":"pt-PT","datePublished":"2025-08-31","url":ent_url,"mainEntityOfPage":ent_url,"image":SITE+'/og/entrevista-'+ENT_SLUG+'.jpg',"author":{"@type":"Person","name":"João Pinhal"},"about":{"@id":SITE+"/#pessoa"},"publisher":{"@type":"Organization","name":"O Sesimbrense"}},
 {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Início","item":SITE+"/"},{"@type":"ListItem","position":2,"name":"Imprensa","item":SITE+"/imprensa"},{"@type":"ListItem","position":3,"name":ENT_TITLE}]}]
open('_site/entrevista/%s.html'%ENT_SLUG,'w',encoding='utf-8').write(head('/entrevista/'+ENT_SLUG,esc(ENT_TITLE),ent_desc,css+'\n'+article_css,'article',ent_ld,'<meta property="article:published_time" content="2025-08-31">\n<meta property="og:image:alt" content="Entrevista de Henrique Longa a O Sesimbrense, 31 de agosto de 2025">\n',SITE+'/og/entrevista-'+ENT_SLUG+'.jpg')+body(header,ent_main))
# biography page
bio_paras=['Henrique José Longa Correia, nascido a 1 de abril de 2005 em Lisboa e natural de Sesimbra, é um estudante e ativista cívico associado ao partido LIVRE.',
'Henrique Longa é aluno na Faculdade de Ciências e Tecnologia da Universidade NOVA de Lisboa, onde realiza a Licenciatura em Química Aplicada. No seu percurso académico, focou a sua investigação no âmbito da Síntese Orgânica.',
'O seu percurso é fortemente marcado pelo associativismo e pelo envolvimento cívico, a começar por um percurso de cerca de doze anos no Escutismo. Integrou a Greve Climática Estudantil e o movimento internacional <span lang="en">Fridays for Future</span>, participando ativamente na organização de greves pelo clima e ações de sensibilização. Desta interseção entre sustentabilidade, juventude e bem-estar resultou a coautoria do <em><span lang="en">Teenager Climate Guide</span>: Promover a comunicação e a saúde mental no contexto da crise climática</em>, um manual pioneiro publicado pela Ecopsi e Greve Climática Estudantil para apoiar jovens ativistas na comunicação e na preservação da saúde mental.',
'Paralelamente, assumiu responsabilidades associativas como dirigente na Associação Nacional de Estudantes de Química, exercendo atualmente funções de Vice-Presidente para as Operações, colaborou com o Conselho Nacional de Juventude e integrou a comissão pedagógica do seu curso e a estrutura da Associação de Estudantes da NOVA FCT.',
'Na política partidária, entrou para o Partido LIVRE em janeiro de 2024. Integra, desde agosto de 2024, o Grupo de Coordenação Local do Núcleo Territorial Distrital de Setúbal. Nas Eleições Legislativas de 2025 integrou a lista do partido pelo círculo eleitoral de Setúbal, e no mesmo ano assumiu o papel de cabeça-de-lista à Assembleia Municipal de Sesimbra nas Eleições Autárquicas, sendo um dos candidatos mais jovens.']
def table(tid,cols,rows):
    FULL={'Cl.':'Classificação do partido','%':'Percentagem de votos'}
    def dt(c):
        t=re.sub('<[^>]+>','',c[0])
        if t in FULL: return '<dt class="ab" data-short="%s"><span class="sr">%s</span></dt>'%(t,FULL[t])
        return '<dt>%s</dt>'%t
    return ''.join('<dl class="res-dl">'+''.join('%s<dd>%s</dd>'%(dt(cols[k]),v) for k,v in enumerate(r))+'</dl>' for r in rows)
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
_bt=open('_site/biografia.html',encoding='utf-8').read()
_bt=_bt.replace('<div class="wrap who">\n<h1>Biografia</h1>','<div class="wrap"><p class="bio-back" id="bio-back" hidden><a href="/imprensa">← Imprensa</a></p></div>\n<div class="wrap who">\n<h1>Biografia</h1>',1)
assert 'id="bio-back"' in _bt
_bt=_bt.replace('</head>','<style>#bio{padding-top:56px}#bio h1{font-size:clamp(34px,6.2vw,66px);line-height:1.06;margin-bottom:18px}#bio .prose p{font-size:20px;line-height:1.75;margin:0 0 1.25em}@media(max-width:600px){#bio{padding-top:36px}}.bio-back{margin:0 0 30px;font:600 16px Archivo,"Helvetica Neue",Arial,sans-serif}.bio-back a{text-underline-offset:5px}</style>\n</head>',1)
_bt=_bt.replace('</body>','<script>(function(){var a=document.getElementById("bio-back");if(!a)return;try{var r=new URL(document.referrer);if(r.origin===location.origin&&r.pathname.replace(/\\/$/,"")==="/imprensa")a.hidden=false}catch(e){}})();</script>\n</body>',1)
open('_site/biografia.html','w',encoding='utf-8').write(_bt)

import unicodedata, html as _h
def norm(t): return ''.join(c for c in unicodedata.normalize('NFD',t.lower()) if unicodedata.category(c)!='Mn')
OUT={k:v['meio'] for k,v in arts.items()}
rows=[]
for slug,d in arts.items():
    iso=re.search(r'datetime="(\d{4}-\d{2}(?:-\d{2})?)"',d['meta']).group(1); when=re.search(r'<time[^>]*>(.*?)</time>',d['meta']).group(1)
    paras=[_h.unescape(re.sub('<[^>]+>','',x)) for x in re.findall(r'<p>(.*?)</p>',d['text'],flags=re.S)]
    ex=paras[0]
    if len(ex)>200:
        ex=ex[:200].rsplit(' ',1)[0]
        while ' ' in ex and len(re.sub(r'\W','',ex.rsplit(' ',1)[1]))<=3: ex=ex.rsplit(' ',1)[0]
        ex=ex.rstrip(' ,;:.')+'…'
    rows.append((iso,slug,d,OUT[slug],when,ex,' '.join(paras)))
rows.sort(reverse=True)
q=lambda t:esc(t).replace('"','&quot;')
lis=''.join(f'<li data-y="{iso[:4]}" data-o="{q(o)}" data-t="{q(sx)}"><a href="/opiniao/{slug}"><span class="t">{d["title"]}</span><span class="s">{esc(o)}, {when}</span><span class="x">{esc(ex)}</span></a></li>\n' for iso,slug,d,o,when,ex,sx in rows)
years=sorted({r[0][:4] for r in rows},reverse=True); outs=sorted({r[3] for r in rows})
opts=lambda L:''.join(f'<option value="{esc(v)}">{esc(v)}</option>' for v in L)
list_css=r"""
.articles .x{display:block;margin-top:10px;font-size:17px;line-height:1.6;text-wrap:pretty}
.articles li[hidden]{display:none}
.articles mark{background:rgba(180,202,173,.55);color:var(--ink);font-weight:600;-webkit-text-stroke:.35px currentColor;paint-order:stroke fill;padding:0 .12em;margin:0 -.04em;border-radius:3px}
.ctl{display:flex;flex-wrap:wrap;gap:16px;margin:0 0 20px;max-width:44em}
.ctl .f{display:flex;flex-direction:column;gap:6px;font:600 15px Archivo,"Helvetica Neue",Arial,sans-serif}
.ctl .grow{flex:1 1 280px}
.ctl input,.ctl select{min-width:0;padding:12px 14px;font:500 17px Archivo,"Helvetica Neue",Arial,sans-serif;color:var(--ink);background:var(--paper);border:2px solid var(--ink);border-radius:6px}
.ctl input:focus-visible,.ctl select:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
input[type=search]::-webkit-search-cancel-button{-webkit-appearance:none;appearance:none;width:20px;height:20px;cursor:pointer;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath d='M4 4l12 12M16 4L4 16' stroke='%234a6a45' stroke-width='2.6' stroke-linecap='round'/%3E%3C/svg%3E") center/contain no-repeat}
.count{margin:0 0 8px;font:600 16px Archivo,"Helvetica Neue",Arial,sans-serif;color:var(--muted)}
#none{margin:24px 0;font-size:19px}
"""
list_main=f"""<main class="article" id="conteudo" tabindex="-1">
<div class="wrap">
<h1>Artigos de opinião</h1>
<div class="ctl" role="search" aria-label="Pesquisar artigos">
<label class="f grow"><span>Pesquisar</span><input type="search" id="q" placeholder="Palavra ou título" autocomplete="off"></label>
<label class="f"><span>Ano</span><select id="y"><option value="">Todos</option>{opts(years)}</select></label>
<label class="f"><span>Publicação</span><select id="o"><option value="">Todas</option>{opts(outs)}</select></label>
</div>
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
function nc(s){var r="";for(var i=0;i<s.length;i++){var c=s.charAt(i),d=c.normalize("NFD").replace(/[̀-ͯ]/g,"");r+=(d?d.charAt(0):c).toLowerCase().charAt(0)}return r}
function esc(s){return s.replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
function w1(a,b){var la=a.length,lb=b.length;if(Math.abs(la-lb)>1)return false;var i=0;while(i<la&&i<lb&&a.charAt(i)===b.charAt(i))i++;if(i===la&&i===lb)return true;if(la===lb)return a.slice(i+1)===b.slice(i+1)||(a.charAt(i)===b.charAt(i+1)&&a.charAt(i+1)===b.charAt(i)&&a.slice(i+2)===b.slice(i+2));if(la>lb)return a.slice(i+1)===b.slice(i);return a.slice(i)===b.slice(i+1)}
function exact(n,t){var r=[],i=n.indexOf(t);while(i>-1){r.push([i,i+t.length]);i=n.indexOf(t,i+t.length)}return r}
function fuzzy(n,toks){var r=[];for(var k=0;k<toks.length;k++){var tk=toks[k],hit=null;if(tk.length<4){var i=n.indexOf(tk);if(i>-1)hit=[i,i+tk.length]}else{var re=/[^\s.,;:!?()"“”«»…\-–—]+/g,m;while((m=re.exec(n))){var w=m[0];if(w1(tk,w)||w1(tk,w.slice(0,tk.length))){hit=[m.index,m.index+w.length];break}}}if(!hit)return null;r.push(hit)}return r.sort(function(a,b){return a[0]-b[0]})}
function mark(s,rs,a,b){var h="",p=a;rs.forEach(function(r){var x=Math.max(r[0],p),z=Math.min(r[1],b);if(z>x){h+=esc(s.slice(p,x))+"<mark>"+esc(s.slice(x,z))+"</mark>";p=z}});return h+esc(s.slice(p,b))}
function snip(s,rs){var f=rs[0][0],a=Math.max(0,f-70),b=Math.min(s.length,f+130);if(a>0){var u=s.indexOf(" ",a);if(u>-1&&u<f)a=u+1}if(b<s.length){var v=s.lastIndexOf(" ",b);if(v>f)b=v}return(a>0?"…":"")+mark(s,rs,a,b)+(b<s.length?"…":"")}
items.forEach(function(li){var t=li.querySelector(".t"),x=li.querySelector(".x");li._t=t;li._x=x;li._th=t.innerHTML;li._xh=x.innerHTML;li._h=t.textContent;li._b=li.getAttribute("data-t");li._nh=nc(li._h);li._nb=nc(li._b)})
function sh(li,rt,rb){li._t.innerHTML=rt.length?mark(li._h,rt,0,li._h.length):li._th;li._x.innerHTML=rb.length?snip(li._b,rb):li._xh}
function sync(){var p=new URLSearchParams();if(q.value.trim())p.set("q",q.value.trim());if(y.value)p.set("ano",y.value);if(o.value)p.set("publicacao",o.value);var s=p.toString(),path=location.pathname.replace(/\/$/,"");history.replaceState(null,"",path+(s?"?"+s:"")+location.hash)}
function run(){var s=nc(q.value.trim()),k=0,fz=false,pool=items.filter(function(li){return(!y.value||li.getAttribute("data-y")===y.value)&&(!o.value||li.getAttribute("data-o")===o.value)}),res=new Map();
if(s){pool.forEach(function(li){var rt=exact(li._nh,s),rb=exact(li._nb,s);if(rt.length||rb.length)res.set(li,[rt,rb])});
if(!res.size){var tk=s.split(/\s+/).filter(Boolean);pool.forEach(function(li){var rt=fuzzy(li._nh,tk),rb=fuzzy(li._nb,tk);if(rt||rb)res.set(li,[rt||[],rb||[]])});fz=res.size>0}}
items.forEach(function(li){var ok=pool.indexOf(li)>-1&&(!s||res.has(li));li.hidden=!ok;if(ok){k++;var r=res.get(li)||[[],[]];sh(li,r[0],r[1])}});
var ul=document.getElementById("list");function wl(n,r){return!/[a-z0-9]/.test(n.charAt(r[0]-1)||" ")&&!/[a-z0-9]/.test(n.charAt(r[1])||" ")}
function sc(li){var r=res.get(li);if(!r)return[0,0,0];var w=r[0].some(function(x){return wl(li._nh,x)})||r[1].some(function(x){return wl(li._nb,x)});return[w?1:0,r[0].length?1:0,r[0].length+r[1].length]}
var ord=items.slice();if(s)ord.sort(function(a,b){var x=sc(a),z=sc(b);for(var i=0;i<3;i++)if(x[i]!==z[i])return z[i]-x[i];return items.indexOf(a)-items.indexOf(b)});
ord.forEach(function(li){ul.appendChild(li)});
c.textContent=fz?"Sem resultados exatos. Resultados parecidos:":(k===1?"1 artigo":k+" artigos");n.hidden=k>0;sync()}
function setv(el,v){if(!v)return;for(var i=0;i<el.options.length;i++)if(el.options[i].value===v){el.value=v;return}}
var sp=new URLSearchParams(location.search);q.value=sp.get("q")||"";setv(y,sp.get("ano"));setv(o,sp.get("publicacao"));
[q,y,o].forEach(function(e){e.addEventListener("input",run);e.addEventListener("change",run)});
run();
})();
</script>
"""
list_header=header.replace('<a href="/opiniao/">','<a href="/opiniao/" aria-current="page">')
open('_site/opiniao/index.html','w',encoding='utf-8').write(head('/opiniao/','Artigos de opinião','Artigos de opinião de Henrique Longa sobre Sesimbra, habitação, regionalização, juventude e democracia.',css+'\n'+article_css+list_css,'website')+body(list_header,list_main,list_js))

# ---------- gallery ----------
from PIL import Image, ImageOps
GAL=json.load(open('gerador/galeria.json',encoding='utf-8'))
PHOTOS=[dict(file=g['ficheiro'],src='fotos-originais/'+g['original'],title=g['titulo'],desc=g.get('legenda'),alt=g['alt'],credit=g.get('credito')) for g in GAL]
os.makedirs('_site/fotos/miniaturas',exist_ok=True)
items=''
GAL_IMGS=[]
with zipfile.ZipFile('_site/fotos/henrique-longa-fotografias.zip','w',zipfile.ZIP_STORED) as zf:
    for ph in PHOTOS:
        shutil.copy(ph['src'],'_site/fotos/'+ph['file']); zf.write(ph['src'],ph['file'])
        im=Image.open(ph['src']); full=im.size; real=ImageOps.exif_transpose(im).size
        oi={"@type":"ImageObject","contentUrl":SITE+"/fotos/"+ph['file'],"thumbnailUrl":SITE+"/fotos/miniaturas/"+ph['file'],"name":ph['title'],"description":ph['alt'],"width":real[0],"height":real[1],"encodingFormat":"image/jpeg"}
        if ph['credit']: oi["creator"]={"@type":"Person","name":ph['credit']}; oi["creditText"]=ph['credit']
        GAL_IMGS.append(oi)
        t=ImageOps.exif_transpose(im).convert('RGB'); t.thumbnail((900,900)); t.save('_site/fotos/miniaturas/'+ph['file'],'JPEG',quality=84,optimize=True)
        _s=t.copy(); _s.thumbnail((480,480*3)); _s=_s.resize((480,round(480*t.height/t.width)),Image.LANCZOS) if t.width>480 else _s; _sn=ph['file'].rsplit('.',1)[0]+'-480.jpg'; _s.save('_site/fotos/miniaturas/'+_sn,'JPEG',quality=82,optimize=True)
        mb=('%.1f'%(os.path.getsize(ph['src'])/1e6)).replace('.',',')
        desc='<span class="gd">%s</span>'%esc(ph['desc']) if ph.get('desc') else ''
        cred='<span class="gc">Fotografia: %s</span>'%esc(ph['credit']) if ph['credit'] else ''
        items+=f'<li><figure><img src="/fotos/miniaturas/{ph["file"]}" srcset="/fotos/miniaturas/{_sn} 480w, /fotos/miniaturas/{ph["file"]} {t.width}w" sizes="(max-width:632px) calc(100vw - 32px), 464px" width="{t.width}" height="{t.height}" alt="{esc(ph["alt"])}" loading="lazy"><figcaption><span class="gt">{ph["title"]}</span>{desc}<span class="gm">JPG, {full[0]} × {full[1]} px, {mb} MB</span>{cred}<a class="dl" href="/fotos/{ph["file"]}" download aria-label="Descarregar: {esc(ph["title"])}">Descarregar</a></figcaption></figure></li>\n'
gal_css="""
.gal-all{margin:26px 0 8px}
.gal{list-style:none;margin:28px 0 0;padding:0;display:grid;grid-template-columns:repeat(auto-fill,minmax(min(300px,100%),1fr));gap:0 32px;align-items:start}
.gal li{margin:0 0 36px}
.gal figure{margin:0}
.gal img{display:block;width:100%;height:auto;border-radius:4px;background:var(--sea)}
.gal figcaption{display:flex;flex-direction:column;gap:3px;padding-top:12px;font:500 15px Archivo,"Helvetica Neue",Arial,sans-serif}
.gal .gt{font-weight:800;font-size:19px}
.gal .gd{font-size:16px}
.gal .gm,.gal .gc{color:var(--muted)}
.gal .dl{align-self:flex-start;margin-top:10px;padding:9px 16px;border:2px solid var(--ink);border-radius:6px;font-weight:800;text-decoration:none}
:where(html:not(.sem-rato)) .gal .dl:hover{background:var(--ink);color:var(--paper)}
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
gal_ld={"@context":"https://schema.org","@type":"ImageGallery","name":"Galeria de fotos de Henrique Longa","url":SITE+"/galeria","about":{"@id":SITE+"/#pessoa"},"image":GAL_IMGS}
gal_desc='Fotografias de Henrique Longa, ativista cívico em Sesimbra, para descarregar: '+', '.join(g['titulo'] for g in GAL)+'.'
open('_site/galeria.html','w',encoding='utf-8').write(head('/galeria','Galeria de fotos',gal_desc,css+'\n'+article_css+gal_css,'website',gal_ld)+body(gal_header,gal_main,GAL_BACK_JS))
# ---------- 404 (also turns /page/ into /page) ----------
nf_main="""<main class="article" id="conteudo" tabindex="-1">
<div class="wrap">
<h1>Página não encontrada</h1>
<p class="meta">O endereço que abriste não existe ou mudou.</p>
<div class="after">
<a href="/">Página inicial</a>
<a href="/opiniao">Artigos de opinião</a>
<a href="/biografia">Biografia</a>
<a href="/imprensa">Imprensa</a>
</div>
<div class="more-articles nf-more">
<h2>Últimos artigos</h2>
<ul class="articles">
"""+''.join('<li><a href="/opiniao/%s"><span class="t">%s</span><span class="s">%s</span></a></li>\n'%(k,arts[k]['title'],OUT[k]) for k in ORDER[:3])+"""</ul>
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
open('_site/ff36041429c8421a1bf64647f7ac8dbb.txt','w').write('ff36041429c8421a1bf64647f7ac8dbb')  # chave IndexNow (pública por desenho)

from PIL import Image, ImageDraw
def _circ(n):
    k=8; big=Image.new('RGBA',(n*k,n*k),(0,0,0,0)); ImageDraw.Draw(big).ellipse((0,0,n*k-1,n*k-1),fill=(180,202,173,255)); return big.resize((n,n),Image.LANCZOS)
for _n in (48,96,192): _circ(_n).save('_site/icon-%d.png'%_n)
_circ(256).save('_site/favicon.ico',sizes=[(16,16),(32,32),(48,48)])
Image.new('RGB',(180,180),(180,202,173)).save('_site/apple-touch-icon.png')
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
<li>Na página do programa (/programa), o mapa vai buscar as imagens do mapa ao OpenStreetMap, um serviço da Fundação OpenStreetMap, que recebe o teu endereço IP e dados técnicos do teu navegador. O mapa não cria cookies e não envia para lado nenhum o que escolhes ou pesquisas nele. Mais informação na <a href="https://wiki.osmfoundation.org/wiki/Privacy_Policy" target="_blank" rel="noopener">política de privacidade da Fundação OpenStreetMap</a>.</li>
<li>No computador, a página do programa tem a opção "Sugerir no mapa". O que desenhas e escreves fica só no teu navegador até clicares em "Enviar por email", que abre o teu programa de email com a sugestão escrita. O site não recebe nem guarda nada.</li>
<li>Se usares o menu de acessibilidade (tamanho do texto, contraste e outras opções) ou fechares um aviso no topo do site, essa escolha fica guardada apenas no teu navegador, para a lembrar na visita seguinte. Não é enviada para lado nenhum.</li>
</ul>
{stats}<h2>Se me enviares um email</h2>
<p>Se usares o botão de email ou escreveres para o endereço indicado, uso o teu nome, o teu endereço de email e o conteúdo da mensagem apenas para te responder. As mensagens passam pelo serviço de email que aloja este endereço, que as trata segundo a sua própria política de privacidade.</p>
<p>Uma mensagem dirigida a uma pessoa com atividade política pode revelar opiniões políticas, que são dados de categoria especial (artigo 9.º do RGPD). Se a tua mensagem os incluir, o seu tratamento baseia-se no consentimento que dás ao enviá-la, e podes retirá-lo a qualquer momento, pedindo-me para apagar a conversa. Não divulgo as mensagens a terceiros, salvo obrigação legal. Guardo-as pelo tempo necessário para tratar do assunto e apago-as quando deixarem de ser precisas.</p>
<h2>Ligações para outros sites</h2>
<p>O site tem ligações para as redes sociais (Instagram, Facebook, X e LinkedIn) e para os jornais onde publiquei artigos. Quando clicas numa ligação, passas a estar sujeito à política de privacidade desse serviço, que não controlo.</p>
<h2>Os teus direitos</h2>
<p>Tens o direito de pedir acesso aos teus dados pessoais, a sua retificação ou apagamento, a limitação ou oposição ao tratamento e a portabilidade, nos termos do Regulamento Geral sobre a Proteção de Dados (RGPD). Para exercer qualquer um destes direitos, escreve para <a href="mailto:{EMAIL}">{EMAIL}</a>. Tens ainda o direito de apresentar reclamação à Comissão Nacional de Proteção de Dados (CNPD), em <a href="https://www.cnpd.pt" target="_blank" rel="noopener">www.cnpd.pt</a>.</p>
<h2>Alterações</h2>
<p>Se esta política mudar, a data no topo da página é atualizada.</p>
"""
acc=f"""<p>Quero que este site possa ser usado por todas as pessoas. A referência que sigo são as Diretrizes de Acessibilidade para o Conteúdo Web (WCAG) 2.1, nível AA.</p>
<h2>Estado de conformidade</h2>
<p>Esta declaração é voluntária. O site não foi sujeito a uma auditoria de acessibilidade independente. Foi verificado com ferramentas automáticas, como o AccessMonitor, e com testes próprios em vários tamanhos de ecrã, e os problemas encontrados foram corrigidos. Por isso, não declaro conformidade total com as WCAG 2.1, só o objetivo de as cumprir.</p>
<h2>O que o site já tem</h2>
<ul>
<li>Uma ligação “Saltar para o conteúdo principal”, que aparece quando se navega com o teclado.</li>
<li>Títulos organizados por níveis, em sequência, para facilitar a navegação com leitores de ecrã.</li>
<li>Texto alternativo nas imagens, e os ícones decorativos marcados para os leitores de ecrã os ignorarem.</li>
<li>Navegação por teclado, com indicação visível do elemento selecionado.</li>
<li>Um menu de acessibilidade, no canto inferior esquerdo, para aumentar e diminuir o texto, usar escala de cinza, aumentar o contraste, inverter as cores, usar fundo claro, sublinhar as ligações e mudar para uma letra mais legível. As escolhas ficam guardadas no teu navegador.</li>
<li>Um desenho que se adapta ao telemóvel, ao tablet e ao computador, e que suporta ampliação. As páginas não obrigam a deslizar para o lado em ecrãs com 320 píxeis de largura.</li>
<li>Os resultados eleitorais são apresentados como uma lista de etiquetas e valores, que se adapta ao telemóvel sem deslizar para o lado e que os leitores de ecrã e os modos de leitura apresentam sem repetições.</li>
<li>As ligações que abrem num separador novo avisam os leitores de ecrã disso. Os botões de descarregar fotografias dizem, para os leitores de ecrã, de que fotografia se trata, e as expressões em inglês estão marcadas com o idioma certo, para serem lidas com a pronúncia correta.</li>
<li>Respeito pela definição do sistema “reduzir movimento”: quem a tiver ligada deixa de ver a página deslizar e as setas a rodar.</li>
<li>Na página do programa, o mapa pode ser deslocado e aproximado com o teclado (setas para o deslocar, mais e menos para aproximar). Os pontos e as linhas do mapa só se abrem com o rato ou com o toque, por isso tudo o que está no mapa também está em texto.</li>
<li>O idioma da página indicado (português de Portugal).</li>
</ul>
<h2>Limitações conhecidas</h2>
<ul>
<li>As descrições das fotografias são curtas e descrevem a cena de forma geral.</li>
<li>O mapa do programa é visual por natureza. Os pontos e as linhas não se podem selecionar com o teclado, os traçados e as localizações são indicativos e as ilustrações dos cartões são decorativas.</li>
<li>Em ecrãs de toque, as ligações do rodapé e do menu são pequenas, o que pode dificultar o toque.</li>
<li>As ligações para sites de terceiros (jornais e redes sociais) levam a páginas cuja acessibilidade não controlo.</li>
</ul>
<h2>Encontraste um problema?</h2>
<p>Se alguma parte do site te for difícil de usar, ou se precisares do conteúdo noutro formato, escreve para <a href="mailto:{EMAIL}">{EMAIL}</a>. Respondo e, sempre que possível, corrijo.</p>
"""
open('_site/privacidade.html','w',encoding='utf-8').write(legal_page('/privacidade','Política de privacidade','Que dados pessoais este site trata e porquê: sem cookies, sem publicidade e com estatísticas que respeitam a privacidade.',priv))
open('_site/acessibilidade.html','w',encoding='utf-8').write(legal_page('/acessibilidade','Declaração de acessibilidade','O que este site faz para ser acessível, as limitações conhecidas e como reportar problemas.',acc))
# ---------- home: fonts self-hosted, JSON-LD, extras ----------
home=open(src,encoding='utf-8').read()
home=NAVFIX(home)
home=re.sub(r'<link rel="icon"[^>]*>\s*<link rel="apple-touch-icon"[^>]*>',lambda m:fav,home,count=1)
assert 'data:image/png' not in home
home=re.sub(r'<link rel="preconnect" href="https://fonts.googleapis.com">\n','',home)
home=home.replace('<link rel="icon"','<link rel="canonical" href="https://henriquelonga.pt/">\n<link rel="icon"',1)
home=home.replace('<meta name="twitter:card" content="summary_large_image">','<meta name="twitter:card" content="summary_large_image">\n'+SOCIAL_META,1)
home=re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com/css2[^>]*>\n','',home)
home=re.sub(r'(<style>)(.*?)(</style>)',lambda m:m.group(1)+'\n'+FONTFACE+FX(m.group(2).lstrip('\n'))+NOTICE_CSS+MOTION_CSS+m.group(3),home,count=1,flags=re.S)
home=home.replace('<div id="page">\n','<div id="page">\n'+NOTICE_HTML,1)
home=home.replace('</body>',UX_JS+NOTICE_JS+'</body>',1)
home_lis=''.join('<li><a href="/opiniao/%s"><span class="t">%s</span><span class="s">%s</span></a></li>'%(k,arts[k]['title'],OUT[k]) for k in ORDER[:3])
home=re.sub(r'<ul class="articles">.*?</ul>',lambda m:'<ul class="articles">'+home_lis+'</ul>',home,count=1,flags=re.S)
home_ld={"@context":"https://schema.org","@graph":[PERSON,WEBSITE]}
home=home.replace('<style>',extra_head(home_ld)+'<style>',1)
open('_site/index.html','w',encoding='utf-8').write(home)

# ---------- press page ----------
BIO50='Henrique Longa, natural de Sesimbra, é estudante de Química Aplicada na NOVA FCT e ativista cívico. Integra o Grupo de Coordenação Local do LIVRE em Setúbal e foi cabeça-de-lista do partido à Assembleia Municipal de Sesimbra em 2025. Tem percurso no Escutismo e na Greve Climática Estudantil.'
BIO100='Henrique José Longa Correia, natural de Sesimbra, é estudante de Química Aplicada na Faculdade de Ciências e Tecnologia da Universidade NOVA de Lisboa, com investigação em Síntese Orgânica. Tem cerca de doze anos de Escutismo, integrou a Greve Climática Estudantil e o Fridays for Future e é coautor do Teenager Climate Guide. É Vice-Presidente para as Operações da Associação Nacional de Estudantes de Química e colaborou com o Conselho Nacional de Juventude. Membro do LIVRE desde 2024, integra o Grupo de Coordenação Local do Núcleo Territorial Distrital de Setúbal e foi cabeça-de-lista à Assembleia Municipal de Sesimbra em 2025.'
print('words',len(BIO50.split()),len(BIO100.split()))
def EN(t): return t.replace('Fridays for Future','<span lang="en">Fridays for Future</span>').replace('Teenager Climate Guide','<span lang="en">Teenager Climate Guide</span>')
MEDIA=[
 ('Declarações na manifestação pela habitação','Canal NOW, 27 de outubro de 2026 (Instagram)','https://www.instagram.com/p/DfCm8RLIo3c'),
 ('Autárquicas 2025: debate para a Assembleia Municipal de Sesimbra','Vídeo no YouTube, 30 de setembro de 2025','https://youtu.be/upJXiGhW1j8'),
 ('Henrique Longa: LIVRE quer “Sesimbra de 15 minutos” e “Plano de ação climática”','O Sesimbrense, entrevista, 31 de agosto de 2025','/entrevista/livre-quer-sesimbra-de-15-minutos-e-plano-de-acao-climatica'),
 ('LIVRE avança com Carina Calisto à Câmara de Sesimbra e Henrique Longa para a Assembleia Municipal','O Setubalense, notícia, 31 de julho de 2025','https://osetubalense.com/local/sesimbra/livre-avanca-com-carina-calisto-a-camara-de-sesimbra-e-henrique-longa-para-a-assembleia-municipal'),
 ('Apresentação de Henrique Longa – Sesimbra | Primárias do LIVRE','Vídeo no YouTube, 6 de julho de 2025','https://youtu.be/HQIG6Ry5ZEo'),
]
media_li=''.join('<li><a href="%s"%s><span class="t">%s</span><span class="s">%s</span></a></li>\n'%(u,'' if u.startswith('/') else ' target="_blank" rel="noopener"',esc(t),esc(m)) for t,m,u in MEDIA)
op_li=''.join('<li><a href="/opiniao/%s"><span class="t">%s</span><span class="s">%s, %s</span></a></li>\n'%(k,arts[k]['title'],OUT[k],re.search(r'<time[^>]*>(.*?)</time>',arts[k]['meta']).group(1)) for k in ORDER[:3])
press_css="""
.press-sec{margin:2em 0 .5em;font:800 clamp(24px,3.4vw,30px)/1.2 Archivo,"Archivo Fallback","Helvetica Neue",Arial,sans-serif}
h1+.press-sec{margin-top:0}
.press-text{max-width:36em;font-size:20px;line-height:1.7}
.press-text p{margin:0 0 1em}
.bio-short{margin:0 0 30px;max-width:36em}
.bio-short h3{margin:0 0 8px;font:800 18px/1.3 Archivo,"Archivo Fallback","Helvetica Neue",Arial,sans-serif}
.bio-short p{margin:0 0 12px;font-size:20px;line-height:1.7}
.copybtn{padding:9px 16px;border:2px solid var(--ink);border-radius:6px;background:transparent;color:var(--ink);font:700 15px Archivo,"Archivo Fallback",Arial,sans-serif;cursor:pointer}
:where(html:not(.sem-rato)) .copybtn:hover{background:var(--ink);color:var(--paper)}
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
<div class="bio-short"><h3>Versão de cerca de 100 palavras</h3><p id="bio100">{EN(esc(BIO100))}</p><button type="button" class="copybtn" data-copy-target="bio100">Copiar</button></div>
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
LASTMOD={'/opiniao/'+r[1]:r[0] for r in rows}   # data de publicação de cada artigo

# ---------- Programa para Sesimbra (/programa) ----------
import time as _t
_V=str(int(_t.time()))
def prog_page():
    import json as _j
    comp=_j.load(open('gerador/programa/programa_completo.json',encoding='utf-8'))
    areas=''
    for n,a in enumerate(comp,1):
        li=''
        for m in a['medidas']:
            w=m['t'].rsplit(' ',1)
            tt=(esc(w[0])+' ' if len(w)>1 else '')+'<span class="lw">'+esc(w[-1])+'<i class="chv" aria-hidden="true"></i></span>'
            onde=''   # o programa completo não leva ligações para o mapa
            li+='<li><details><summary>%s</summary><p>%s</p>%s</details></li>'%(tt,esc(m['d']),onde)
        areas+='<div class="area"><h3 data-c="p%d"><span class="acc-t">%s</span></h3><div class="acc-body" id="p%d"><ul>%s</ul></div></div>\n'%(n,esc(a['area']),n,li)
    main=f"""<main id="conteudo" tabindex="-1" class="prog">
<section class="sq">
<div class="wrap">
<h1>Programa para Sesimbra</h1>
<p class="sq-lead">Sesimbra tem tudo para valorizar as suas raízes, respeitar o ambiente e preparar o futuro. Bairros, transportes, habitação acessível e espaços verdes, onde se vive em comunidade.</p>
<a class="skip" href="#programa-completo">Saltar o mapa e ir para o programa completo</a>
<h2 class="sr">Mapa do programa</h2>
<div class="sq-busca" role="search"><label for="sq-q">Procurar no mapa</label><div class="sq-busca-c"><input type="search" id="sq-q" role="combobox" aria-expanded="false" aria-controls="sq-res" aria-autocomplete="list" autocomplete="off" placeholder="Localidade, serviço, rua…"><ul id="sq-res" role="listbox" aria-label="Resultados da pesquisa" hidden></ul></div><p class="sr" id="sq-res-n" aria-live="polite"></p></div>
<div class="sq-corpo">
<div class="sq-col-mapa">
<div class="sq-mapa" id="sq-mapa" role="region" aria-label="Mapa do programa para o concelho de Sesimbra"></div>
<p class="sq-dica" id="sq-dica"><span class="sq-dica-pc">Com o cursor sobre o mapa, a roda do rato aproxima e afasta. Fora do mapa, a página desce normalmente. Para escolher o que ver no mapa, abre-o em ecrã inteiro.</span><span class="sq-dica-tel">Afasta dois dedos no ecrã para aproximar. Para escolher o que ver, abre o mapa em ecrã inteiro.</span></p>
<div class="sq-notas" id="sq-notas"></div>
</div>
<div class="sq-col-cartao">
<article class="sq-postal" id="sq-postal" aria-label="Cartão da localidade"></article>
</div>
</div>
<p class="sq-aviso sq-vivo"><strong>Um programa vivo.</strong> Este mapa reúne ideias e propostas para Sesimbra, que vão sendo atualizadas e discutidas. Os traçados e as localizações são indicativos.</p>
<p class="sq-dados sq-sug-txt">Para sugerir alterações, abre o mapa em ecrã inteiro e usa “Sugerir no mapa”.</p>
<p class="sq-dados sq-sug-mail">Para sugerir alterações, envia email para <a href="mailto:geral@henriquelonga.pt">geral@henriquelonga.pt</a>.</p>
<p class="sq-dados">Dados do mapa abertos para descarregar: <a href="/programa-mapa/dados/programa-sesimbra.geojson" download>GeoJSON</a> e <a href="/programa-mapa/dados/programa-sesimbra.csv" download>CSV</a>.</p>
<noscript><p class="sq-semjs">O mapa precisa de JavaScript. O programa completo está mais abaixo nesta página.</p></noscript>
</div>
</section>
<section id="programa-completo" class="tint sq-completo">
<div class="wrap">
<h2>Programa completo</h2>
{areas}</div>
</section>
</main>"""
    ex='<script src="/programa-mapa/leaflet.js?v='+_V+'"></script>\n<script src="/programa-mapa/programa-dados.js?v='+_V+'"></script>\n<script src="/programa-mapa/programa.js?v='+_V+'"></script>\n<script src="/programa-mapa/sugestao.js?v='+_V+'"></script>\n'
    h=head('/programa','Programa para Sesimbra','Programa de Henrique Longa para Sesimbra. Mapa com as propostas para cada localidade, estradas e natureza, e o programa completo por áreas.',css+'\n'+article_css,'website',None,'<link rel="stylesheet" href="/programa-mapa/leaflet.css?v='+_V+'">\n<link rel="stylesheet" href="/programa-mapa/programa.css?v='+_V+'">')
    return h+body(header.replace('<a href="/programa">','<a href="/programa" aria-current="page">'),main,ex)
if os.path.isdir('gerador/programa'):
    os.makedirs('_site/programa-mapa',exist_ok=True)
    for _f in ('leaflet.css','leaflet.js','programa.css','programa.js','sugestao.js'):
        shutil.copy('gerador/programa/'+_f,'_site/programa-mapa/'+_f)
    import json as _jj
    _D=_jj.load(open('gerador/programa/mapa.json',encoding='utf-8'))
    for _l in _D.get('linhas',[]): _l.pop('pontos',None)
    open('_site/programa-mapa/programa-dados.js','w',encoding='utf-8').write('/* Gerado a partir de gerador/programa/mapa.json (painel do mapa) */\nvar DADOS = '+_jj.dumps(_D,ensure_ascii=False,separators=(',',':'))+';\n')
    # índice de ruas para a pesquisa: nome, ponto, cartão da localidade (se estiver dentro de uma) e nome da localidade
    if os.path.isfile('gerador/programa/ruas.json'):
        _R=_jj.load(open('gerador/programa/ruas.json',encoding='utf-8'))
        _ZB=[(z['id'],z['nome'],z['limite']) for z in _D['zonas'] if z.get('camada')=='bairros' and z.get('limite')]
        def _dentro(la,lo,anel):
            c=False; j=len(anel)-1
            for i in range(len(anel)):
                yi,xi=anel[i]; yj,xj=anel[j]
                if (xi>lo)!=(xj>lo) and la<(yj-yi)*(lo-xi)/(xj-xi)+yi: c=not c
                j=i
            return c
        _LOC=[(l['nome'],l['p']) for l in _D.get('localidades',[])]
        _EXC={'footway','steps','cycleway','path','track','bridleway','proposed','construction','service','corridor'}
        # contorno do concelho de Sesimbra (anéis montados a partir dos troços 'outer' da relação), para não incluir ruas de concelhos vizinhos
        _bb=[e['bounds'] for e in _jj.load(open('gerador/programa/limites.json',encoding='utf-8'))['elements'] if e.get('tags',{}).get('name')=='Sesimbra' and e['type']=='relation'][0]
        _rel=[e for e in _jj.load(open('gerador/programa/limites.json',encoding='utf-8'))['elements'] if e.get('tags',{}).get('name')=='Sesimbra' and e['type']=='relation'][0]
        _rest=[[(p['lat'],p['lon']) for p in m['geometry']] for m in _rel['members'] if m['role']=='outer' and m.get('geometry')]
        _aneis=[]
        while _rest:
            _cur=_rest.pop(0)
            while _cur[0]!=_cur[-1]:
                for _i,_w in enumerate(_rest):
                    if _w[0]==_cur[-1]: _cur=_cur+_w[1:]
                    elif _w[-1]==_cur[-1]: _cur=_cur+_w[::-1][1:]
                    elif _w[-1]==_cur[0]: _cur=_w+_cur[1:]
                    elif _w[0]==_cur[0]: _cur=_w[::-1]+_cur[1:]
                    else: continue
                    _rest.pop(_i); break
                else: break
            _aneis.append(_cur)
        def _noConcelho(la,lo): return any(_dentro(la,lo,a) for a in _aneis)
        _porNome={}
        for _e in _R.get('elements',[]):
            _t=_e.get('tags',{}); _g=_e.get('geometry')
            if not _t.get('name') or not _t.get('highway') or _t['highway'] in _EXC or not _g: continue
            _m=_g[len(_g)//2]
            if not (_bb['minlat']-0.002<=_m['lat']<=_bb['maxlat']+0.002 and _bb['minlon']-0.002<=_m['lon']<=_bb['maxlon']+0.002) and not any(_bb['minlat']<=p['lat']<=_bb['maxlat'] and _bb['minlon']<=p['lon']<=_bb['maxlon'] for p in _g[::3]): continue
            # entra se qualquer parte da rua estiver dentro do concelho; o ponto escolhido é um ponto dentro dele
            _rep=None
            for _p in [_m,_g[0],_g[-1]]+_g[::2]:
                if _bb['minlat']<=_p['lat']<=_bb['maxlat'] and _bb['minlon']<=_p['lon']<=_bb['maxlon'] and _noConcelho(_p['lat'],_p['lon']): _rep=_p; break
            if not _rep: continue
            _porNome.setdefault(_t['name'],[]).append((_g,_rep))
        # troços do mesmo nome que se tocam (a menos de ~300 m) são a mesma rua: uma só entrada
        _gr={}
        for _n,_ways in _porNome.items():
            _reps=[r for _,r in _ways]; _ways=[g for g,_ in _ways]
            _pai=list(range(len(_ways)))
            def _f(x):
                while _pai[x]!=x: _pai[x]=_pai[_pai[x]]; x=_pai[x]
                return x
            _cel={}
            for _i,_w in enumerate(_ways):
                for _p in _w[::2]+[_w[-1]]:
                    _c=(round(_p['lat']/0.003),round(_p['lon']/0.004))
                    for _dy in (-1,0,1):
                        for _dx in (-1,0,1):
                            for _k in _cel.get((_c[0]+_dy,_c[1]+_dx),()):
                                _pai[_f(_i)]=_f(_k)
                    _cel.setdefault(_c,set()).add(_i)
            _cl={}
            for _i,_w in enumerate(_ways): _cl.setdefault(_f(_i),[]).append((_w,_reps[_i]))
            for _k,_ws in _cl.items():
                _pts=[r for _,r in _ws]; _tam=sum(len(w) for w,_ in _ws)
                _cla=sum(p['lat'] for p in _pts)/len(_pts); _clo=sum(p['lon'] for p in _pts)/len(_pts)
                _m=min(_pts,key=lambda p:(p['lat']-_cla)**2+(p['lon']-_clo)**2)   # ponto da rua mais perto do centro
                _gr[(_n,_k)]=(_tam,_m['lat'],_m['lon'])
        _out=[]
        _out_t=[]
        for (_n,_k2),(_ln,_la,_lo) in sorted(_gr.items(),key=lambda kv:-kv[1][0]):
            _zid='';_loc=''
            for _id,_nm,_lim in _ZB:
                if any(_dentro(_la,_lo,_a) for _a in _lim): _zid=_id;_loc=_nm;break
            if not _zid and _LOC:
                _d,_nn=min(((( _la-p[0])**2+((_lo-p[1])*0.78)**2),n) for n,p in _LOC)
                if _d<0.02**2: _loc=_nn
            if any(o[0]==_n and (o[1]-_la)**2+((o[2]-_lo)*0.78)**2<0.015**2 for o in _out): continue   # troço da mesma rua, perto de outro maior
            _out.append([_n,round(_la,5),round(_lo,5),_zid,_loc])
        _v=set(); _o2=[]
        for _r in _out:
            _kk=(_r[0],_r[3] or _r[4] or (_r[1],_r[2]))
            if _kk in _v: continue
            _v.add(_kk); _o2.append(_r)
        _out=_o2
        _out.sort(key=lambda r:r[0])
        open('_site/programa-mapa/programa-ruas.js','w',encoding='utf-8').write('/* Ruas (© colaboradores do OpenStreetMap, ODbL) para a pesquisa do mapa */\nvar RUAS = '+_jj.dumps(_out,ensure_ascii=False,separators=(',',':'))+';\n')
    # dados abertos: GeoJSON e CSV gerados a partir do mesmo ficheiro do mapa
    import csv as _csv, io as _io
    _CAT={'parque':'Parque ou jardim','escola':'Escola','saude':'Saúde','farmacia':'Farmácia','estacionamento':'Estacionamento','bombeiros':'Bombeiros','policia':'Polícia','igreja':'Igreja ou capela','cultura':'Biblioteca, auditório, cultura','servicos':'Serviços públicos','mercado':'Mercado e supermercado','desporto':'Desporto','social':'Apoio social e comunitário','obra':'Proposta no mapa','transporte':'Estação ou terminal'}
    _CAM={c['id']:c['nome'] for c in _D.get('camadas',[])}; _CAM.update({'vias':'Estradas','autocarro':'Autocarro'})
    _feat=[]; _rows=[]
    for _p in _D.get('pontos',[])+_D.get('manuais',[]):
        _t='proposta' if _p['cat']=='obra' else 'existente'
        _pr={'tipo':_t,'categoria':_CAT.get(_p['cat'],_p['cat']),'nome':_p['nome']}
        if _p.get('texto') and _p['cat']!='obra': _pr['descricao']=_p['texto']
        _feat.append({'type':'Feature','properties':_pr,'geometry':{'type':'Point','coordinates':[_p['p'][1],_p['p'][0]]}})
        _rows.append([_pr['tipo'],_pr['categoria'],_pr['nome'],_pr.get('descricao',''),_p['p'][0],_p['p'][1]])
    for _i in _D.get('interfaces',[]):
        _pr={'tipo':'existente' if _i.get('existe') else 'proposta','categoria':'Estação ou hub','nome':_i['nome'],'descricao':_i.get('texto','')}
        _feat.append({'type':'Feature','properties':_pr,'geometry':{'type':'Point','coordinates':[_i['p'][1],_i['p'][0]]}})
        _rows.append([_pr['tipo'],_pr['categoria'],_pr['nome'],_pr['descricao'],_i['p'][0],_i['p'][1]])
    for _l in _D.get('linhas',[]):
        _pr={'tipo':_l.get('estado','proposta'),'categoria':_CAM.get(_l.get('camada'),_l.get('camada','')),'nome':_l['nome']}
        if _l.get('texto'): _pr['descricao']=_l['texto']
        _feat.append({'type':'Feature','properties':_pr,'geometry':{'type':'LineString','coordinates':[[c[1],c[0]] for c in _l['coords']]}})
    _gj={'type':'FeatureCollection','name':'Programa para Sesimbra','license':'ODbL-1.0','attribution':'Contém dados © colaboradores do OpenStreetMap (ODbL). © Henrique Longa, programa para Sesimbra.','features':_feat}
    os.makedirs('_site/programa-mapa/dados',exist_ok=True)
    open('_site/programa-mapa/dados/programa-sesimbra.geojson','w',encoding='utf-8').write(_jj.dumps(_gj,ensure_ascii=False,separators=(',',':')))
    _o=_io.StringIO(); _w=_csv.writer(_o,lineterminator='\n'); _w.writerow(['tipo','categoria','nome','descricao','latitude','longitude']); _w.writerows(_rows)
    open('_site/programa-mapa/dados/programa-sesimbra.csv','w',encoding='utf-8-sig',newline='').write(_o.getvalue())
    open('_site/programa.html','w',encoding='utf-8').write(prog_page())
urls=['/','/biografia','/programa','/opiniao/']+['/opiniao/'+r[1] for r in rows]+['/imprensa','/entrevista/livre-quer-sesimbra-de-15-minutos-e-plano-de-acao-climatica','/galeria','/privacidade','/acessibilidade']
def _sm(u):
    img=''.join('<image:image><image:loc>%s/fotos/%s</image:loc></image:image>'%(SITE,ph['file']) for ph in PHOTOS) if u=='/galeria' else ''
    lm=('<lastmod>%s</lastmod>'%LASTMOD[u]) if u in LASTMOD else ''
    return '<url><loc>%s%s</loc>%s%s</url>\n'%(SITE,u,lm,img)
open('_site/sitemap.xml','w',encoding='utf-8').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+''.join(_sm(u) for u in urls)+'</urlset>\n')
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
    _n=re.sub(r'<a\b([^>]*\btarget="_blank"[^>]*)>',lambda m: m.group(0) if 'aria-describedby' in m.group(1) else '<a'+m.group(1)+' aria-describedby="nt">',_n)
    if 'aria-describedby="nt"' in _n and 'id="nt"' not in _n:
        _n=_n.replace('<body>','<body>\n<span id="nt" hidden>Abre num novo separador</span>',1)
    _n=_n.replace('a:focus-visible{outline:3px solid var(--accent);outline-offset:3px}','a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid var(--accent);outline-offset:3px}',1)
    if 'id="fx"' not in _n:
        _n=_n.replace('</head>','<style id="fx">.ctl input:focus-visible,.ctl select:focus-visible,.skip:focus,.acc-btn:focus-visible{outline-offset:3px}.sea a:focus-visible,.sea button:focus-visible,.sea input:focus-visible,.sea summary:focus-visible,.contact a:focus-visible,.contact button:focus-visible{outline-color:var(--ink)}</style>\n</head>',1)
    if _n!=_t: open(_f,'w',encoding='utf-8').write(_n)
print('Site gerado em _site/ com',sum(len(f) for _,_,f in os.walk('_site')),'ficheiros e',len(arts),'artigos.')

# ---------- glossário, ligação no rodapé e siglas ----------
_old='Henrique Longa. Todos os direitos reservados. <a href="/privacidade">Privacidade</a> | <a href="/acessibilidade">Acessibilidade</a></footer>'
_new='Henrique Longa. Todos os direitos reservados. <a href="/privacidade">Privacidade</a> | <a href="/acessibilidade">Acessibilidade</a></footer>'
for _f in glob.glob('_site/*.html')+glob.glob('_site/opiniao/*.html'):
    _t=open(_f,encoding='utf-8').read()
    if _old in _t: _t=_t.replace(_old,_new)
    open(_f,'w',encoding='utf-8').write(_t)
