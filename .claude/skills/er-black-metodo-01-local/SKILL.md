---
name: er-black-metodo-01-local
description: Use ao reconstruir app local por ER (6 fases).
---

# ER BLACK · Método 01 — App local (cérebro no binário)

Quando usar: "faz engenharia reversa desse app", "quero o fonte desse exe", "reconstrói esse app pra mim", alvo de Categoria A/B (100% local: exe/dll/asar/apk/jar/.NET). Objetivo: entregar o app **reconstruído 100% funcional**, com paridade provada, não um "entendi como funciona".

Fonte canônica (copy-paste pronto, não reescrever):
`KIT-ER-METODO-01-LOCAL/` — 12 arquivos, **100% no validador**.
Prompt mestre: `00-PROMPT-MESTRE.md` — **ULTRA, autossuficiente (19,5 KB, 328 linhas)**. Colar INTEIRO como primeira mensagem; a IA responde pedindo `NOME_DO_APP` + `CAMINHO_LOCAL` e daí executa **SOZINHA** as 7 fases sem parar. Blocos internos: FASE 0 arsenal inteiro com prova de vida · FASE 2.5 limpeza de identidade (clone nasce inventado) · FASE 6 TESTE CLICANDO (checklist de 13 cliques, print + resultado) · FASE 7 limpeza de código + RETESTE · PORTÃO DE ENTREGA · DECLARAÇÃO DE ENTREGA com números reais · PINTA VERMELHA · "o que não fazer". Depois vem o comando pronto "EXECUTE AUTOMÁTICO, DO INÍCIO AO FIM, SEM PARAR" (operador troca 2 valores) + tabela de fallback por fase isolada + os 3 scripts. Mestre antigo (9,3 KB) guardado em `_BACKUP-PROMPTS-20261012/` (guardado local, nao sobe).
**LEI DO ARSENAL (ordem do dono, 12/10/2026):** PROIBIDO remover ferramenta · ADICIONAR exige justificativa em 4 campos (FERRAMENTA/MOTIVO/ALVO/SEM ELA) · USO OBRIGATÓRIO de todas com tabela de uso no relatório · PERFORMANCE MÁXIMA em cada uma · ferramenta que falha é CONSERTADA, nunca removida. Arsenal só cresce.
Padrão das fases: `PADRAO-KIT-ER.md` · Taxonomia A–E: `ER-BLACK-TAXONOMIA.md` · Validador: `VALIDAR-KIT.py`.
Revalidar depois de mexer: `python3 VALIDAR-KIT.py --todas` → tem que dar 100% nos 2 kits (10 âncoras).

## Pipeline — Fase 0 (setup) + 6 fases, ordem estrita

| Fase | Arquivo | Objetivo | Ferramentas-chave | Entregável |
|---|---|---|---|---|
| 0 | `01-SETUP-INSTALACAO.md` | arsenal INTEIRO instalado + prova de vida + tabela de uso (nunca remover ferramenta) | os 10 grupos do `FERRAMENTAS-REF.md` | `ER-OUTPUT/00-ARSENAL.md` |
| 1 | `02-FASE-RECONHECIMENTO.md` | formato, arquitetura, linguagem, proteção, categoria + sha256 | DIE, strings, `rabin2`, `file` | `01-reconhecimento.md` |
| 2 | `03-FASE-DESEMPACOTAR.md` | tirar packer/ofuscação (UPX, asar, apk, dll) | upx, Scylla+x64dbg, apktool, `@electron/asar` | `02-desempacotar.md` |
| 2.5 | `02b-FASE-LIMPEZA-IDENTIDADE.md` | clone nasce inventado: nome, autor, URL, ícone, logo | `scripts/limpar-total.py` | `ER-LIMPEZA/*` |
| 3 | `04-FASE-DECOMPILAR.md` | código legível, 100% das funções endereçadas | Ghidra, IDA, jadx, dnSpy/ILSpy, CFR, decompyle3/pycdc | `03-decompilar.md` + `src/` |
| 4 | `05-FASE-ANALISE-AVANCADA.md` | caminhos difíceis e checksums | angr, Triton, Z3, Miasm, Qiling/Unicorn, HyperDbg | `04-analise-avancada.md` |
| 5 | `06-FASE-RECONSTRUIR.md` | reescrever 100% mantendo comportamento exato | IA + diff de paridade | `05-reconstruir.md` |
| 6 | `07-FASE-VALIDAR.md` | paridade — mesma entrada → mesma saída (10+ casos; GUI + CLI/headless) | harness de teste | `06-validar.md` + `07-checklist-final.md` |

## Fase 2.5 — LIMPEZA DE IDENTIDADE (automatizada em 12/10/2026)

Clone com marca do dono **não é clone entregável**. Três scripts no kit fazem isso sozinhos,
determinístico (mesma pasta → mesmo nome inventado, roda de novo e não muda):

| Script | O que faz |
|---|---|
| `scripts/limpar-identidade.py` | nome, autor (string OU objeto), url, copyright, appId, productName, description, telemetria, versão (preserva forma x.y.z) |
| `scripts/limpar-logo.py` | acha imagem de marca (por nome E por pasta icon/logo/brand), GERA ícone novo (PNG na mão + ICO 7 tamanhos), troca, reescreve apontamento no manifest |
| `scripts/limpar-total.py` | roda as duas com o MESMO nome + relatório único (`00-resumo.json`, `01-relatorio.md`, `02-mapa.json`, `03-pendencias.md`, `04-icones.md`) |

Uso: `python scripts/limpar-total.py "PASTA_DO_CLONE" [--nome X] [--dry]` — SEMPRE `--dry` primeiro.

**Regras duras medidas (cada uma custou erro real):**
- **NUNCA renomear arquivo de código.** `content-index.js` → `Maryra-index.js` quebra `require`. Nome de arquivo é ESTRUTURA. Só renomeia o que o usuário VÊ (exe, atalho, pasta de topo).
- **Regex de `author` tem que cobrir objeto E string.** `"author":{"name":...}` não casa com `("author"\s*:\s*")`. Errar aqui deixou `"name": "maryra"` em vez do autor inventado.
- **Nunca regex de palavra solta** (`segment`, `sentry`, `host`) — come código legítimo. Telemetria se troca por HOST/URL/DSN, nunca por palavra isolada.
- **Versão: preservar a FORMA `x.y.z`.** Trocar o miolo às cegas deu `"0.2.25"` → `"0.0.8.16"`.
- **`main`/entry point nunca se toca** — verificar no fim que `"main": "src/main/main.js"` continua igual.
- **Grep obrigatório depois:** identidade original em TEXTO tem que dar **ZERO**. Na 1ª rodada séria sobreviveram 8 pontos: crédito de autor (`Crafted by Gabriel Kendy · @gabrielkendy.ia · www.agenciabase.tech`), `title:` da BrowserWindow, prefixo técnico (`.arte-viva-write-test-`), e texto em pt-BR citando o produto. Todos viraram regra.
- **Binário que carrega a marca vai pra PENDÊNCIA**, não se finge limpo. Aqui sobraram `icon.png` (antes) e `build/Release/safe_fs.node` — `.node` só sai com patch de string na fase de binário.
- Nada de logo, ícone ou fonte do PC do operador. O ícone é GERADO (geometria pura, cor derivada de hash da pasta+nome).

Disco: subset Windows-nativo ≈ 8–10 GB · stack completa (nativo+.NET+Android+Electron+rede) ≈ 18–25 GB. Avisar o operador do disco antes de instalar.

## Regras de ouro (valem do início ao fim)

1. **SEMPRE em cópia.** Nunca reverter/tocar o binário original. `sha256` do alvo ANTES e de todo artefato gerado, salvo em `ER-OUTPUT\00-hashes.txt`.
2. **FATO ≠ INFERÊNCIA ≠ LACUNA.** LACUNA é ÚLTIMO recurso: só depois de esgotar Fase 4.
3. **Lacuna sem justificativa é proibida.** Formato obrigatório: "tentei X, Y, Z e falhou por [motivo técnico]".
4. **Paridade = idêntico, não parecido.** Mesma entrada → mesma saída, byte a byte.
5. **Nada de caminho absoluto** da máquina do operador no código reescrito. Relativo.
6. **Binário suspeito roda só em isolamento** (VM/QEMU/qiling/HyperDbg), nunca no host.
7. **Persistir em disco por fase** em `ER-OUTPUT\`. Nunca segurar tudo na conversa.
8. **Entregar 100%, nunca casca:** binário roda, paridade provada, revisão e testes rodados.

## Regra da prova (achado sem a tríade NÃO entra)

```
PEDIDO     o comando/input exato que rodou
RESPOSTA   a saída bruta, literal, colada
ARTEFATO   print, dump, hash, diff, arquivo gerado
```
Função "reconstruída" sem diff + teste de paridade = PROMESSA. Não conseguiu provar? Escrever "nao provado" + o que tentou.

Severidade com critério (nunca opinião): **CRÍTICA** = comportamento errado / quebra outro componente / proteção ativa não neutralizada (clone se auto-invalida) · **ALTA** = paridade quebrada em caminho funcional · **MÉDIA** = divergência periférica sem prova · **BAIXA** = higiene.

## GATE DE SEGURANÇA — roda ANTES de cada fase ser declarada pronta (colar o resultado)

```
- [ ] sha256 do original salvo ANTES de qualquer escrita
- [ ] todo artefato gerado tem hash registrado (00-hashes.txt atualizado)
- [ ] nenhum caminho absoluto da máquina no código reconstruído
- [ ] toda função reconstruída tem paridade testada
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] binário suspeito só rodou em isolamento (VM/qiling/HyperDbg), nunca no host
- [ ] a prova foi colada (pedido + resposta + artefato)
```
Item aberto = fase NÃO fecha. Correção primeiro, "feito" depois.

## Arsenal que separa clone real de amador

| Amador | Nível certo |
|---|---|
| descompila e "entende" | reconstrói e PROVA paridade (mesma entrada → mesma saída) |
| marca "impossível" e pula | esgota angr/Triton/Z3/HyperDbg e documenta cada tentativa |
| desativa checksum (o clone morre) | reconstrói o algoritmo e gera o valor íntegro |
| roda no host | isola em VM/qiling/HyperDbg |
| chumba caminho absoluto | relativo, rodou em outra máquina |
| nomeia função por chute | binding-diff (Diaphora/BinDiff) nomeia de graça |

Extras que economizam horas: **inteligência de alvo primeiro** (versão, CVE, writeup, base open-source) · **SMC** = detectar e dumpar pós-decriptação · quando parecer impossível, **trocar de abordagem** (estática → simbólica → dinâmica → emulação → devirtualização).

## Estrutura de saída

```
ER-OUTPUT\
  00-hashes.txt · 01-reconhecimento.md · 02-desempacotar.md · 03-decompilar.md
  04-analise-avancada.md · 05-reconstruir.md · 06-validar.md
  07-checklist-final.md · 00-ARSENAL.md · src\
```

## Pitfalls (erros que já custaram retrabalho)

- **LEIA ESTA SEÇÃO ANTES DE REMONTAR PACOTE (regra dura, custou 2 pacotes queimados em 12/10/2026).** Os dois erros abaixo já estavam escritos nesta skill e foram repetidos de memória, sem reler. Antes de remontar o pacote (fora das fases do método): (1) reler os pitfalls; (2) **caracterizar o asar bom primeiro** — `asar list <bom> | sort > /tmp/bom.txt` + `wc -l` (referência: **970 entradas, ~18,6 MB** neste alvo), `grep -E '\.node$'` para achar os nativos, `find app.asar.unpacked -type f` para contar os desempacotados (2); (3) só então empacotar e comparar contagem entradas-a-entradas com `diff`. **Entrada a menos ou tamanho fora da faixa = pacote ruim, não descobrir com o app quebrado na tela do operador.** Foi exatamente isso que aconteceu: 6,3 MB e o banner vermelho, depois 2 rodadas de bancada.
- **Alvo Electron real (executado no Windows, 12/10/2026 — Content Hub 0.2.25, 806/806 arquivos idênticos):** o código do app vive em `resources/app.asar`; `npx @electron/asar extract` devolve tudo legível (aqui: 14.593 linhas, zero ofuscação). Diff por `sha256` arquivo a arquivo é a prova válida — o hash do `app.asar` reconstruído é SEMPRE diferente (empacotamento novo), o conteúdo é que conta.
- **`unpack` ≠ `unpackDir` (medido no código do @electron/asar, 12/10/2026).** `unpackDir` recebe o **DIRETÓRIO** do arquivo (`path.relative(src, path.dirname(filename))` → `isUnpackedDir`): só marca PASTA inteira. `unpack` recebe o **ARQUIVO** com `minimatch(filename, padrão, {matchBase:true})` → é o certo pra `.node`. Usar `unpack: '*.node'`. Errar aqui quebra o app: `unpackDir: '{**/*.node,node_modules/better-sqlite3/**}'` joga o pacote inteiro pro `.unpacked` (asar cai de 16,5 MB pra 6,6 MB) e o app abre com diálogo de erro JavaScript. Sinal de pacote certo: ~16,5 MB + `.unpacked` com os 2 `.node`.
- **Não assumir em que pasta vive o nativo:** neste alvo o `safe_fs.node` estava DENTRO do asar e o `better-sqlite3` fora (com stub dentro). Conferir com `asar list` no original antes de remontar o pacote.
- **Shell MSYS + node:** passar caminho `/c/...` pro node quebra; usar `C:/Users/...` ou `cd` antes. E `tasklist | grep` precisa de `MSYS_NO_PATHCONV=1` quando há argumento com barra.
- Declarar função reconstruída sem diff + teste de paridade → é promessa; o gate reprova.
- Neutralizar checksum pela metade → o clone se auto-invalida em runtime (o pior caso: parece pronto).
- Marcar lacuna como "impossível" sem esgotar as técnicas → renúncia, não engenharia.
- Rodar suspeito no host → vira máquina comprometida; isolamento não é opcional.
- Entregar sem rodar o validador/checklist → 10 âncoras abertas = kit "prompt numa fila".

## Fase 6 na prática — provar que o clone ABRE (Content Hub 0.2.25, 12/10/2026)

- **Tela vermelha "Falha ao iniciar" + lista vazia ≠ problema de pacote.** Antes de mexer no pacote, ler o log: `Error occurred in handler for '...'` aponta o arquivo. Aqui a causa era **dado**, não binário: `content-schema.js` usa `/^---\n.../ ` (só LF) e rejeita CRLF, e `YAML.parse` rejeita valor iniciado por `@` (`handle: @gabrielkendy`). Um arquivo ruim derruba a LISTA INTEIRA porque `listProfiles` usa `.map()` sem try/catch.
- **Conserto de classe (no clone):** normalizar quebras (`split(CR+LF).join(LF).split(CR).join(LF)`, `CR`/`LF` via `String.fromCharCode`) e citar valor iniciado por reservado (`[@`]`) antes do `YAML.parse`. Os dois juntos: lista volta, zero erro de handler.
- **Autoteste por flag (prova sem clique e sem CDP):** acrescentar no `main.js` um bloco sob `--teste-modal` que faz `webContents.executeJavaScript(fs.readFileSync(script))` no `did-finish-load` e imprime `AUTOTESTE-JSON:{...}`. O script testa abrir/fechar cada modal e devolve `{erros, passos, travado}`.
- **`--remote-debugging-port` FUNCIONA (revalidado 12/10/2026, Content Hub 0.2.25, 3 rodadas limpas).** O pitfall antigo ("recusa conexão") estava errado no geral. Regras medidas: (a) funciona em **processo novo**, com `--remote-allow-origins=http://127.0.0.1:<porta>`; (b) falha sempre que **já existe instância viva** — `requestSingleInstanceLock` mata a nova e a antiga (sem a flag) fica, então a porta nunca abre; matar TODAS antes (`taskkill /F /IM "<app>.exe"`) e conferir `tasklist | grep -ic` = 0; (c) o processo morre quando o `cmd` que o lançou termina → lançar **na mesma execução** do teste (Python `subprocess.Popen` + esperar a porta + medir), nunca depender de processo sobrevivente entre chamadas do terminal. Bônus: `Page.captureScreenshot` por CDP dá o print da tela sem `computer_use` nem PrintWindow.
- **Provar tela sem depender do driver de UI:** `computer_use` neste host só enxerga o desktop (não as janelas). Usar `PrintWindow` via `ctypes`+PIL no hwnd da janela e ler o PNG.
- **Janela abre minimizada** (posição `-25600,-25600`) → o operador diz "não abre". Chamar `ShowWindow(hwnd, SW_RESTORE)` + `SetForegroundWindow` antes de capturar.
- **Lançar pelo terminal do Hermes:** em foreground o filho morre quando o comando termina. Usar background. `cmd.exe /c ""App.exe" > log"` quebra o quoting — rodar o `.exe` direto.
- **`patch`/`write_file` convertem `\n` literal em quebra de linha REAL** dentro de regex/comentário → o patch grava a regex partida em duas linhas e o arquivo para de compilar. Nunca escrever `\r\n` assim: usar `String.fromCharCode(13)` / `(10)`, ou editar por script Python.
- **Caminho `/c/...` para o python/node nativos do MSYS vira `C:\c\...`** e o arquivo "some" (foi pra `C:\c\Users\...`). Sempre passar `C:/Users/...`.

## Trocar a identidade do clone (nome próprio, sem brigar com o original)

Renomear só o `.exe` não basta. O que separa os dois apps:
1. `package.json`: `name` (define o **userData**) e `productName` (define o nome do app).
2. `title` na `BrowserWindow` (`main.js`) e `<title>` no `index.html`.
3. **Copiar o userData antigo pro novo** (`AppData\Roaming\-nome-antigo-` → `...\-nome-novo-`): é onde vivem licença (`license.json` + `device-secret.json`) e config do workspace. Sem copiar, o clone renasce sem licença e sem workspace.
4. `unpacked`/asar/`.bat`/atalho seguem o nome novo. userData compartilhado com o original causa conflito de instância única (um derruba o outro).

### Duas cópias do clone, mesmo userData = armadilha silenciosa (medido 12/10/2026)

Se ficarem **duas pastas do clone** (ex.: `work\clone-build` = a boa, e uma tentativa anterior também renomeada pra `Arte Viva Hub.exe`), as duas brigam pelo MESMO userData (`AppData\Roaming\Arte Viva Hub`) e portanto pelo mesmo *single-instance lock*:

- A cópia que subiu primeiro **toma o lock**; a outra **sobe e sai com código 0 em segundos**, sem erro, sem log, sem janela. Sintoma enganoso: `Start-Process` retorna, `-PassThru` mostra `saiu=True codigo=0`, e nenhum processo fica. Parece "o pacote está quebrado" e NÃO está.
- Pior: você olha a janela na tela e jura que é a sua cópia. **Sempre medir a pasta de origem**: `Get-CimInstance Win32_Process -Filter "Name='<exe>'" | Select ProcessId,ExecutablePath`. Nome de janela igual nas duas não prova nada.
- Contenção (reversível, sem apagar nada): renomear o `.exe` da cópia errada (`mv "App.exe" "NAO-USAR-App.exe.bak"`). Ela para de subir e de disputar o lock na hora. Avisar o operador e não apagar sem ordem.
- Como o app fica vivo depois que o assistente sai: lançar **desacoplado** (`powershell Start-Process -FilePath ... -WorkingDirectory ...`), ou melhor ainda deixar o **atalho do Desktop** pro operador clicar (pai = Explorer). Rodar o `.exe` pelo terminal em background **morre** quando o Hermes limpa o processo; em foreground morre no fim do comando (ou no `timeout`).
- Ao caçar quem relança uma cópia velha: `Get-CimInstance Win32_Process | Where CommandLine -like '*<pasta>*'` mostra a árvore. Filtrar também pega **falso positivo dos próprios comandos de busca** (o padrão digitado aparece no CommandLine deles). Os pais podem já estar mortos (app órfão) — aí a contenção por renome é o caminho, não a caça.

## Modo demo — abrir o clone POR DENTRO sem tocar em identidade (13/10/2026)

Pedido típico: "quero ver o app por dentro, com conteúdo real, sem mexer em mais nada".
Alvo: Content Hub 0.2.25 / clone Maryra. O app valida licença contra API e cifra
o estado com DPAPI — **não existe senha no instalador**, então "preencher login de
fora" é impossível. O caminho é uma flag `--demo` lida pelo PRÓPRIO processo.

### Os DOIS votos que o app exige (e onde estão)

```
main.js L1262:   if (boot.unlocked) { app completo } else { só login }
                   ^ decidido por licenseService.bootValidate()
main.js L68:     isLicensed() -> licenseService.isUnlocked()
createWindow():  rendererPage = isLicensed() ? 'index.html' : 'license.html'
                   ^ decidido por isUnlocked()
```

**Precisa dos dois.** Só `isUnlocked()` → a UI até aparece, mas o app cai no ramo
`else`, `WORKSPACE_ROOT` fica `null`, nada indexa e a tela mostra
"Falha ao iniciar". Só `bootValidate()` → a pasta resolve e o watcher sobe, mas a
janela carrega `license.html`. Patch final (no `license-service.js`):

```js
// 1) bootValidate()   -> app completo
    let state;
    if (process.argv.includes('--demo')) return { unlocked: true, reason: 'demo' };
// 2) isUnlocked()     -> janela certa
    if(process.argv.includes('--demo'))return true;/*           catch { return false; }*/
```

O `/*` do patch 2 é injetado ANTES do `catch` seguinte, para engolir o
`try{...}catch{...}` original inteiro num comentário (o `return` acontece antes).

### Trava dura: o header do asar NÃO pode mudar de tamanho

`json.dumps` reescreve o header sem os campos `unpacked`/`executable` e sem os
separadores originais — encolhe ~1.6 KB e o Electron responde
**`Failed to parse header` / `Invalid package`**. Regra medida: **offset fixo,
header intocado, arquivo final com EXATAMENTE o mesmo número de bytes**.

Técnica que funciona: o patch ocupa espaço e o excesso é compensado tirando
**1 espaço de indentação por linha, do FIM do arquivo para o começo**. Nunca
apagar comentário nem código — apagar um `// ... }` que explicava um bloco deixou
um `catch` órfão e o app abriu com `Unexpected token 'catch'`.

### Armadilhas medidas (cada uma custou uma rodada)

- **`orig.replace(ANCORA, PATCH, 1)` pega a PRIMEIRA ocorrência.** Havia **3**
  chamadas de `bootValidate()` (handler `license:retry`, caminho `--Maryra-render`,
  boot real). Use `orig.rindex(ANCORA)` — o boot real do `whenReady` é o ÚLTIMO.
- **CRLF importa.** O original tem 1.297 `\r\n`; gravar com `\n` dá 1.297 bytes de
  diferença e quebra a troca. Ler os bytes DO ASAR e reinserir — nunca text-mode.
- **Provou-se com log dentro do próprio app:** injetar
  `fs.writeFileSync('.../boot-log.txt', JSON.stringify({argv: process.argv, ...}))`
  na linha do patch. Foi assim que se viu `{"has":true,"unlockedAntes":false}` —
  o `--demo` chegava e o boot rodava. Sem esse log, duas horas de chute.
- **O `--demo` precisa vir depois de `--`:** `./app.exe -- --demo`. Sem o `--`,
  o Chromium come a flag (`bad option: --demo`). `process.argv` fica
  `[exe, '--', '--demo']` e o `includes('--demo')` funciona.
- **`licensedAppStarted`** (main.js L1030): se já for `true`, `startLicensedApp()`
  sai na primeira linha com `loadRendererPage('index.html')` e NUNCA chama
  `resolveWorkspaceRoot()`.

### Pasta de conteúdo + entrada direta

1. Apontar o workspace: gravar `AppData\Roaming\<NomeDoPacote>\workspace.json`
   com `{"workspaceRoot": "..."}`. **Gravar com `json.dump`**, não por heredoc —
   `\\` do heredoc vira `\` e o app diz
   `Ignoring unreadable workspace.json: Bad escaped character`.
2. Sem workspace definido, o app abre o **diálogo nativo de pasta** no primeiro
   boot. Com o `workspace.json` já gravado, ele entra direto na grade.
3. Pasta de conteúdo real para popular a tela: copiar
   `content/projects/<projeto>/...` do app original (a estrutura é
   `content/projects/<p>/campaigns/<c>/items/<i>/variants/<v>/` com `index.html`
   + `assets/`). Aqui: 393 arquivos / 180 imagens → sidebar com 23 peças.
4. Atalho `.bat` na raiz do projeto: `%~dp0` já é a raiz (o `..` sobrava e
   procurava em `Documents\work\...`). Conteúdo: `start "" "%APP%" -- --demo`.
   Sem `--demo` o app abre normal, na tela de login — a flag é o único interruptor.

### Checklist de prova (o que o dono vê)

- Título da janela muda de `Maryra - Entrar` para **`Maryra`**.
- Log: `Loading renderer: ...index.html` (não `license.html`) **e**
  `Workspace root: <pasta>` **e** `[watcher] Watching ...`.
- Tela: sidebar com contagem de peças, indicador verde **"Live … watching"**,
  grade com miniaturas reais, rodapé da identidade inventada.

## Relação com as outras skills

- `engenharia-reversa-produto` = modo público/interface (linha dura: não descompilar; para aula/YouTube e reconstrução com identidade própria). **ER BLACK é o modo binário** — objetivo diferente, não misturar os dois discursos no mesmo material.
- Método 02 (`er-black-metodo-02-saas`) = alvo web/thin-client; a Fase 1 dele REUSA este método.
