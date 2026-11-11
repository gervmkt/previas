"""Gera a prévia estática de um cliente (abre no navegador, sem login).
uso: python3 make_static.py <slug> <perfil.json> <posts_dir> <redes,separadas> <filtro> <dir_midias> <saida_site>
"""
import sys,json,os,shutil,re,subprocess
slug,perfil_f,posts_dir,redes,filtro,mdir,out=sys.argv[1:8]
PINI=sys.argv[8] if len(sys.argv)>8 and sys.argv[8] else None
PFIM=sys.argv[9] if len(sys.argv)>9 and sys.argv[9] else None
redes=[r for r in redes.split(",") if r]
subprocess.run(["python3","make_cliente.py","/tmp/_cli.html"],check=True,cwd=os.path.dirname(os.path.abspath(__file__)))
s=open("/tmp/_cli.html").read()
perfil=json.load(open(perfil_f));perfil.setdefault("id","p")
ACC={"ig":["foto","carrossel","reel","story"],"li":["foto","carrossel","reel","texto","artigo","enquete","link","evento"],"tt":["reel","carrossel","foto"],"fb":["foto","carrossel","reel","texto","story","link"],"wa":["foto","carrossel","reel","texto","link","story"]}
OK={"todos":None,"aprov":{"aprovacao","aprovado","agendado","publicado"},"emaprov":{"aprovacao"}}[filtro]
posts=[]
for f in sorted(os.listdir(posts_dir)):
    x=json.load(open(os.path.join(posts_dir,f)));x.setdefault("id",f.rsplit(".",1)[0])
    x["redes"]=[r for r in x.get("redes",[]) if r in redes and x.get("formato") in ACC[r]]
    if not x["redes"] or (OK and x.get("status") not in OK):continue
    if x.get("formato") not in ("texto","enquete","link") and not (x.get("midias") or []):continue
    if PINI:
        dt=(x.get("data") or "")[:10]
        if not dt or dt<PINI or dt>PFIM:continue
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
import datetime
data={"perfis":[perfil],"posts":posts,"redes":redes,"geradoEm":datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),"periodo":({"ini":PINI,"fim":PFIM} if PINI else None)}
def rep(a,b):
    global s
    assert s.count(a)==1,(a[:60],s.count(a));s=s.replace(a,b)
rep('const media=m=>m?(m.a?"/_blob/"+m.a:','const media=m=>m?(m.a?"media/"+m.a:')
rep('Clique num post para vê-lo no celular. Para comentar ou aprovar, use os comentários desta página.','Clique num post para vê-lo no celular. Para aprovar ou pedir ajustes, responda pela conversa com a {ger}.')
i=s.index('(async()=>{\n  db=await claude.use("db");');j=s.index('})();',i)+5
boot='''(function(){const D=window.__PREVIA;canWrite=false;const r=D.redes||[];
  if(r.length){Object.keys(NETS).forEach(k=>{if(!r.includes(k))delete NETS[k]});if(!NETS[net])net=Object.keys(NETS)[0]}
  perfis=D.perfis;posts=D.posts;cur=perfis[0].id;setStatus("");renderAll()})();
(function(){const _rp=renderPhone;renderPhone=function(){_rp();document.getElementById("phone").classList.toggle("auto",!isFull())};renderPhone()})();
(function(){const D=window.__PREVIA,p=(D.perfis||[])[0]||{};const h=document.querySelector(".hbar");if(!h)return;let f="";const t=new Date(D.geradoEm||"");if(!isNaN(t)){f=t.toLocaleDateString("pt-BR",{timeZone:"America/Sao_Paulo",day:"numeric",month:"short"}).replace(/\\./g,"").replace(/ de /g," ")+", "+t.toLocaleTimeString("pt-BR",{timeZone:"America/Sao_Paulo",hour:"2-digit",minute:"2-digit"})}const redes=Object.values(NETS).map(n=>n.n);const nav=document.getElementById("nets");if(nav&&redes.length<2)nav.classList.add("solo");const m=document.createElement("div");m.className="pv-meta";const b=document.createElement("b");b.textContent="Prévia · "+(p.nome||p.usuario||"");const P=D.periodo;let ptxt="";if(P&&P.ini){const a=new Date(P.ini+"T12:00"),z=new Date(P.fim+"T12:00");const M=x=>x.toLocaleDateString("pt-BR",{month:"long"});ptxt=(a.getMonth()===z.getMonth()?"Semana de "+a.getDate()+" a "+z.getDate()+" de "+M(z):"De "+a.getDate()+" de "+M(a)+" a "+z.getDate()+" de "+M(z))}
 if(ptxt){const w=document.createElement("em");w.textContent=ptxt;m.append(b,w)}else m.append(b);const s=document.createElement("span");s.innerHTML="<i></i>";s.append((redes.length<2?redes[0]+" · ":"")+(f?"atualizada em "+f:""));m.append(s);const br=h.querySelector(".brand");h.insertBefore(m,br?br.nextSibling:h.firstChild);document.title="{ger} · Prévia "+(p.nome||"")})();
(function(){const D=window.__PREVIA,P=D.periodo;if(!P||!P.ini)return;
 const DOW=["DOM","SEG","TER","QUA","QUI","SEX","SÁB"],DOWL=["Domingo","Segunda","Terça","Quarta","Quinta","Sexta","Sábado"];
 const days=[];{const a=new Date(P.ini+"T12:00"),z=new Date(P.fim+"T12:00");for(const t=new Date(a);t<=z&&days.length<31;t.setDate(t.getDate()+1))days.push(t.getFullYear()+"-"+String(t.getMonth()+1).padStart(2,"0")+"-"+String(t.getDate()).padStart(2,"0"))}
 const dOf=p=>(p.data||"").slice(0,10);const okNet=p=>(p.redes||[]).some(r=>NETS[r]&&NETS[r].acc.includes(p.formato));
 const per=d=>posts.filter(p=>dOf(p)===d&&okNet(p));
 let dia=null,cur1=null;
 vis=function(p){if(!dia||view[net]==="perfil"||(net==="tt"&&view.tt==="perfil"))return true;return dOf(p)===dia};
 ord=function(a,b){const x=String(a.data||"9"),y=String(b.data||"9");return (view[net]==="perfil"||view[net]==="perfil")?y.localeCompare(x):x.localeCompare(y)};
 const FN={foto:"Foto",carrossel:"Carrossel",reel:"Reel",story:"Story",texto:"Post de texto",artigo:"Artigo",enquete:"Enquete",link:"Link",evento:"Evento"};
 function lbl(p){const d=dOf(p);if(!d)return"";const t=new Date(d+"T12:00");const hh=(p.data||"").slice(11,16);const h=hh?(hh.endsWith(":00")?String(+hh.slice(0,2))+"h":hh.replace(":","h")):"";
   return DOWL[t.getDay()]+", "+String(t.getDate()).padStart(2,"0")+"/"+String(t.getMonth()+1).padStart(2,"0")+(h?" · "+h:"")+" · "+(FN[p.formato]||"")}
 const box=document.createElement("div");box.className="pv-week";const stage=document.querySelector(".stage");stage.insertBefore(box,stage.firstChild);
 function strip(){const tot=posts.filter(okNet).length;
   box.innerHTML='<button type="button" class="pv-all" data-dia="" aria-pressed="'+(!dia)+'">Semana toda <span>'+tot+(tot>1?" posts":" post")+'</span></button><div class="pv-days" role="toolbar" aria-label="Dias da semana">'+days.map(d=>{const n=per(d).length,t=new Date(d+"T12:00");return'<button type="button" class="pvd" data-dia="'+d+'" aria-pressed="'+(dia===d)+'"'+(n?"":" disabled")+' aria-label="'+DOWL[t.getDay()]+", "+t.getDate()+(n?", "+n+(n>1?" posts":" post"):", sem post")+'"><small>'+DOW[t.getDay()]+'</small><b>'+t.getDate()+'</b>'+(n?'<i>'+(n>1?n:"")+'</i>':"")+'</button>'}).join("")+'</div>'+(dia?(()=>{const t=new Date(dia+"T12:00"),ps=per(dia).sort((a,b)=>String(a.data).localeCompare(String(b.data)));return'<p class="pv-hint"><b>'+DOWL[t.getDay()]+", "+t.getDate()+" de "+t.toLocaleDateString("pt-BR",{month:"long"})+"</b> · "+ps.length+(ps.length>1?" posts. Toque para ver cada um:":" post")+'</p>'+(ps.length>1?'<div class="pv-items">'+ps.map(p=>{const hh=(p.data||"").slice(11,16);const h=hh?(hh.endsWith(":00")?String(+hh.slice(0,2))+"h":hh.replace(":","h")):"";const nets=(p.redes||[]).filter(r=>NETS[r]&&NETS[r].acc.includes(p.formato)).map(r=>NETS[r].n).join(" + ");return'<button type="button" class="pvi" data-go="'+p.id+'" aria-pressed="'+(cur1===p.id)+'">'+(h?"<b>"+h+"</b> · ":"")+(FN[p.formato]||"")+" · "+nets+"</button>"}).join("")+"</div>":"")})():'<p class="pv-hint">Toque num dia para ver só o que sai nele.</p>');
}
 function marks(){const scr=document.getElementById("scr");scr.querySelectorAll(".pv-dl").forEach(x=>x.remove());
   if(view[net]==="perfil")return;
   scr.querySelectorAll("[data-pid]").forEach(el=>{if(el.closest(".tile")||el.classList.contains("tile"))return;const p=posts.find(x=>x.id===el.dataset.pid);if(!p)return;const t=lbl(p);if(!t)return;
     const b=document.createElement("div");b.className="pv-dl";b.textContent=t;if(el.matches(".vitem,.fsv")){b.classList.add("ov");el.appendChild(b)}else el.parentNode.insertBefore(b,el)})}
 const _rp2=renderPhone;renderPhone=function(){_rp2();marks()};
 function goPost(id){const p=posts.find(x=>x.id===id);if(!p)return;cur1=id;const rs=(p.redes||[]).filter(r=>NETS[r]&&NETS[r].acc.includes(p.formato));if(!rs.includes(net))net=rs[0];
   if(p.formato==="story")view[net]=net==="wa"?"status":"stories";else if(net==="tt")view.tt="fyp";else if(net==="wa")view.wa="conversa";else if(net==="ig"&&p.formato==="reel")view.ig="reels";else view[net]="feed";
   artOpen=null;st.key="";st.elapsed=0;focusId=id;pendingFocus=true;renderAll();
   if(p.formato==="story"){const k=st.list.findIndex(x=>x.id===id);if(k>=0&&k!==st.i){st.i=k;renderPhone()}}
   strip()}
 box.addEventListener("click",e=>{const g=e.target.closest("[data-go]");if(g)return goPost(g.dataset.go);const c=e.target.closest("[data-dia]");if(!c||c.disabled)return;dia=c.dataset.dia||null;cur1=null;artOpen=null;st.key="";st.elapsed=0;
   if(dia){const ps=per(dia);if(!ps.some(p=>(p.redes||[]).includes(net)&&NETS[net].acc.includes(p.formato))){const r=(ps[0].redes||[]).find(r=>NETS[r]&&NETS[r].acc.includes(ps[0].formato));if(r)net=r}
     const here=ps.filter(p=>(p.redes||[]).includes(net));const feedish=here.some(p=>p.formato!=="story");
     if(net==="ig")view.ig=feedish?"feed":"stories";else if(net==="fb")view.fb=feedish?"feed":"stories";else if(net==="wa")view.wa=feedish?"conversa":"status";else if(net==="tt")view.tt="fyp";else view[net]="feed";
     const first=ps.sort((a,b)=>String(a.data).localeCompare(String(b.data))).find(p=>(p.redes||[]).includes(net)&&(view[net]==="stories"||view[net]==="status")===(p.formato==="story"));cur1=first?first.id:null}
   else{if(view[net]==="perfil"||view[net]==="stories")view[net]=NETS[net].views.find(v=>v[0]!=="perfil")[0]}
   renderAll();strip();const ph=document.getElementById("phone");if(ph&&dia&&ph.getBoundingClientRect().top<0)ph.scrollIntoView({block:"start",behavior:"smooth"})});
 strip();renderPhone()})();
(function(){const FEED={ig:["foto","carrossel","reel"],fb:["foto","carrossel","reel","texto","link"],wa:["foto","carrossel","reel","texto","link"]};
 function cnt(n,f){return postsFor(n,f).length}
 function prof(n,f){const sv=view[n],sn=net;net=n;view[n]="perfil";const r=postsFor(n,f).length;view[n]=sv;net=sn;return r}
 function has(n,v){if(n==="ig")return v==="perfil"?prof("ig",FEED.ig)>0:cnt("ig",v==="stories"?["story"]:v==="reels"?["reel"]:FEED.ig)>0;
   if(n==="tt")return v==="perfil"?prof("tt"):cnt("tt")>0;
   if(n==="fb")return cnt("fb",v==="stories"?["story"]:FEED.fb)>0;
   if(n==="wa")return cnt("wa",v==="status"?["story"]:FEED.wa)>0;
   return cnt(n)>0}
 const _rv=renderViews;renderViews=function(){const av=NETS[net].views.map(v=>v[0]).filter(v=>has(net,v));if(av.length&&!av.includes(view[net])){view[net]=av[0];st.key=""}
   _rv();document.querySelectorAll("#views [data-view]").forEach(b=>{if(!av.includes(b.dataset.view))b.remove()});document.getElementById("views").hidden=av.length<2};
 const _rt=renderTop;renderTop=function(){const ns=Object.keys(NETS).filter(n=>cnt(n)>0);if(ns.length&&!ns.includes(net))net=ns[0];
   _rt();document.querySelectorAll("#nets [data-net]").forEach(b=>{if(!ns.includes(b.dataset.net))b.remove()});document.getElementById("nets").classList.toggle("solo",ns.length<2)};
 renderAll()})();'''
s=s[:i]+boot+s[j:]
s=s.replace('setStatus("Carregando a prévia…");','')
nome=perfil.get("nome") or perfil.get("usuario") or slug
s=s.replace('<title>{ger} Prévia</title>','')
payload=json.dumps(data,ensure_ascii=False).replace("</","<\\/")
html=f'''<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow,noarchive"><title>{{ger}} Prévia · {nome}</title>
<style>*,*::before,*::after{{box-sizing:border-box}}html{{-webkit-text-size-adjust:100%}}body{{margin:0}}</style>
<style>.side{{display:none!important}}.layout{{grid-template-columns:minmax(0,1fr)!important;justify-items:center}}.stage{{position:static!important}}.statmark{{display:none!important}}.stage{{width:auto!important;max-width:100%}}.vtabs[hidden]{{display:none!important}}.wa-bg .pv-dl{{width:max-content;max-width:90%;margin:10px auto 6px;border-radius:99px;padding:5px 12px;box-shadow:0 1px 1px rgb(0 0 0/.08)}}.pv-week{{width:100%;display:flex;flex-direction:column;align-items:center;gap:6px}}.pv-week{{max-width:440px}}.pv-all{{width:100%;height:42px;border-radius:12px;border:1px solid var(--line);background:var(--surface);color:var(--fg);font:700 14px/1 var(--font);cursor:pointer;display:flex;align-items:center;justify-content:center;gap:8px;transition:background .15s,border-color .15s}}.pv-all span{{font-weight:600;color:var(--muted)}}.pv-all[aria-pressed=true]{{background:var(--yellow);border-color:var(--yellow);color:#111}}.pv-all[aria-pressed=true] span{{color:#111;opacity:.75}}.pv-days{{display:grid;grid-template-columns:repeat(7,minmax(0,1fr));gap:6px;width:100%;padding-top:4px}}.pvd{{min-width:0;height:60px;border-radius:12px;border:1px solid var(--line);background:var(--surface);color:var(--fg);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;cursor:pointer;position:relative;font:inherit;padding:0;transition:background .15s,border-color .15s,color .15s}}.pvd small{{font-size:10px;font-weight:700;letter-spacing:.06em;color:var(--muted)}}.pvd b{{font-size:18px;font-weight:800;line-height:1.1}}.pvd i{{position:absolute;top:-6px;right:-5px;min-width:17px;height:17px;border-radius:99px;background:var(--ink);color:var(--yellow);font:800 10px/17px var(--font);font-style:normal;text-align:center;padding:0 4px;box-shadow:0 0 0 2px var(--bg)}}.pvd i:empty{{min-width:9px;width:9px;height:9px;top:-3px;right:-2px;padding:0;background:var(--yellow)}}.pvd:hover:not(:disabled){{border-color:var(--fg)}}.pvd[aria-pressed=true]{{background:var(--yellow);border-color:var(--yellow);color:#111}}.pvd[aria-pressed=true] small{{color:#111;opacity:.7}}.pvd[aria-pressed=true] i:empty{{background:#111}}.pvd:disabled{{opacity:.35;cursor:default}}.pv-items{{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;max-width:100%}}.pvi{{border:1px solid var(--line);background:var(--surface);color:var(--fg);border-radius:99px;padding:6px 12px;font:600 12.5px/1.2 var(--font);cursor:pointer}}.pvi b{{font-weight:800}}.pvi:hover{{border-color:var(--fg)}}.pvi[aria-pressed=true]{{background:var(--brand-soft);border-color:var(--yellow);color:var(--fg)}}.pv-hint{{margin:0;font-size:13px;color:var(--muted);text-align:center}}.pv-hint b{{color:var(--fg)}}.pv-dl{{display:flex;align-items:center;gap:6px;background:var(--yellow);color:#111;font:700 12.5px/1.2 var(--font);padding:8px 14px;letter-spacing:.01em}}.pv-dl::before{{content:'';width:7px;height:7px;border-radius:50%;background:#111;flex:none}}.li-post+.pv-dl,.fb-post+.pv-dl,.ig-post+.pv-dl{{margin-top:10px}}.pv-dl.ov{{position:absolute;left:12px;top:100px;z-index:31;border-radius:99px;padding:6px 12px;box-shadow:0 2px 8px rgb(0 0 0/.3)}}.hbar{{flex-wrap:nowrap!important;gap:16px!important;padding-block:18px 16px!important;align-items:center!important}}.hbar .brand small{{display:none}}.pv-meta{{display:flex;flex-direction:column;gap:3px;padding-left:16px;border-left:1px solid #3a3a3a;min-width:0}}.pv-meta b{{color:var(--band-fg);font-size:16px;font-weight:700;line-height:1.2;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}.pv-meta em{{font-style:normal;color:var(--yellow);font-size:13.5px;font-weight:700;line-height:1.25}}.pv-meta span{{color:var(--band-muted);font-size:12.5px;font-weight:500;line-height:1.35;display:block}}.pv-meta i{{width:6px;height:6px;border-radius:50%;background:var(--yellow);display:inline-block;vertical-align:2px;margin-right:7px}}nav.solo{{display:none!important}}.phone.auto{{height:auto!important;min-height:0!important}}.phone.auto .scr{{position:relative;inset:auto;overflow:visible}}.phone.auto .sb,.phone.auto .ig-top,.phone.auto .li-top,.phone.auto .fb-top,.phone.auto .igp-tabs{{position:relative!important;top:auto!important}}</style>
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
