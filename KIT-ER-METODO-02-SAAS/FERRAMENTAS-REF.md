# 🔧 FERRAMENTAS — REFERÊNCIA (Método 02 — SaaS thin-client)

## Extração do contrato (o essencial deste método)

| Ferramenta | O que faz | Disco |
|-----------|-----------|-------|
| **ripgrep (`rg`)** | varrer código por URLs/rotas/call sites (rápido) | ~5 MB |
| **@electron/asar** | extrair bundle de app Electron | ~5 MB |
| **jadx / apktool** | extrair APK (DEX/Java/smali) | ~150 MB |
| **dnSpy / ILSpy** | decompilar clientes .NET | ~100 MB |
| **mitmproxy** | capturar tráfego real app↔servidor | ~40 MB |
| **Frida (frida-tools)** | cert-unpinning pra ver HTTPS | ~300 MB |
| **Wireshark** | captura de pacotes | ~150 MB |
| **Detect It Easy** | identificar tipo do cliente | ~30 MB |

## Reconstrução do backend (cérebro)

| Camada | Ferramenta | Disco |
|--------|-----------|-------|
| API | **FastAPI + uvicorn** | ~200 MB |
| Auth/DB | **Supabase** (Postgres + Auth) | nuvem (0 local) |
| DB local alt. | Docker + Postgres | ~2 GB |
| Vetores | **pgvector** (na Supabase) | 0 extra |
| Transcrição | **faster-whisper** (local) OU **groq** (API) | +1–5 GB (modelo) |
| IA | **DeepSeek** (API) OU **Ollama** (local) | 0 OU +5–12 GB |
| Embeddings | **sentence-transformers** | ~500 MB |
| Fila | Celery + Redis (Docker) | ~300 MB |

## Total

| Cenário | Espaço |
|---------|--------|
| Mais barato (tudo API: Groq + DeepSeek + Supabase) | ~2–3 GB |
| Com Whisper local (CPU) | ~6–8 GB |
| Full local (Ollama + Whisper + Docker Postgres) | ~18–25 GB |

> **Recomendação de custo:** Groq (transcrição) + DeepSeek (IA) + Supabase (DB/auth/vetor)
> = quase zero de disco local e zero GPU. Só precisa das chaves no `.env`.
