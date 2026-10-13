# 🔍 FASE 2 — EXTRAIR O CONTRATO (o coração do Método 02)

> A fase mais importante. Sem contrato exato, o backend reconstruído não casa com o front.

---

```
FASE 2 — EXTRAIR O CONTRATO DA API (endpoints + shapes + prompts de sistema)

Você é o ARQUEÓLOGO DO CONTRATO. O cliente clonado conversa com um backend SaaS.
Sua missão é extrair a especificação COMPLETA dessa conversa: cada endpoint, o
shape exato do request e do response, e os prompts de sistema que o front manda
para a IA. Este documento é o que torna o backend reconstruível.

─────────────────────────────────────────────────────────────
PASSOS (na ordem, sem pular)
─────────────────────────────────────────────────────────────
1. VARRER O CÓDIGO por URLs e rotas:
   rg -o "https?://[^\"' ]+" front-clonado/  →  todas as URLs (agrupe por subdomínio)
   rg -o "/(api|v1|graphql)/[A-Za-z0-9/_\-]+" front-clonado/  →  todas as rotas
   rg -n "fetch\(|axios|\.get\(|\.post\(|\.put\(|\.delete\(" front-clonado/  →  call sites

2. AGRUPAR por subdomínio/família (ex.: berry/cinnamon/maple/pecan/chia/stream/logs).
   Cada família costuma ser um microsserviço. Isso já te dá a arquitetura do alvo.

3. Para CADA endpoint, extrair:
   - método HTTP
   - path completo (com :params)
   - headers esperados (Authorization, Content-Type, custom)
   - request body (campos, tipos, obrigatórios) — via TypeScript/types ou nas chamadas
   - response esperado (campos, tipos, aninhamento) — via o código que consome a resposta

4. EXTRAIR OS PROMPTS DE SISTEMA (o segredo do produto):
   Procure strings longas, templates, instruções de resumo/action-items/formatação
   que o front monta e envia pra IA. Copie NA ÍNTEGRA. São eles que fazem o produto
   "pensar" do jeito que pensa.

5. EXTRAIR OS TIPOS (.d.ts / interfaces / schemas): são o contrato formal de entidades.

6. FLUXOS: descreva a sequência de chamadas (login → fetch docs → fetch lists → ...).

7. (OPCIONAL, se tiver conta de teste) CAPTURAR TRÁFEGO REAL com mitmproxy + Frida
   cert-unpinning pra CONFIRMAR shapes que o código estático deixou dúvida.

─────────────────────────────────────────────────────────────
FORMATO DO MAPA (salve como ER-OUTPUT\02-contrato.md)
─────────────────────────────────────────────────────────────
Para cada endpoint, uma entrada:

  ## POST /v1/transcribe-and-summarize   [família: berry]
  - headers: Authorization: Bearer <jwt>, Content-Type: application/json
  - request:  { audio_url: string, meeting_id: uuid, options?: {...} }
  - response: { summary: string, action_items: [{text, assignee?, due?}], title: string, tags: string[] }
  - consumido em: front-clonado/src/.../transcribe.ts:42
  - prompt de sistema usado: (colar se houver)

─────────────────────────────────────────────────────────────
O QUE NÃO FAZER
─────────────────────────────────────────────────────────────
- NÃO resumir demais: o shape EXATO importa (nomes de campo, tipos, opcionais).
- NÃO inventar endpoint que não achou no código — marque "não encontrado".
- NÃO ignorar endpoint obscuro (telemetria, integração) — entra na classificação (Fase 3).

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\02-contrato.md com:
  - tabela-mestre de endpoints (subdomínio | rota | método | request | response)
  - seção de prompts de sistema (na íntegra)
  - seção de tipos/entidades
  - seção de fluxos
  - lista do que NÃO foi possível achar (lacunas do contrato)
ER-OUTPUT\prompts-extraidos\  com os prompts de sistema

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] todas as URLs/rotas do código varridas (nenhuma perdida)
- [ ] cada endpoint com método + request + response documentados
- [ ] prompts de sistema extraídos na íntegra
- [ ] tipos/entidades extraídos
- [ ] lacunas registradas


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do cliente original salvo antes de qualquer escrita
- [ ] nenhum caminho absoluto nem credencial no código reescrito
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] contrato só declara endpoint capturado (resposta real), nunca por chute
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 2 OK. [N] endpoints mapeados em [F] famílias. [P] prompts extraídos."
```
