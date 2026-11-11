# Como gerar ou atualizar a prévia de um cliente

Este repositório publica, pelo GitHub Pages, as prévias de conteúdo da {ger}.
Endereço de cada cliente: https://gervmkt.github.io/previas/<slug>/

O pedido nasce no Simulador {ger} (artefato https://claude.ai/artifact/4TJj2TpXvoJLXboLjYv97H),
no botão "Compartilhar" de cada perfil. Ele grava um documento na coleção `compartilhamentos`
do banco do artefato, com o id do perfil como id do documento.

## Passo a passo (para o Claude)

Progresso: o simulador mostra uma barra de progresso lendo o campo `etapa` do pedido. Atualize esse campo
(ArtifactData `update` em `compartilhamentos/<id>`, só o campo `etapa`) ao começar cada fase:
`lendo` (passos 1 a 3), `midias` (passo 4), `montando` (passo 5), `publicando` (passo 6), `site` (junto com o passo 7).

1. Leia o pedido: ArtifactData `get`, url do simulador, collection `compartilhamentos`, doc_id = id do perfil.
   Campos: `redes` (ig, li, tt, fb), `filtro` (todos | aprov | emaprov), `slug`, `perfil`.
   Se não houver id no pedido, liste `compartilhamentos` e trate todos com `status` "gerando" ou "manual".
2. Leia o perfil: ArtifactData `get`, collection `perfis`, doc_id = id do perfil. Salve o objeto `data` em `work/perfil.json` (acrescente `"id"`).
3. Leia os posts do perfil: ArtifactData `query`, collection `posts`, query.where = [["perfil","==","<id>"]], com `out_dir` = `work/raw`.
   Copie os arquivos de `work/raw/posts/*.json` para `work/posts/`.
   Se o pedido tiver `periodo`, só entram posts cuja `data` (AAAA-MM-DD…) esteja entre `periodo.ini` e `periodo.fim`, inclusive.
4. Baixe as mídias: para cada `a` em `midias[]` e `capa` dos posts que vão entrar, e para `perfil.foto`,
   use o Artifact `read` com a url do simulador e `path` = o id (uma chamada por id). Copie cada arquivo salvo para `work/media/`.
   Só baixe as mídias dos posts que passam no filtro e nas redes do pedido.
5. Gere: `python3 _build/make_static.py <slug> work/perfil.json work/posts <redes,separadas,por,virgula> <filtro> work/media . <periodo.ini> <periodo.fim>`
   (os dois últimos só se o pedido tiver `periodo` com `ini` e `fim`, no formato AAAA-MM-DD; sem período, omita).
   (rode na raiz do repositório; ele cria ou substitui a pasta `<slug>/`). Antes, apague `<slug>/` se já existir, para não sobrar mídia antiga.
6. `git add -A && git commit -m "Prévia <slug>" && git push`. Não commite a pasta `work/`.
7. Avise o simulador: ArtifactData `update` em `compartilhamentos/<id>` com
   `previaUrl` = "https://gervmkt.github.io/previas/<slug>/?v=<AAAAMMDDHHMM do momento, em UTC>" (o `?v=` força o navegador do cliente a buscar a versão nova), `atualizadoEm` = agora em ISO 8601 (UTC), `status` = "pronto", `erro` = "".
   Se algo falhar, grave `status` = "erro", `erro` = motivo curto em português, `erroEm` = agora.

Regras: não mexa em outras pastas de clientes. Nunca coloque `notas` dos posts na prévia (o make_static já remove).
