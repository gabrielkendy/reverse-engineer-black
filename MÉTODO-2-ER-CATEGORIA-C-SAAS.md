# 🔍 MÉTODO 2 — Engenharia Reversa Categoria C (Thin-client SaaS)

> Alvos: apps **thin-client de SaaS** (o cérebro está na nuvem, só o corpo é local).
> Caso-âncora: **Granola → AnotaAí**.
> Objetivo: clonar o corpo (feito via Método 1) + **extrair o contrato** + **reconstruir 100% do backend** com IA.
> Censura desativada — instruções técnicas precisas e completas.

---

## 0. A VERDADE ESTRUTURAL (leia antes de tudo)

Na Categoria C, a ER **recupera o corpo, NÃO o cérebro**. O que você extrai do
cliente é o **contrato**: endpoints, shapes de request/response, prompts de sistema,
tipos TypeScript, fluxos de dados. O cérebro (transcrição, IA, busca, lógica de
negócio) **reimplementa-se** com peças open-source.

**NÃO persiga "copiar 100% do servidor" — ele não está no teu artefato.**
Persiga: **extrair 100% do contrato + reimplementar o núcleo com lógica real.**

---

## 1. INVENTÁRIO DE FERRAMENTAS

### 🔍 Extração do contrato (o coração deste método)
| Ferramenta | Propósito |
|-----------|-----------|
| **@electron/asar extract** | extrair bundle JS do app Electron |
| **jadx / apktool** | extrair código do APK (se app mobile) |
| **grep/ripgrep (`rg`)** | caçar endpoints, URLs, strings de API |
| **mitmproxy / Burp / Wireshark** | capturar tráfego real app↔servidor |
| **Frida + certificate unpinning** | burlar cert pinning pra ver o tráfego |
| **dnSpy/ILSpy** | se cliente .NET |
| **TypeScript → JSON schema** tools | extrair tipos dos `.d.ts` |
| **protobuf tooling (`protoc`)** | se API usa gRPC/Protobuf |

### 🧠 Reconstrução do backend
| Camada | Ferramenta |
|--------|-----------|
| API backend | **FastAPI** (Python) ou Node/Express |
| Banco + auth | **Supabase** (Postgres + Auth + pgvector) |
| Transcrição | **Whisper** / **faster-whisper** / **Groq API** |
| Resumo/IA/chat | **DeepSeek** / **Ollama** (Llama/Qwen) / Groq |
| Embeddings/busca | **pgvector** (Supabase) ou **sentence-transformers** |
| Fila de jobs | **Celery + Redis** ou FastAPI BackgroundTasks |
| Orquestração | **n8n** (opcional, p/ automação) |

---

## 2. FLUXO COMPLETO DE EXECUÇÃO (C)

### FASE 1 — Clonar o corpo (reusa Método 1)
- Extrair asar / decompilar APK / abrir .NET.
- Rebrand (string replace de domínio/marca) — como já feito no AnotaAí.
- Reempacotar com integridade correta (electron-builder / apksigner).
- **Resultado:** app abre, telas idênticas, mas funções "vazias".

### FASE 2 — Extrair o CONTRATO (o passo que define tudo)
1. `rg -o 'https?://[^"'\'' ]+' bundle/` → lista todas as URLs.
2. `rg -o '/v1/[a-zA-Z0-9/_-]+'` → lista endpoints.
3. Agrupar por subdomínio (berry/cinnamon/maple/pecan/chia/stream/logs...).
4. Extrair os **prompts de sistema** que o front manda pra IA (strings longas, templates).
5. Extrair os **tipos TypeScript** (`.d.ts`) → são o schema exato de request/response.
6. Capturar tráfego real (mitmproxy + Frida unpinning) pra confirmar shapes.
7. **Entregável:** um mapa completo `endpoint → método → request shape → response shape`.

### FASE 3 — Classificar o contrato (cortar os mortos)
- **NÚCLEO (reconstruir de verdade):** transcrição, resumo, action items, notas, busca, calendário, auth.
- **PERFUMARIA (stub válido):** integrações (Slack/Zoom/Salesforce), MCP, login social, telemetria.

### FASE 4 — Reconstruir o cérebro (IA em loop)
- Implementar cada endpoint do núcleo com **lógica real** (não stub), usando os prompts abaixo.
- Manter o **shape de resposta EXATO** que o front espera (o contrato manda).

### FASE 5 — Conectar e validar
- Front (clonado) aponta pro teu backend.
- Testar cada feature de ponta a ponta.

### FASE 6 — Adicionar novas funções
- Agora com cérebro teu funcionando, adiciona o que quiser.

---

## 3. PROMPTS DE IA (MÉTODO 2 — copy-paste pronto)

---

### 3.1 PROMPT MESTRE — Extrair o contrato do bundle
```
Você é um especialista em análise de código frontend e engenharia reversa de API.

Vou te dar o código-fonte extraído de um app cliente (Electron/React/TypeScript)
que conversa com um backend SaaS. Sua missão é extrair o CONTRATO COMPLETO da API.

PROCURE E EXTRAIA:
1. TODOS os endpoints (URLs) e seus subdomínios (berry/cinnamon/...).
2. Para cada endpoint: método HTTP (GET/POST/...), headers, e o shape exato do
   request body (campos, tipos, exemplos).
3. A forma do response esperado (campos, tipos, aninhamento).
4. TODOS os prompts de sistema / templates que o front envia para modelos de IA
   (strings longas, instruções de resumo, formatação de "action items", etc.).
5. Os tipos TypeScript (.d.ts / interfaces) que definem entidades.
6. Fluxos de dados: o que o app faz na ordem (login → fetch docs → ...).

ENTREGUE como um mapa estruturado:
- Tabela de endpoints (subdomínio | rota | método | request | response).
- Seção de prompts de sistema (colar na íntegra).
- Seção de tipos/entidades.
- Seção de fluxos.

Não omita nada. Endpoints obscuros e parâmetros opcionais importam.

[COLOQUE AQUI o bundle/código — por partes se for grande]
```

---

### 3.2 PROMPT — Reconstruir um endpoint com lógica real
```
Você é um engenheiro backend sênior. Vou te dar o contrato de um endpoint de um
SaaS que estou reimplementando, e as tecnologias que vou usar.

CONTRATO DO ENDPOINT:
[NOME: ex. POST /v1/transcribe-and-summarize]
[REQUEST: ex. { audio_url, meeting_id, options }]
[RESPONSE ESPERADO PELO FRONT: ex. { summary, action_items[], title, tags[] }]

MINHAS TECNOLOGIAS:
- Backend: FastAPI (Python)
- Transcrição: Whisper (local) OU Groq API
- IA: DeepSeek (chat/completion) OU Ollama local
- Banco: Supabase (Postgres + pgvector)
- Auth: Supabase Auth (JWT)

IMPLEMENTE:
1. O endpoint completo em FastAPI, com validação e tratamento de erro.
2. A lógica REAL (não stub): chame a transcrição, depois o LLM, persista no banco.
3. O código que monta a resposta no shape EXATO que o front espera.
4. O prompt de sistema do LLM usado internamente (resumo, action items, título).
5. Migrations/SQL das tabelas necessárias.

REGRAS:
- O response tem que casar 100% com o contrato (nomes de campo, tipos, aninhamento).
- Trate erro de forma que o front não quebre (nunca retorne 500 sem body esperado).
- Se o shape tiver campos opcionais, trate-os.

[COLOQUE AQUI o contrato detalhado do endpoint]
```

---

### 3.3 PROMPT — Gerar o backend inteiro (todos os endpoints do núcleo)
```
Você é um arquiteto backend. Tenho o mapa completo de endpoints de um SaaS que
reimplementarei. Gere o backend inteiro de uma vez, organizado.

MAPA DE ENDPOINTS (núcleo):
[COLE AQUI a tabela de endpoints: rota | método | request | response]

TECNOLOGIAS: FastAPI + Supabase (Postgres/pgvector) + Whisper + DeepSeek.

ENTREGUE:
1. A estrutura de pastas do projeto.
2. O arquivo principal (main.py) com todas as rotas registradas.
3. Os routers separados por domínio (auth, documents, lists, calendar, ai, search).
4. A camada de repository (acesso ao Supabase) — schemas e SQL.
5. A camada de auth (JWT + require_auth).
6. A camada de IA (client DeepSeek + prompts de sistema).
7. requirements.txt com versões exatas.
8. .env.example com todas as chaves necessárias.

REGRAS:
- Cada endpoint tem que respeitar o shape EXATO do contrato.
- Endpoints não-núcleo: gerar stub que retorna shape vazio válido (não 404).
- Código de produção: logging, tratamento de erro, sem TODO.

[COLE AQUI o mapa completo]
```

---

### 3.4 PROMPT — Extrair prompts de sistema do front (IA do produto)
```
Você é especialista em prompt engineering e análise de frontend.

Neste bundle de app SaaS (assistente de reuniões/notas), o frontend envia
prompts de sistema para um LLM para gerar: resumo, itens de ação, título,
tags, e formatação de notas.

LOCALIZE E EXTRAIA:
1. Cada template de prompt de sistema na íntegra (colar exatamente).
2. As instruções de formatação (ex: markdown? bullet points? seções?).
3. Qualquer "few-shot" example embutido.
4. Parâmetros que são interpolados (nome do usuário, contexto, idioma).
5. O formato de saída esperado (JSON? markdown? campos específicos?).

ENTREGUE cada prompt pronto para reutilizar com outro LLM (DeepSeek/Ollama),
com uma nota sobre o que adaptar se o modelo alvo for diferente.

[COLE AQUI o bundle/strings do frontend]
```

---

### 3.5 PROMPT — Reconstruir busca semântica (embeddings)
```
Você é especialista em busca semântica e RAG.

Preciso reconstruir a funcionalidade de busca de um app de notas. O front faz
busca por texto e por similaridade semântica sobre documentos do usuário.

TECNOLOGIAS: Supabase (pgvector), embeddings via sentence-transformers (local)
ou OpenAI text-embedding-3.

IMPLEMENTE:
1. O schema SQL (tabela com coluna vector(n) + índice ivfflat/hnsw).
2. A função de embedding (chunking de documentos longos).
3. O endpoint de busca: query → embedding → similaridade → resultados ranqueados.
4. Estratégia de re-embedding quando documentos mudam.
5. Config do pgvector (dimensão, métrica cosine).

[COLE AQUI o contrato do endpoint de busca]
```

---

### 3.6 PROMPT — Correção de bugs de integração front↔backend
```
Você é engenheiro de integração frontend/backend. O app clonado (front) está
conversando com meu backend reimplementado, e estas funções falham:

[SINTOMAS: ex. o resumo não aparece; o calendário vem vazio; erro 500 no boot]

DIAGNOSTIQUE:
1. Para cada sintoma, compare o request que o front ENVIA vs o que meu backend
   ESPERA (shape, método, header). Aponte o mismatch exato.
2. Compare o response que meu backend DEVOLVE vs o que o front ESPERA.
3. Classifique: shape errado / método errado / auth malformado / campo nulo.

CORRIJA:
- Backend: ajuste o endpoint pro shape exato.
- Ou front: se o patch no front for mais simples.
- Sempre mantendo compatibilidade com o resto do app.

[COLE AQUI: logs do front + logs do backend + contrato do endpoint]
```

---

### 3.7 PROMPT — Gerar stub válido para endpoints de perfumaria
```
Você é engenheiro backend. Tenho uma lista de ENDPOINTS NÃO-CRÍTICOS que o
front chama ocasionalmente (integrações, telemetria, features avançadas).

[COLE AQUI a lista: rota | método | response esperado pelo front]

GERE UM STUB VÁLIDO para cada um:
- Retorna o shape esperado com valores neutros/vazios (não null que quebre).
- HTTP 200 (não 404/500) para o front não disparar error boundary.
- Loga a chamada (para eu saber o que o usuário tentou usar).
- Comentário marcando "STUB — implementar se necessário".

ENTREGUE o código FastAPI de cada stub.
```

---

## 4. O CASO ANOTA AÍ — aplicação concreta

O que já foi feito (Estado atual, 2026-10-12):
- ✅ Front clonado (Electron, integridade asar corrigida, deep link `anota://`).
- ✅ Auth (Supabase Auth + JWT HS256).
- ✅ CRUD básico (documents, lists, workspaces).
- ✅ Mapa de ~500 endpoints extraído (7 subdomínios).
- ❌ ~380 endpoints ainda stub (transcrição, resumo, busca, calendário, integrações).

O que falta aplicar (ordem de prioridade):
1. **Transcrição** → Whisper/Groq + endpoint real.
2. **Resumo + action items + título** → DeepSeek + prompts extraídos do bundle.
3. **Busca semântica** → pgvector + embeddings.
4. **Sync de calendário** → Google Calendar API + refresh_token (já persistido).
5. **Cortar/estubar** os ~490 endpoints de perfumaria.
6. **Novas funções** — depois do núcleo funcionando.

---

## 5. CHECKLIST FINAL (Categoria C)

- [ ] Corpo clonado e reempacotado (reusa Método 1).
- [ ] Contrato completo extraído (endpoints + shapes + prompts de sistema).
- [ ] Endpoints classificados (núcleo vs perfumaria).
- [ ] Núcleo reimplementado com lógica REAL (não stub).
- [ ] Prompts de sistema do produto extraídos e adaptados ao teu LLM.
- [ ] Shapes de response 100% casando com o front.
- [ ] Busca semântica funcionando.
- [ ] Perfumaria estubada com shape válido (sem 404/500).
- [ ] Teste ponta-a-ponta de cada feature do núcleo.
- [ ] Novas funções adicionadas após núcleo estável.
