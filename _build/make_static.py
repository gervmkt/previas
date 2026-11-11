"""Gera a prévia estática de um cliente (abre no navegador, sem login).
uso: python3 make_static.py <slug> <perfil.json> <posts_dir> <redes,separadas> <filtro> <dir_midias> <saida_site>
"""
import sys,json,os,shutil,re,subprocess
slug,perfil_f,posts_dir,redes,filtro,mdir,out=sys.argv[1:8]
redes=[r for r in redes.split(",") if r]
subprocess.run(["python3","make_cliente.py","/tmp/_cli.html"],check=True,cwd=os.path.dirname(os.path.abspath(__file__)))
s=open("/tmp/_cli.html").read()
perfil=json.load(open(perfil_f));perfil.setdefault("id","p")
ACC={"ig":["foto","carrossel","reel","story"],"li":["foto","carrossel","reel","texto","artigo","enquete","link","evento"],"tt":["reel","carrossel","foto"],"fb":["foto","carrossel","reel","texto","story","link"]}
OK={"todos":None,"aprov":{"aprovacao","aprovado","agendado","publicado"},"emaprov":{"aprovacao"}}[filtro]
posts=[]
for f in sorted(os.listdir(posts_dir)):
    x=json.load(open(os.path.join(posts_dir,f)));x.setdefault("id",f.rsplit(".",1)[0])
    x["redes"]=[r for r in x.get("redes",[]) if r in redes and x.get("formato") in ACC[r]]
    if not x["redes"] or (OK and x.get("status") not in OK):continue
    if x.get("formato") not in ("texto","enquete","link") and not (x.get("midias") or []):continue
    x.pop("notas",None);x["perfil"]=perfil["id"];posts.append(x)
site=os.path.join(out,slug);os.makedirs(os.path.join(site,"media"),exist_ok=True)
files={f.rsplit(".",1)[0]:f for f in os.listdir(mdir)}
def fix(m):
    if m and m.get("a"):
        fn=files[m["a"]];shutil.copy(os.path.join(mdir,fn),os.path.join(site,"media",fn));m["a"]=fn
for x in posts:
    for m in x.get("midias") or []:fix(m)
    if x.get("capa"):fix(x["capa"])
if perfil.get("foto"):
    fn=files[perfil["foto"]];shutil.copy(os.path.join(mdir,fn),os.path.join(site,"media",fn));perfil["foto"]=fn
data={"perfis":[perfil],"posts":posts,"redes":redes}
def rep(a,b):
    global s
    assert s.count(a)==1,(a[:60],s.count(a));s=s.replace(a,b)
rep('const media=m=>m?(m.a?"/_blob/"+m.a:','const media=m=>m?(m.a?"media/"+m.a:')
rep('Clique num post para vê-lo no celular. Para comentar ou aprovar, use os comentários desta página.','Clique num post para vê-lo no celular. Para aprovar ou pedir ajustes, responda pela conversa com a {ger}.')
i=s.index('(async()=>{\n  db=await claude.use("db");');j=s.index('})();',i)+5
boot='''(function(){const D=window.__PREVIA;canWrite=false;const r=D.redes||[];
  if(r.length){Object.keys(NETS).forEach(k=>{if(!r.includes(k))delete NETS[k]});if(!NETS[net])net=Object.keys(NETS)[0]}
  perfis=D.perfis;posts=D.posts;cur=perfis[0].id;setStatus("");renderAll()})();
(function(){const _rp=renderPhone;renderPhone=function(){_rp();document.getElementById("phone").classList.toggle("auto",!isFull())};renderPhone()})();'''
s=s[:i]+boot+s[j:]
s=s.replace('setStatus("Carregando a prévia…");','')
nome=perfil.get("nome") or perfil.get("usuario") or slug
s=s.replace('<title>{ger} Prévia</title>','')
payload=json.dumps(data,ensure_ascii=False).replace("</","<\\/")
html=f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow,noarchive"><title>{{ger}} Prévia · {nome}</title>
<style>*,*::before,*::after{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}body{{margin:0}}</style>
<style>.side{{display:none!important}}.layout{{grid-template-columns:minmax(0,1fr)!important;justify-items:center}}.stage{{position:static!important}}.phone.auto{{height:auto!important;min-height:0!important}}.phone.auto .scr{{position:relative;inset:auto;overflow:visible}}.phone.auto .sb,.phone.auto .ig-top,.phone.auto .li-top,.phone.auto .fb-top,.phone.auto .igp-tabs{{position:relative!important;top:auto!important}}</style>
<script>window.__PREVIA={payload};</script>
</head><body>
{s}
</body></html>'''
open(os.path.join(site,"index.html"),"w").write(html)
os.makedirs(out,exist_ok=True)
open(os.path.join(out,"robots.txt"),"w").write("User-agent: *\nDisallow: /\n")
if not os.path.exists(os.path.join(out,"index.html")):
    open(os.path.join(out,"index.html"),"w").write('<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex"><title>{ger}</title><body style="font-family:sans-serif;background:#111;color:#FFC800;display:grid;place-items:center;height:100vh;margin:0"><b style="font-size:40px">{ger}</b></body>')
open(os.path.join(out,".nojekyll"),"w").write("")
print(site,len(posts),"posts")
