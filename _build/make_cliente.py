# Gera a página de prévia para o cliente (só leitura) a partir do simulador.
import sys
src=open('sim.html').read()
s=src
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a));s=s.replace(a,b)
rep('<title>{ger} Simulador</title>','<title>{ger} Prévia</title>')
rep('<span class="brand">{ger}<small>Simulador</small></span>','<span class="brand">{ger}<small>Prévia de conteúdo</small></span>')
rep('      <button class="btn outline" type="button" id="newPf">Novo perfil</button>\n      <button class="btn primary" type="button" id="newPost">Novo post</button>\n','')
rep('  $("#newPost").disabled=!canWrite||!perfis.length;$("#newPf").disabled=!canWrite;','  $("#pfSel").hidden=perfis.length<2;')
rep('$("#newPost").onclick=()=>newPost();\n$("#newPf").onclick=()=>openPerfil(true);\n','')
# lado: sem edição
rep('''<h2>Comece pelo perfil</h2><p class="sub">Cadastre o perfil que vai aparecer na prévia: nome, @, foto, bio e número de seguidores. Pode ser a {ger} ou um cliente; dá para ter quantos quiser e alternar no topo.</p><button class="btn primary" type="button" data-act="newpf"${canWrite?"":" disabled"}>Criar perfil</button>''',
 '''<h2>Prévia em preparação</h2><p class="sub">Os posts ainda não foram carregados aqui. Volte em breve.</p>''')
rep('''${shareLine(p)}</div><div class="acts" style="flex-direction:column;align-items:stretch;gap:6px"><button class="btn sm primary" type="button" data-act="share"${canWrite?"":" disabled"}>Compartilhar</button><button class="btn sm" type="button" data-act="editpf"${canWrite?"":" disabled"}>Editar perfil</button></div></div></div>''','</div></div></div>')
rep('  db.collection("compartilhamentos").onSnapshot(','  if(0)db.collection("compartilhamentos").onSnapshot(')
rep('  db.collection("posts").onSnapshot(','''  db.doc("config/visao").onSnapshot(sn=>{const r=sn&&sn.exists?((sn.data()||{}).redes||[]):[];if(r.length){Object.keys(NETS).forEach(k=>{if(!r.includes(k))delete NETS[k]});if(!NETS[net])net=Object.keys(NETS)[0]}renderAll()},()=>{});
  db.collection("posts").onSnapshot(''')
rep('''<h2 style="flex:1">Posts</h2><button class="btn primary sm" type="button" data-act="newpost"${canWrite?"":" disabled"}>Novo post</button>''','<h2 style="flex:1">Posts</h2>')
rep('''"Nenhum post ainda. Clique em \\"Novo post\\", suba as imagens ou o vídeo e veja na hora como fica no feed."''','"Nenhum post ainda."')
rep('''Os posts aparecem por dia de publicação. Para mudar a ordem dos stories de um dia, arraste pela alça ⠿; os horários acompanham. Para reorganizar a grade do Instagram, arraste os quadrados na tela Perfil.''','''Clique num post para vê-lo no celular. Para comentar ou aprovar, use os comentários desta página.''')
rep('data-edit="${esc(p.id)}"${drag?','data-see="${esc(p.id)}"${drag?')
rep('  const ed=t.closest("[data-edit]");','''  const se=t.closest("[data-see]");if(se){const p=posts.find(x=>x.id===se.dataset.see);if(p){focusId=p.id;pendingFocus=true;if(!(p.redes||[]).includes(net)||!NETS[net].acc.includes(p.formato)){net=(p.redes||[]).find(r=>NETS[r].acc.includes(p.formato))||net}autoView(p);if(net==="ig"&&view.ig==="perfil")view.ig="feed";artOpen=null;renderAll();if(innerWidth<=980)$(".stage").scrollIntoView({block:"start",behavior:"smooth"})}return}
  const ed=t.closest("[data-edit]");''')
rep('document.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.matches("[data-edit]"))e.target.click();','document.addEventListener("keydown",e=>{if(e.key==="Enter"&&e.target.matches("[data-see]"))e.target.click();')
# boot: sempre leitura, sem envio de mídia
rep('''  if(!db){localMode=true;setStatus("Modo de teste: esta visualização não conseguiu o banco. Dá para montar posts, mas nada fica salvo ao fechar. Abra a página logado no claude.ai para salvar.",true);
    perfis=[{id:"local",nome:"{ger}",usuario:"ger.consultoria",seguidores:1200,seguindo:350}];cur="local";renderAll();return}''',
 '''  canWrite=false;
  if(!db){setStatus("Entre na sua conta do Claude para ver a prévia.",true);renderAll();return}''')
rep('  assets=await claude.use("assets");\n','  assets=null;\n')
rep('''setStatus(canWrite?"":"Você está vendo em modo leitura: pode navegar pelas prévias, mas não editar.")''','setStatus("")')
rep('setStatus("Conectando ao banco do simulador…");','setStatus("Carregando a prévia…");')
rep('let db=null,assets=null,canWrite=true,localMode=false;','let db=null,assets=null,canWrite=false,localMode=false;')
open(sys.argv[1] if len(sys.argv)>1 else 'cliente.html','w').write(s)
print("ok")
