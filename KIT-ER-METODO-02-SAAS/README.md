# 🧬 KIT ER BLACK — MÉTODO 02 (Thin-client SaaS — cérebro na NUVEM)

> **O que é:** pacote drop-in que instrui QUALQUER IA a clonar um app SaaS thin-client,
> do contrato da API ao backend reconstruído 100% funcional.
> Caso-âncora: **Granola → AnotaAí**.
> O operador só fornece **o nome do app** e **o caminho do cliente/instalador local**. O resto é da IA.

---

## 🚀 COMO USAR (90 segundos)

1. **Abra sua IA** com shell/ferramentas.
2. **Cole o `00-PROMPT-MESTRE.md`** como primeira mensagem.
3. Forneça só:
   - `NOME_DO_APP` — ex.: `Granola`
   - `CAMINHO_LOCAL` — ex.: `C:\Alvos\granola-instalador.exe` ou a pasta do app instalado
4. **Não faça mais nada.** A IA extrai o cliente, mapeia o contrato, reconstrói o backend
   com peças open-source e recoloca no ar 100% funcional — sem pagar a mensalidade do alvo.

---

## 📂 ESTRUTURA DO KIT

| Arquivo | Conteúdo |
|---------|----------|
| `README.md` | Este guia |
| `00-PROMPT-MESTRE.md` | Prompt único que orquestra tudo + gate + regra da prova + severidade |
| `01-SETUP-INSTALACAO.md` | Instalação das ferramentas + disco (GB) |
| `02-FASE-CORPO.md` | Fase 1 — clonar o corpo (reusa método 01) |
| `03-FASE-CONTRATO.md` | Fase 2 — extrair o contrato da API (o coração) |
| `04-FASE-CLASSIFICAR.md` | Fase 3 — separar núcleo vs perfumaria |
| `05-FASE-CEREBRO.md` | Fase 4 — reconstruir o cérebro (IA real) |
| `06-FASE-CONECTAR.md` | Fase 5 — ligar front clonado ao backend novo |
| `07-FASE-VALIDAR.md` | Fase 6 — provar paridade + novas funções |
| `08-CHECKLIST-FINAL.md` | Conferência final |
| `FERRAMENTAS-REF.md` | Tabela de ferramentas + espaço |

> **Padrão e validação:** o `../PADRAO-KIT-ER.md` define a ossatura que toda fase segue
> (anatomia + gate + regra da prova + severidade). O `../VALIDAR-KIT.py` mede o KIT sem
> opinião — rode `python VALIDAR-KIT.py --todas` para conferir a nota antes de entregar.

---

## ⚡ A VERDADE ESTRUTURAL (leia antes)

A ER recupera o **corpo** (front/instalador), não o **cérebro** (servidor + modelos).
O que se extrai do cliente é o **CONTRATO**: endpoints, shapes de request/response,
prompts de sistema, tipos. O cérebro **reimplementa-se** com peças open-source.

**Não persiga "copiar o servidor" — ele não está no artefato.**
Persiga: **extrair 100% do contrato + reconstruir o núcleo com lógica real.**

---

## 🧩 O QUE A IA RECONSTRÓI (stack recomendada)

| Camada | Peça |
|--------|------|
| API | **FastAPI** (Python) |
| Auth + DB | **Supabase** (Postgres + Auth + pgvector) |
| Transcrição | **Whisper / faster-whisper / Groq** |
| Resumo/IA/chat | **DeepSeek / Ollama / Groq** |
| Busca semântica | **pgvector + sentence-transformers** |
| Fila de jobs | **FastAPI BackgroundTasks** ou Celery+Redis |

---

## ✅ RESULTADO ESPERADO

- Front clonado idêntico (mesmas telas, deep links, rebrand)
- Contrato da API 100% mapeado
- Backend próprio rodando, com núcleo real (não stub)
- App funcional de ponta a ponta, sem mensalidade

---

*Próximo passo: abrir `00-PROMPT-MESTRE.md` e colar na IA.*
