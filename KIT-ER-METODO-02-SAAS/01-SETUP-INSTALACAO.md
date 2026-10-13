# 🛠️ FASE 0 — SETUP COMPLETO (Método 02 — SaaS thin-client)

---

```
FASE 0 — SETUP COMPLETO (ambiente de ER + reconstrução de backend)

Instale e configure TODO o ambiente. Breve na parte de ER (você só precisa extrair
o cliente) e completo na parte de backend (onde o cérebro nasce).

─────────────────────────────────────────────────────────────
BLOCO A — PYTHON + malha de ER (reusa do Método 01)
─────────────────────────────────────────────────────────────
1. Python 3.11+ →  winget install Python.Python.3.11
2. python -m venv ER-OUTPUT\venv  +  activate
3. Extração de cliente:
   pip install frida-tools pefile lief
   npm install -g @electron/asar
   winget install --id horsicq.Detect-It-Easy
4. Rede (capturar contrato):
   winget install --id mitmproxy.mitmproxy
   winget install --id WiresharkFoundation.Wireshark
5. Busca em código (o essencial aqui):
   winget install --id BurntSushi.ripgrep.MSVC

─────────────────────────────────────────────────────────────
BLOCO B — BACKEND (a reconstrução do cérebro)
─────────────────────────────────────────────────────────────
6. FastAPI + stack web:
   pip install "fastapi[all]" uvicorn[standard] pydantic[email] httpx asyncpg
7. Supabase (auth + Postgres + pgvector):
   pip install supabase
   (ou Postgres local via Docker:  winget install Docker.DockerDesktop)
8. Transcrição:
   pip install faster-whisper          (CPU)
   OU pip install groq                   (API — rápida, sem GPU)
9. IA / LLM:
   pip install openai                    (DeepSeek usa endpoint OpenAI-compatible)
   OU instalar Ollama local:  winget install Ollama.Ollama
10. Busca semântica:
   pip install sentence-transformers pgvector
11. Fila de jobs (opcional):  pip install celery redis

─────────────────────────────────────────────────────────────
BLOCO C — INSTRUA O USUÁRIO SOBRE FERRAMENTAS E CONTAS DO BACKEND
─────────────────────────────────────────────────────────────
⚠️ REGRA OBRIGATÓRIA DESTA FASE: você NÃO começa a Fase 4 (cérebro) antes de
   entregar ao usuário uma lista CLARA do que ele precisa providenciar. Backend
   sem conta/chave não sobe. Você instrui, ele providencia, você só segue com tudo.

12. ENTREGUE AO USUÁRIO o documento ER-OUTPUT\REQUISITOS-BACKEND.md com:

   A) FERRAMENTAS/STACK (o que você VAI usar e por quê):
      - API:            FastAPI (Python 3.11+)
      - Banco + Auth:   Supabase (Postgres)   OU   Docker + Postgres local
      - Vetor/busca:    pgvector (na Supabase)
      - Transcrição:    Groq API   OU   faster-whisper local
      - IA/LLM:         DeepSeek API   OU   Ollama local
      - Embeddings:     sentence-transformers   OU   embeddings da Supabase/OpenAI
      - Fila:           FastAPI BackgroundTasks   OU   Celery+Redis

   B) CONTAS QUE O USUÁRIO PRECISA CRIAR (com o link de cada uma):
      1. Supabase    → crie um projeto gratuito em https://supabase.com
                       anote: URL do projeto + anon key + service_role key
      2. DeepSeek    → crie conta em https://platform.deepseek.com  → gere API key
      3. Groq        → https://console.groq.com  → gere API key (se for usar)
      4. Google Cloud → https://console.cloud.google.com → ative Calendar API
                       e gere OAuth client + refresh_token (se o app tiver calendário)
      5. (se VPS)    → servidor Linux (você já tem a VPS: apontar o DNS)

   C) O QUE VOCÊ JÁ TEM vs O QUE FALTA (marque cada um: ✅ pronto / ⚠️ falta):
      Reproduza a lista das variáveis de ambiente e marque o status de cada uma.

   D) INSTRUÇÃO DE 3 LINHAS de como o usuário preenche o .env.

13. Crie o .env.example com TODAS as variáveis (sem preencher valor):
    SUPABASE_URL=
    SUPABASE_ANON_KEY=
    SUPABASE_SERVICE_ROLE_KEY=
    DEEPSEEK_API_KEY=
    GROQ_API_KEY=
    GOOGLE_CLIENT_ID=
    GOOGLE_CLIENT_SECRET=
    GOOGLE_CALENDAR_REFRESH_TOKEN=
    DATABASE_URL=
    JWT_SECRET=

14. NÃO siga para a Fase 4 de cérebro enquanto o .env não estiver preenchido com
    valores reais OU o usuário não confirmar que as contas estão prontas.
    Se algo depender só de você (ex.: JWT_SECRET), você gera. O resto, aguarda.

─────────────────────────────────────────────────────────────
ESPAÇO EM DISCO
─────────────────────────────────────────────────────────────
- ER leve (extrair cliente): ~2 GB
- Backend + libs Python: ~3 GB
- Whisper modelo small/medium (se local): +1 a 5 GB
- Ollama + modelo LLM local (opcional): +5 a 12 GB
TOTAL realista: 6–12 GB (sem LLM local) | 15–25 GB (com Ollama+Whisper local).

MEÇA o espaço livre e avise. Se o operador quiser o mais barato, sugira:
  Groq (transcrição) + DeepSeek (IA) = sem GPU, sem baixar modelo, ~2 GB só de libs.

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\00-setup.md com versão de cada ferramenta + verificação + disco usado.

Confirme: "SETUP COMPLETO. [N] ferramentas. Disco usado: [X] GB."
```
