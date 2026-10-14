# 🧼 FASE 2.5 — LIMPEZA DE IDENTIDADE (o clone nasce inventado)

> Cole DEPOIS de desempacotar (Fase 2) e ANTES de reconstruir (Fase 5).
> É etapa própria porque tem regra dura: **o clone não pode carregar NENHUM resquício
> de identidade do original** — nem nome, nem logo, nem ícone, nem autor, nem URL.

---

```
FASE 2.5 — LIMPEZA DE IDENTIDADE (automática, com prova)

Você é o LIMPADOR. O clone desempacotado na Fase 2 ainda carrega a marca do dono
original. Aqui você apaga essa marca e põe uma IDENTIDADE INVENTADA, gerada por
script. Nada do computador do operador entra — nada de nome real, nada de logo,
nada de ícone do PC. Tudo nasce inventado pela máquina.

═══════════════════════════════════════════════════════════════
REGRA DURA (a razão desta fase existir)
═══════════════════════════════════════════════════════════════
1. PROIBIDO o clone manter QUALQUER identidade do original: nome do produto,
   nome do autor, e-mail, site, copyright, appId, ícone, logo, splash, tray,
   imagem de marca, nome de executável, nome de atalho, título de janela.
2. Se o script não souber julgar, ele NEUTRALIZA. Nunca "deixa passar".
3. O que ele não resolve, ele LISTA em pendencias. Pendência não tratada
   significa clone NÃO ENTREGÁVEL.
4. Ferramenta que falha NÃO é removida: você conserta a ferramenta.
5. Uso OBRIGATÓRIO das duas ferramentas desta fase. Uma sem a outra deixa
   metade da marca viva (texto sem ícone, ou ícone sem texto).

═══════════════════════════════════════════════════════════════
O QUE ESTA FASE FAZ, EM TRÊS FRENTES
═══════════════════════════════════════════════════════════════
FRENTE 1 — IDENTIDADE DE TEXTO  (`scripts/limpar-identidade.py`)
  Troca, em TODOS os arquivos de texto do clone:
    · nome do produto (Content Hub, Content Studio, slug, PascalCase, tudo)
    · autor, nome do autor, e-mail do autor
    · URL do site, endpoint de API do produto
    · copyright (ano + titular)
    · appId, productName, executableName, homepage, description
    · DSN/chave de telemetria (Sentry, PostHog, Segment)
    · versão (troca o miolo e PRESERVA a forma "x.y.z")
  Preserva o que é ESTRUTURA:
    · `main`, entry points, require/import, nomes de arquivo de código
  Backup de cada arquivo tocado em `ER-LIMPEZA/_antes/`.

FRENTE 2 — LOGO, ÍCONE E NOME VISÍVEL  (`scripts/limpar-logo.py`)
  · Acha TODA imagem de marca (.ico .icns .png .svg .jpg) — por nome do arquivo
    E por pasta (icon/, logo/, brand/, assets/)
  · GERA um ícone novo, inventado, sem depender de nada externo
    (PNG desenhado na mão + ICO multi-tamanho: 16/24/32/48/64/128/256)
  · Troca no lugar, com backup em `ER-LIMPEZA/_antes-icones/`
  · Reescreve o apontamento de ícone no manifest para `build/icon.ico`
  · Lista os nomes VISÍVEIS (executável, atalho, desinstalador)

FRENTE 3 — ORQUESTRAÇÃO  (`scripts/limpar-total.py`)
  Roda as duas em sequência com o MESMO nome inventado e produz:
    · `ER-LIMPEZA/00-resumo.json`
    · `ER-LIMPEZA/01-relatorio.md`
    · `ER-LIMPEZA/02-mapa.json`       (de → para, arroba por arroba)
    · `ER-LIMPEZA/03-pendencias.md`   (o que exige olho humano)
    · `ER-LIMPEZA/04-icones.md`

═══════════════════════════════════════════════════════════════
EXECUÇÃO
═══════════════════════════════════════════════════════════════
1. SEMPRE em cópia de trabalho nomeada. NUNCA no original.
2. Simulação primeiro (não grava nada), para ler o que vai acontecer:
      python scripts/limpar-total.py "CAMINHO_DO_CLONE" --nome "NOME_INVENTADO" --dry
3. Leia a amostra de trocas. Se algo estiver errado, NÃO rode de verdade:
   conserte o script antes. Troca errada é pior que troca faltando.
4. Rode de verdade:
      python scripts/limpar-total.py "CAMINHO_DO_CLONE" --nome "NOME_INVENTADO"
5. Confira o `package.json` na tela e compare com o backup.
6. Abra `ER-LIMPEZA/03-pendencias.md` e trate cada item.

═══════════════════════════════════════════════════════════════
COMO O NOME INVENTADO É GERADO (não use nome real)
═══════════════════════════════════════════════════════════════
O script inventa a partir de uma semente determinística (hash da pasta + 2). Nada
de aleatório solto: rodar de novo dá o MESMO nome, então o clone é reproduzível.
Deriva dele: nome curto, slug npm, pacote reverso (com.x.y), autor, URL, versão.

Se o operador quiser um nome específico, passe `--nome`. Se não, deixe o script
inventar — é mais seguro que escolher na mão e vazar preferência pessoal.

═══════════════════════════════════════════════════════════════
VERIFICAÇÃO OBRIGATÓRIA (sem isso a fase está incompleta)
═══════════════════════════════════════════════════════════════
Depois da limpeza, GREP no clone inteiro pela identidade do original. Tem que
dar ZERO. Rode e mostre o resultado:
    grep -ri "content-hub\|content studio\|agenciabase\|getlayers" CLONE --exclude-dir=ER-LIMPEZA
    grep -ri "NOMEDOAUTOR_ORIGINAL\|emailoriginal" CLONE --exclude-dir=ER-LIMPEZA
Zero resultado = fase OK. Qualquer linha = volta e conserta a regra que faltou.

Confirme:
"LIMPEZA OK. [N] trocas de texto, [M] ícones trocados, [P] pendências.
 Grep da identidade original: zero ocorrências."

═══════════════════════════════════════════════════════════════
O QUE NÃO FAZER
═══════════════════════════════════════════════════════════════
- NÃO renomear arquivo de código. (Quebra require/import; o app não abre.)
  Nome de arquivo é ESTRUTURA. Só renomeia o que o usuário VÊ.
- NÃO apagar a palavra "segment" ou "sentry" solta no código. (Mata variável
  legítima. Telemetria se troca por HOST/URL, nunca por palavra isolada.)
- NÃO usar logo, ícone ou fonte do PC do operador. Tudo inventado.
- NÃO entregar clone com pendência aberta. Trate ou documente o motivo.
- NÃO pular este arquivo porque "o nome já mudou": ícone e logo continuam vivos
  mesmo quando o texto já está trocado.

═══════════════════════════════════════════════════════════════
VERIFICAÇÃO NA TELA (não dá para automatizar)
═══════════════════════════════════════════════════════════════
Depois de reconstruir (Fase 5), rode o app a partir do código e confira:
  [ ] Ícone na barra de tarefas
  [ ] Ícone no canto da janela
  [ ] Título da janela
  [ ] Nome no Gerenciador de Tarefas
  [ ] Nome no atalho / menu Iniciar
  [ ] Ícone e nome no instalador
  [ ] Tela "Sobre" / rodapé
  [ ] Splash screen, se houver
  [ ] Ícone da bandeja (tray), se houver
Item não conferido na tela = fase não terminada.


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do artefato desta fase registrado em ER-OUTPUT\00-hashes.txt
- [ ] o script rodou em SIMULAÇÃO (--dry) antes de gravar, com a amostra lida
- [ ] backup dos originais existe em ER-LIMPEZA\_antes\ e _antes-icones\
- [ ] a verificação obrigatória de grep rodou: ZERO ocorrência da identidade original em TEXTO
- [ ] o binário que ainda carrega a marca foi LISTADO como pendência (não fingiu limpar)
- [ ] `main` / entry point / require intactos (o app ainda abre)
- [ ] versão preservou a forma x.y.z (não virou 0.0.8.16)
- [ ] nenhum caminho absoluto da máquina do operador no que foi gerado
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
Se um item falhar, corrija e rode o gate de novo. Não declare a fase pronta antes
de todos os itens verdes.

DECLARAÇÃO DE FIM DE FASE (imprima literalmente)
"LIMPEZA OK. [N] trocas de texto, [M] ícones trocados, [P] pendências.
 Grep da identidade original: zero ocorrências."

⛔ PINTA VERMELHA — se marcar QUALQUER item abaixo, o trabalho para aqui:
- [ ] clone ainda tem nome, ícone, logo ou autor do original
- [ ] app não abre mais depois da limpeza
- [ ] usei logo/ícone/fonte do meu computador em vez de gerar inventado
- [ ] entreguei com pendência aberta e não documentei o motivo
```
