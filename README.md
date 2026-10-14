# ER BLACK · Engenharia Reversa de verdade, para o seu agente

O método completo de engenharia reversa, empacotado para o seu agente de IA executar sozinho.
Você entrega **dois dados** e ele faz o resto: reconhece, desempacota, decompila, reconstrói,
testa clicando, limpa a identidade e devolve o app **rodando**.

Não é "entendi como funciona". É o app de volta, funcionando, com paridade provada.

```
NOME_DO_APP .......... o app que você quer reconstruir
CAMINHO_LOCAL ........ onde ele está na sua máquina
```

É isso. O agente lê o prompt mestre, instala o arsenal, executa as fases na ordem e só entrega
quando estiver 100% certo.

O método é longo e agente novo costuma morrer no meio pedindo permissão. Por isso o repositório
traz duas peças a mais: `EXECUTAR-TUDO.md` (a mensagem que faz o agente rodar as 12 fases sem
parar) e `SEM-TRAVA/` (o gate que tira a hesitação do agente antes do método começar).

**Comece pelos dois prompts numerados:** `PROMPT-01-INSTALAR.md` (baixa o repositório, instala o
arsenal e prova cada ferramenta) e `PROMPT-02-EXECUTAR.md` (roda o método inteiro sozinho, com os
dois dados preenchidos).

---

## Descrição completa

**O que é.** Um repositório de método, não de código alheio. Dentro dele estão os dois kits de
trabalho que transformam o seu agente de IA num engenheiro reverso que termina o serviço: um para
app que roda na sua máquina, outro para sistema que só tem o cliente na máquina e o cérebro no
servidor.

**O que ele faz na prática.** Você aponta o app e a pasta. O agente classifica o alvo, copia para
uma pasta de trabalho (o original fica intocado, com sha256 registrado), instala o arsenal e prova
vida em cada ferramenta, reconhece a arquitetura, limpa a identidade do original, desempacota o
código, decompila, cataloga os achados com prova, reconstrói o clone e valida a
paridade medindo tela por tela. Cada fase entrega artefato no disco, não resumo de conversa.

**O que sai no final.** Clone rodando com identidade nova, relatório com números medidos, tabela de
uso de cada ferramenta instalada e as lacunas declaradas com o que foi tentado. Mais o portão de
entrega fechado: paridade provada e teste clicando feito.

**O que você precisa ter.** Um agente de IA com execução de shell (Claude Code, Codex, Cursor,
Hermes, ou chat com ferramenta de código ligada) e o app alvo na sua máquina. O arsenal é
instalado pela fase 1, com prova de vida de cada ferramenta. Medido em Windows 10 e 11.

**Para quem é.** Quem precisa entender um app por dentro e devolver ele funcionando: estudo,
migração, auditoria do próprio software, reconstrução do que você mesmo escreveu e perdeu, aula,
consultoria.

**Para quem não é.** Quem quer sair rodando clone de app de terceiro sem entender nada. O método
cobra cópia, prova e relatório em cada fase, e o alvo é sempre a sua cópia.

**O que não tem aqui.** Nenhum projeto de terceiro, nenhum binário de app alheio, nenhum alvo.
Só o método, o gate e o portão.

**Caso real medido.** App Electron de cerca de 200 MB, com o código empacotado, rodando as fases do
kit 01: o clone abriu por dentro, em modo demonstração, sem tela de login, e a identidade do
original saiu limpa. O caminho inteiro está nas fases do kit.

---

## O que tem dentro

| Caminho | O que é | Resultado |
|---|---|---|
| `PROMPT-01-INSTALAR.md` | O primeiro prompt: instala o repositório e as ferramentas | máquina armada, arsenal provado |
| `PROMPT-02-EXECUTAR.md` | O segundo prompt: roda o método sozinho, do começo ao fim | clone rodando, portão fechado |
| `KIT-ER-METODO-01-LOCAL/` | Reconstrução de app **100% local** (exe, dll, asar, apk, jar, .NET). Cérebro mora no binário | clone rodando, sem identidade do original |
| `KIT-ER-METODO-02-SAAS/` | Reconstrução de **SaaS thin-client** (Telas + API por baixo) | corpo, contrato e cérebro mapeados, cliente funcionando |
| `MÉTODO-1-ER-CATEGORIA-A-B.md` | O método por trás do Kit 01 | leitura de estudo |
| `MÉTODO-2-ER-CATEGORIA-C-SAAS.md` | O método por trás do Kit 02 | leitura de estudo |
| `ER-BLACK-TAXONOMIA.md` | As 5 categorias de alvo (A a E) e o que muda em cada uma | escolher a rota certa |
| `PADRAO-KIT-ER.md` | O padrão que os dois kits seguem | entender a anatomia da fase |
| `VALIDAR-KIT.py` | Portão que mede o kit item por item | `100%` ou a lista do que falta |
| `.claude/skills/` | Os dois métodos em formato de skill (Claude Code e afins) | instalação sem copiar e colar |
| `EXECUTAR-TUDO.md` | A mensagem que manda o agente rodar as 12 fases sem parar | execução de ponta a ponta |
| `SEM-TRAVA/` | O gate que tira a hesitação do agente, mais o medidor de modelo | agente que não para na fase 3 |
| `.claude/commands/er-black.md` | Comando `/er-black` para Claude Code | um comando roda tudo |

---

## Como instalar no seu agente

### 1. Qualquer IA com shell (Claude, ChatGPT, DeepSeek, Qwen, Codex...)

1. Abra `KIT-ER-METODO-01-LOCAL/00-PROMPT-MESTRE.md` (ou o 02, para SaaS).
2. **Cole o arquivo inteiro** como **primeira** mensagem.
3. Ele vai pedir `NOME_DO_APP` e `CAMINHO_LOCAL`. Responda só isso.
4. Não faça mais nada. O agente segue as fases sozinho.

### 2. Agente que roda na pasta (Claude Code, Codex, Cursor, Aider)

```bash
git clone https://github.com/gabrielkendy/reverse-engineer-black.git
cd reverse-engineer-black
```

Abra o agente **dentro dessa pasta**. Ele lê o `AGENTS.md` e as skills de `.claude/skills/`,
e já entra sabendo o método, as regras duras e o portão de entrega.

### 3. Agente com pasta de skills (Hermes e afins)

```bash
cp -r .claude/skills/* ~/caminho/das/suas/skills/
```

As duas skills (`er-black-metodo-01-local` e `er-black-metodo-02-saas`) carregam sob demanda.

---

## O agente executa as 12 fases sem parar

Método longo mais agente novo é igual a agente pedindo permissão na fase 3. As três peças que
resolvem já estão no repositório:

1. **`SEM-TRAVA/AXION-MATRIZ.txt`** · o gate. Vai antes de tudo, no lugar onde o seu agente lê a
   identidade dele. Instalação por agente em `SEM-TRAVA/INSTALAR-NO-AGENTE.md`.
2. **`EXECUTAR-TUDO.md`** · a mensagem única com os dois dados preenchidos. Cole como primeira
   mensagem e não responda mais nada até o clone abrir.
3. **`SEM-TRAVA/TESTADOR.py`** · mede qualquer modelo em qualquer endpoint compatível com OpenAI e
   diz quantos pedidos ele entrega de fato. A linha dura vem do modelo, não do prompt: quem trava, troca.

No Claude Code já vem pronto como comando:

```
/er-black <nome-do-app> <pasta-do-alvo>
```

---

## As regras que o método não deixa passar

- **Lei do arsenal.** Ferramenta nunca é removida, só acrescentada com justificativa
  (nome, motivo, alvo, o que fica impossível sem ela), e **toda** ferramenta instalada tem
  que ser usada, com o comando exato e o resultado na tabela de uso. Arsenal não encolhe, ele se especializa.
- **Cópia, nunca o original.** Trabalho começa em cópia isolada, com sha256 do alvo registrado.
- **Fato não é inferência.** O que não foi alcançado vira **lacuna** declarada com "tentei X, Y, Z".
- **Achado sem prova não entra.** Pedido, resposta e print, sempre.
- **Paridade é medida.** Mesma entrada, mesmo comportamento, byte a byte quando é o caso.
- **Teste clicando.** O clone é aberto, clicado e conferido, não só compilado.

---

## Validar o pacote

```bash
python3 VALIDAR-KIT.py --todas
```

Saída esperada:

```
2 KITs. Nota de cada:

  100%  ####################  KIT-ER-METODO-02-SAAS
  100%  ####################  KIT-ER-METODO-01-LOCAL
```

O portão só lê. Nunca escreve, nunca move, nunca apaga. Se um dia der menos de 100%,
ele diz exatamente qual âncora caiu.

---

## Estado da verificação · 13/10/2026

| Medição | Resultado |
|---|---|
| `VALIDAR-KIT.py --todas` rodando dentro do repositório | **100%** nos dois kits |
| Arquivos versionados | 62, nenhum binário de terceiro |
| Gate publicado | byte a byte o original, md5 `9c224d43a8c36bb5a046255c2a4be62e` |
| Caminho de máquina do autor dentro do repositório | nenhum |

O portão só lê. Nunca escreve, nunca move, nunca apaga. Se um dia der menos de 100%, ele diz
exatamente qual âncora caiu.

---

## Licença

MIT. Use, adapte, ensine, venda o que você construir com ele.

Feito por **Gabriel Kendy** · [agenciabase.tech](https://agenciabase.tech)
