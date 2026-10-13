# 🔍 ER BLACK — Engenharia Reversa Completa

> Taxonomia da "clonabilidade" por engenharia reversa + método para reconstruir o cérebro de apps SaaS.
> Criado por MAX para Kendy · 2026-10-12

---

## A Régua: quanto do produto está DENTRO do artefato vs. FORA (servidor/modelo)

Quanto mais do valor está no binário que você tem, mais a ER recupera. Quanto mais está no servidor/modelo, menos.

---

## 🟢 Categoria A — 100% local, autocontido (cérebro NO binário)

Toda a lógica roda no dispositivo. Sem servidor, sem conta obrigatória.

**Exemplos famosos:**
- Aplicativos clássicos: **WinRAR, 7-Zip, VLC, IrfanView, Paint.NET, KeePass** (gestor de senha local).
- Jogos offline: **Doom, Stardew Valley, Terraria** (single-player).
- Editores: **Sublime Text (parcial), Notepad++**, **Obsidian** (núcleo local).
- Ferramentas: **HandBrake, OBS (núcleo), qBittorrent**, **DBeaver**.

**ER consegue:** ~100% da lógica. Decompila → reconstroi → funciona.
**Nota:** mesmo aqui, apps comerciais têm ofuscação e licença — a lógica está lá, mas "ler" já é mais difícil (Categoria A opacas, tipo Photoshop).

---

## 🟢 Categoria B — Local + dados locais (cérebro + dados NO binário/disco)

Lógica local, mas com comportamento dependente de modelo local/arquivos.

**Exemplos famosos:**
- **Obsidian** (com plugins), **Logseq**, **Zettlr** (notas locais).
- **Joplin** (sem sync cloud), **Standard Notes** (offline).
- **Audacity**, **GIMP** (com plugins).
- Jogos com save/engine local: **Minecraft (jar), Factorio, RimWorld**.
- **Plex Media Server** (núcleo self-host, mas tem nuvem opcional).

**ER consegue:** 100% da lógica + formato de dados + engine.

---

## 🟡 Categoria C — Thin client de SaaS (corpo local, cérebro NA NUVEM)

O app é uma casca: manda dados pro servidor, renderiza resposta. Sincronização/inferência no servidor.

**Exemplos famosos:**
- **Granola / AnotaAí** ← caso do Kendy (assistente de reuniões).
- **Notion** (app desktop é thin client), **Todoist**, **Trello**, **Slack**, **Discord**.
- **Spotify** (cliente baixa, mas recomendação/busca no servidor).
- **Dropbox/Google Drive** (cliente é só sync; lógica de dedup/indexing no servidor).
- **Zoom/Meet** (cliente pesado, mas transcrição/gravação/IA no servidor).
- **1Password online**, **Canva** (editor é local, mas assets/IA na nuvem).
- **Grammarly** (front local, cérebro de linguagem no servidor).

**ER consegue:** cliente inteiro + **contrato** (endpoints, shapes, prompts). ❌ lógica do servidor.
**Resultado:** clone do corpo ✅, cérebro ❌ → reimplementar backend.

---

## 🔴 Categoria D — Cérebro remoto puro / SSE / streaming de render

Quase nada no cliente; até a UI vem do servidor. Cliente = navegador/streaming fino.

**Exemplos famosos:**
- Apps web server-rendered: **Gmail (UI lógica server), Google Docs (collab engine server-side), Figma (multiuser realtime no servidor), Word online**.
- Streaming de jogo: **GeForce Now, Xbox Cloud Gaming, PlayStation Now** (o jogo roda lá, só vídeo chega).
- **ChatGPT web** (o modelo roda no datacenter; teu browser só exibe).
- **Midjourney, DALL·E** (imagem gerada no servidor).
- APIs puras: **Stripe, Twilio, OpenWeather** (sem cliente offline).

**ER consegue:** só o comportamento observável via rede (MITM captura request/response). Nada de código.
**Resultado:** reproduz comportamento, nunca o código/cérebro.

---

## ⚫ Categoria E — Cérebro em modelo de IA proprietário

O "segredo" é um LLM/modelo ML que **nem o dono tem como código** — são pesos + infraestrutura.

**Exemplos famosos:**
- **A transcrição/IA da Granola, Otter.ai, Fireflies.ai, Fathom** (resumo de reunião).
- **O GPT-4o do ChatGPT, o Claude, o Gemini** — o modelo em si.
- **DeepL, Google Translate** (modelo de tradução).
- **Recomendação do YouTube/TikTok/Netflix** (modelo de ranking).
- **Reconhecimento de imagem do Google Photos**.
- **O Codex/GitHub Copilot** (o modelo de código).

**ER consegue:** nada do modelo. No máximo o **prompt de sistema** (se vazar no bundle) + contrato entrada/saída.
**Resultado:** não se copia — **se substitui** por outro modelo (DeepSeek, Whisper, Llama...).

---

## Resumo visual

| Categoria | Cérebro onde? | ER recupera? | Exemplo-âncora |
|-----------|---------------|--------------|----------------|
| A — local puro | no binário | ✅ 100% | VLC, Doom, KeePass |
| B — local + dados | no disco/binário | ✅ 100% | Obsidian, Minecraft, GIMP |
| C — thin-client SaaS | na nuvem | ⚠️ só corpo + contrato | Granola, Notion, Slack, Spotify |
| D — remoto puro | servidor (render/state) | ❌ só comportamento | Figma, GeForce Now, ChatGPT web |
| E — modelo IA | nos pesos | ❌ substituir, não copiar | Otter, DeepL, ranking TikTok |

---

## O take para o AnotaAí

O **AnotaAí** é **C + E**: corpo (Electron) clonável ✅, mas o valor central
(transcrição + resumo por IA) é cérebro em nuvem **e** em modelo proprietário.
Por isso o clone "parece igual mas não funciona".

**Caminho eficiente:** clona o corpo (feito) + extrai o contrato (mapeado) +
substitui o cérebro por peças open-source (Whisper p/ transcrição +
DeepSeek/Ollama p/ resumo + pgvector p/ busca).

---

## 🧩 Reconstruir o backend após a ER — peças prontas (auto-host, sem mensalidade)

### 🧠 IA / Modelos (substituem o cérebro proprietário)
| Função | Ferramenta | Custo |
|--------|-----------|-------|
| Transcrição de áudio | **Whisper** (open-source, local) / **whisper.cpp** / **faster-whisper** | Gratuito (GPU) |
| Transcrição cloud barata | **Groq** (Whisper-Large-v3) | ~centavos |
| Resumo, action items, chat | **DeepSeek**, **Ollama** (Llama/Qwen local), **Groq**, **OpenRouter** | Local grátis → centavos |
| Embeddings (busca semântica) | **sentence-transformers** (local) ou `text-embedding-3` | Grátis/barato |
| TTS (fala) | **XTTS / Bark / Kokoro** | Grátis local |

### 🗄️ Infra / Backend (auto-host, sem mensalidade)
| Peça | Ferramenta |
|------|-----------|
| Banco + auth | **Supabase** (Postgres + Auth + pgvector) |
| Busca semântica | **pgvector** (no Supabase) ou **Qdrant**/Weaviate |
| Orquestração/agente | **n8n**, LangChain/LlamaIndex |
| Backend API | FastAPI |
| Fila de jobs de transcrição | **Celery** + Redis, ou FastAPI background |

### 🔍 Repositórios open-source que fazem 80% do "cérebro" do Granola
- **OpenMeeting / MeetingBot** — transcrição + resumo de reuniões.
- **RealtimeSTT / Whisper + LLM** — pipeline audio→texto→resumo.
- **Hoarder / Rewind-style** — nota/busca semântica local.
- **khoj / RAG self-host** — busca + chat sobre tuas notas.

**Receita final:** teu front (clonado) + FastAPI (teu) + Whisper (transcrição) +
DeepSeek/Ollama (cérebro) + Supabase/pgvector (memória) = Granola teu, 100% seu, sem mensalidade.
