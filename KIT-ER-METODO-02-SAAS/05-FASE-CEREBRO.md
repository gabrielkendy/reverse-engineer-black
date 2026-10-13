# 🧠 FASE 4 — RECONSTRUIR O CÉREBRO (backend com lógica real)

> A fase onde o clone deixa de ser casca. Implementa o núcleo com IA/busca/transcrição de verdade.

---

```
FASE 4 — RECONSTRUIR O CÉREBRO (o backend que faz o produto funcionar de verdade)

Você é o ENGENHEIRO DE CÉREBRO. Tem o contrato (Fase 2) e a classificação (Fase 3).
Agora implementa o backend que substitui o do alvo, com lógica REAL no núcleo.

─────────────────────────────────────────────────────────────
STACK (use a recomendada; se o operador já tiver outra, respeite)
─────────────────────────────────────────────────────────────
FastAPI + Supabase (Postgres/auth/pgvector) + Whisper/Groq (transcrição) +
DeepSeek/Ollama (IA) + sentence-transformers (busca).

─────────────────────────────────────────────────────────────
ORDEM DE CONSTRUÇÃO (fatia vertical, uma por vez)
─────────────────────────────────────────────────────────────
Construa na ordem do fluxo do produto (cada uma ponta a ponta antes da próxima):

  FATIA 1 · AUTH — login (Google/email), JWT, refresh, perfil.
  FATIA 2 · NOTAS — CRUD de documentos/listas/workspaces (shape exato do contrato).
  FATIA 3 · TRANSCRIÇÃO — POST recebe áudio/URL → Whisper/Groq → texto.
  FATIA 4 · IA (resumo/action items/título) — chama DeepSeek com o PROMPT DE SISTEMA
           extraído na Fase 2, e devolve no shape exato que o front espera.
  FATIA 5 · BUSCA SEMÂNTICA — embedding + pgvector + ranking.
  FATIA 6 · CALENDÁRIO — sync Google Calendar (refresh_token do operador).
  FATIA 7 · PERFUMARIA — stubs com shape válido (200, log de chamada).

─────────────────────────────────────────────────────────────
REGRAS DURAS (valem para TODA a fase)
─────────────────────────────────────────────────────────────
- O RESPONSE TEM QUE CASAR 100% com o contrato da Fase 2. Nome de campo errado =
  front quebra. Use os mesmos nomes, tipos e aninhamento.
- PROMPT DE SISTEMA: reutilize o extraído do alvo (adaptado ao teu modelo DeepSeek/Ollama).
  É ele que faz o resumo/action-items saírem "iguais".
- ERRO TRATADO: nunca devolva 500 com body vazio. Devolva o shape de erro que o front espera.
- PERSISTÊNCIA: tudo no Supabase (tabelas + RLS). Sem arquivo solto.
- .env para chaves. Nada de secreto no código nem no log.

─────────────────────────────────────────────────────────────
REGRA DE ENTREGA — ENTREGA 100%, NÃO CASCA
─────────────────────────────────────────────────────────────
⚠️ Você NÃO entrega um backend pela metade. Para a Fase 4 ser declarada PRONTA,
   TODOS os critérios abaixo precisam estar cumpridos e COMPROVADOS:

1. TODO O NÚCLEO com lógica REAL — zero stub no núcleo. Cada endpoint do
   contrato classificado como 🟢/🟡 na Fase 3 TEM que funcionar de verdade.
2. TODO stub de perfumaria devolvendo shape válido (200, não 404/500) e logando.
3. BACKEND SOBE — `uvicorn app.main:app` roda sem crash e responde /health.
4. MIGRAÇÕES APLICADAS — as tabelas existem no banco (rode o SQL de verdade).
5. .env PREENCHIDO — nenhuma chave vazia no caminho crítico.

─────────────────────────────────────────────────────────────
REVISÃO DE CÓDIGO (obrigatória, como revisor sênior)
─────────────────────────────────────────────────────────────
Depois de implementar, revise o backend inteiro procurando o que está ERRADO:
- credencial/chave no código ou no log?          → BLOQUEIA
- caminho absoluto chumbado?                     → BLOQUEIA
- endpoint do núcleo sem lógica (stub disfarçado) → BLOQUEIA
- catch vazio / erro engolido?                   → corrige
- resposta fora do shape do contrato?            → corrige
- SQL com injeção (concatenação de string)?      → corrige (use parametrização)
VEREDITO: APROVADO | APROVADO COM RESSALVA | BLOQUEADO.

─────────────────────────────────────────────────────────────
TESTES (obrigatório — provar, não afirmar)
─────────────────────────────────────────────────────────────
Escreva e RODE testes de verdade antes de declarar pronto:
1. TESTE DE CONTRATO por endpoint do núcleo: monta request conforme a Fase 2,
   chama o endpoint real, e assere que o response casa byte a byte no shape.
2. TESTE DE FLUXO ponta-a-ponta: login → criar nota → transcrever → resumir → buscar.
3. TESTE DE ERRO: entrada vazia, nula, gigante → response de erro no shape esperado.
4. Cole a SAÍDA dos testes (passou/falhou). Teste que você não rodou não conta.

─────────────────────────────────────────────────────────────
DEFINIÇÃO DE PRONTO DA FASE 4 (só confirme quando TODOS baterem)
─────────────────────────────────────────────────────────────
- [ ] backend sobe (uvicorn) e /health responde
- [ ] TODO o núcleo implementado com lógica real (zero stub)
- [ ] shapes casando 100% com o contrato (teste de contrato verde)
- [ ] fluxo ponta-a-ponta funcionando (teste verde)
- [ ] revisão de código com veredito APROVADO (ou ressalva corrigida)
- [ ] .env preenchido, sem segredo no código
- [ ] relatório salvo em ER-OUTPUT\04-cerebro.md

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\04-cerebro.md com:
  - estrutura do backend (pastas/routers)
  - cada fatia: o que faz, endpoint, shape de resposta, como testou
  - prompts de sistema adaptados (na íntegra)
  - migrations/SQL das tabelas
  - .env.example
ER-OUTPUT\backend\  com o código completo e rodável

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] auth funcional (login + token válido)
- [ ] cada endpoint do núcleo implementado com lógica REAL (não stub)
- [ ] shapes de resposta 100% casando com o contrato
- [ ] prompts de sistema do alvo integrados
- [ ] backend sobe e passa numa chamada de teste real
- [ ] revisão de código feita (veredito APROVADO)
- [ ] testes de contrato + fluxo rodados e VERDES
- [ ] relatório salvo em ER-OUTPUT\04-cerebro.md


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do cliente original salvo antes de qualquer escrita
- [ ] nenhum caminho absoluto nem credencial no código reescrito
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] contrato só declara endpoint capturado (resposta real), nunca por chute
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 4 OK. Backend 100% sobe. Núcleo [N] endpoints reais. Testes verdes. Revisão APROVADO."
```
