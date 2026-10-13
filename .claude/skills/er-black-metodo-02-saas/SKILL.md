---
name: er-black-metodo-02-saas
description: Use ao clonar SaaS thin-client por ER (6 fases).
---

# ER BLACK · Método 02 — SaaS thin-client (cérebro na nuvem)

Quando usar: alvo de **Categoria C** — produto web/app onde quase toda lógica vive no servidor (ex.: Granola, Suno-like, apps de transcrição/resumo). Objetivo: **corpo clonado + contrato da API 100% extraído + cérebro reimplementado com peças open-source**, 100% funcional e sem mensalidade.

Fonte canônica (copy-paste pronto, não reescrever):
`KIT-ER-METODO-02-SAAS/` — 11 arquivos, **100% no validador**.
Prompt mestre: `00-PROMPT-MESTRE.md` (PRIMEIRA mensagem; operador só entrega `NOME_DO_APP` + `CAMINHO_LOCAL`).
Padrão: `PADRAO-KIT-ER.md` · Taxonomia A–E: `ER-BLACK-TAXONOMIA.md` · Validador: `VALIDAR-KIT.py`.
Revalidar: `python3 VALIDAR-KIT.py --todas` → 100% nos 2 kits.

## A verdade estrutural (dita ANTES de tudo)

A ER recupera o **corpo** (front/instalador). O **cérebro** (servidor + modelos) NÃO está no artefato.
O que se extrai do cliente é o **CONTRATO**: endpoints, shapes request/response, **prompts de sistema**, tipos.
**Não persiga "copiar o servidor". Persiga: contrato 100% + núcleo reimplementado com lógica real.**

## Pipeline — Fase 0 (setup) + 6 fases, ordem estrita

| Fase | Arquivo | Objetivo | Ferramentas-chave | Entregável |
|---|---|---|---|---|
| 0 | `01-SETUP-INSTALACAO.md` | stack + disco medido + **`REQUISITOS-BACKEND.md`** (contas que o operador cria: Supabase, DeepSeek, Groq, Google Cloud) + **`.env.example`** (SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, DEEPSEEK_API_KEY, GROQ_API_KEY, GOOGLE_CLIENT_ID/SECRET/REFRESH_TOKEN, DATABASE_URL, JWT_SECRET) — nada de Fase 4 sem contas prontas | mitmproxy, Frida, asar/apktool, Python, Node | versões verificadas |
| 1 | `02-FASE-CORPO.md` | clonar o corpo — **REUSA o Método 01** (extrair, rebrandar, smoke test) | kit 01 | `front-clonado\` |
| 2 | `03-FASE-CONTRATO.md` | **o coração**: todo endpoint, todo shape, todo prompt de sistema | mitmproxy + Frida (unpinning), GraphQL introspection, WS/SSE, `.proto` | `02-contrato.md` + `contrato/` |
| 3 | `04-FASE-CLASSIFICAR.md` | separar **🟢 núcleo** (faz pagar) × **🟡 útil** × **🔴 perfumaria** | régua do valor (2 perguntas: sem ele o produto funciona? / entrega o valor central?) | `03-classificar.md` |
| 4 | `05-FASE-CEREBRO.md` | reimplementar o cérebro com lógica REAL no núcleo | FastAPI + Supabase + Whisper + DeepSeek + pgvector | `backend\` |
| 5 | `06-FASE-CONECTAR.md` | ligar front clonado no backend novo, núcleo ponta-a-ponta | troca de base URL + shapes | `05-conectar.md` |
| 6 | `07-FASE-VALIDAR.md` | paridade de contrato byte a byte + **3+ funções novas** | harness de contrato | `06-validar.md` + `07-checklist-final.md` |

## Stack de reconstrução do cérebro

| Camada | Peça |
|---|---|
| API | **FastAPI** (Python) |
| Auth + DB | **Supabase** (Postgres + Auth + pgvector) |
| Transcrição | **Whisper / faster-whisper / Groq** |
| Resumo / IA / chat | **DeepSeek / Ollama / Groq** |
| Busca semântica | **pgvector + sentence-transformers** |
| Fila de jobs | FastAPI BackgroundTasks ou Celery + Redis |

### Fase 4 — ordem das fatias (vertical: uma ponta-a-ponta antes da próxima)

AUTH (login/JWT/refresh/perfil) → NOTAS (CRUD no shape exato) → TRANSCRIÇÃO (áudio → Whisper/Groq) → IA (resumo/action items/título usando o **prompt de sistema extraído**) → BUSCA SEMÂNTICA (embedding + pgvector) → CALENDÁRIO (Google sync com refresh_token) → PERFUMARIA (stubs 200 + log).

**Prova obrigatória da Fase 4 (colar saída):** teste de contrato por endpoint do núcleo (shape casa 100%), fluxo ponta-a-ponta (login → criar → transcrever → resumir → buscar) e teste de erro (vazio/nulo/gigante → shape de erro esperado). "Compilou" não conta — teste não rodado não conta.

## Regras de ouro

1. **Contrato primeiro, cérebro depois** — sem contrato completo, construir o backend é chute.
2. **Todo endpoint classificado** — stub só na **🔴 perfumaria**: devolve **200 com shape válido** (nunca 404/500, para não disparar error boundary) **e loga a chamada**; núcleo (🟢) é lógica real, sempre.
3. **Shape validado contra o consumidor real** — o front dita o formato; se o front reclama, o shape está errado, não o front.
4. **`REQUISITOS-BACKEND.md` ANTES de construir** — lista do backend lida e aprovada antes de escrever código.
5. **Backend escuta `127.0.0.1`, nunca `0.0.0.0`** — é clone local, não servidor público.
6. **Prompts de sistema = o ativo mais valioso** — cada prompt extraído vira arquivo em `prompts-extraidos\`, com o endpoint de origem anotado.
7. **Interceptar só o SEU tráfego, no SEU login** — sem dado de terceiro, sem endpoint de outra conta.
8. **Rebrand obrigatório** — nome, ícone, cores, textos. Clone 1:1 de marca é problema; identidade própria + uma coisa melhor que o original.

## GATE DE SEGURANÇA — antes de declarar qualquer fase pronta

```
- [ ] sha256 do original + de todo artefato gerado (00-hashes.txt)
- [ ] contrato cobre 100% dos endpoints observados, com shape validado
- [ ] cada endpoint tem classificação (núcleo/útil/perfumaria) e justificativa
- [ ] núcleo implementado com lógica REAL (nenhum stub no que faz pagar)
- [ ] prompts de sistema extraídos e arquivados com origem
- [ ] backend em 127.0.0.1; nada exposto na rede
- [ ] prova colada: pedido (comando/request) + resposta bruta + artefato
```
Item aberto = fase NÃO fecha.

Severidade: **CRÍTICA** = núcleo em stub (o clone "abre" mas não entrega o valor) / shape divergente que quebra o front · **ALTA** = endpoint não mapeado em caminho funcional · **MÉDIA** = divergência periférica sem prova · **BAIXA** = higiene.

## Taxonomia do alvo (a régua que decide o método)

| Cat | Tipo | O que dá pra fazer |
|---|---|---|
| A | 100% local (exe/dll/asar/apk) | reconstrução total — Método 01 |
| B | local com serviços online pontuais | Método 01 + interceptar os pontuais |
| **C** | **thin-client SaaS (lógica na nuvem)** | **este método** — corpo + contrato + cérebro próprio |
| D | web pesado no cliente (bundle grande) | desempacotar bundle → tratar como A/B |
| E | server-rendered/blindado (sem cliente) | só observação externa — não é ER BLACK |

Caso-âncora: **Granola → AnotaAí** (transcrição + resumo + busca semântica: Whisper + LLM + pgvector).

## Arsenal e artefatos

- **Varredura do código (Fase 2)**: `rg -o "https?://[^\"' ]+"` (URLs), `rg -o "/(api|v1|graphql)/[\w/\-]+"` (rotas), `rg -n "fetch\(|axios|\.get\(|\.post\("` (call sites) → agrupar por **subdomínio = família/microsserviço**.
- **Rede**: mitmproxy (HTTP/HTTPS), Wireshark; **pin/unpinning com Frida** quando o cliente não deixa interceptar.
- **Contrato**: OpenAPI/`openapi.json`, GraphQL introspection, mensagens WS/SSE, `.proto` para gRPC, pretty-print do bundle pra achar as chamadas.
- **Saída**: `ER-OUTPUT\00-hashes.txt · 01-corpo.md · 02-contrato.md · 03-classificar.md · 04-cerebro.md · 05-conectar.md · 06-validar.md · 07-checklist-final.md · prompts-extraidos\ · contrato\ · backend\ · front-clonado\`.

## Pitfalls

- Ir para o backend sem contrato completo → reimplementação inventada; o front recusa os shapes.
- Deixar o núcleo em stub e "entregar depois" → o produto não faz o que o usuário paga pra fazer; o gate reprova.
- Assumir que o servidor está no cliente → perda de tempo; no thin-client ele nunca está.
- Backend em `0.0.0.0` → clone exposto na rede local sem necessidade.
- Copiar marca/textos literais → problema de marca; rebrand é etapa, não detalhe.
- Testar só "abre a tela" → paridade é comportamento de contrato (mesma request → mesmo shape/efeito), não tela bonita.

## Relação com as outras skills

- Fase 1 REUSA `er-black-metodo-01-local` (mesma disciplina de cópia, sha256 e prova).
- `engenharia-reversa-produto` = modo público/interface para aula e reconstrução com identidade própria; **não misturar** com o modo binário do ER BLACK no mesmo material.
