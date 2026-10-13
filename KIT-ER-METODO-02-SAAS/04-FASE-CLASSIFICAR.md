# 🗂️ FASE 3 — CLASSIFICAR (núcleo real vs perfumaria stub)

---

```
FASE 3 — CLASSIFICAR OS ENDPOINTS (o que reconstrói de verdade vs o que estuba)

Você é o ARQUITETO DE CUSTO. O mapa da Fase 2 tem dezenas/centenas de endpoints.
Reconstruir TODOS com lógica real é desperdício. Você separa o que é ESSENCIAL
(o núcleo que faz o produto valer) do que é PERIFÉRICO (integrações, telemetria).

─────────────────────────────────────────────────────────────
CRITÉRIO DE CLASSIFICAÇÃO
─────────────────────────────────────────────────────────────
Faça 2 perguntas por endpoint:
  1. SEM ele, o produto funciona?  (não → NÚCLEO)  (sim → perfumaria)
  2. Ele entrega o valor central (transcrição, resumo, notas, busca, calendário)?
     (sim → NÚCLEO)  (não → perfumaria)

Classifique em 3 níveis:
  🟢 NÚCLEO      → reconstrói com lógica REAL (é o produto)
  🟡 ÚTIL        → reconstrói simplificado (funciona, sem luxo)
  🔴 PERFUMARIA  → stub (devolve shape válido, não quebra o front)

─────────────────────────────────────────────────────────────
ENTREGUE A TABELA
─────────────────────────────────────────────────────────────
| endpoint | família | nível (🟢🟡🔴) | justificativa | reconstrução |

Exemplos típicos de um app de notas/assistente de reuniões:
  🟢 auth (login/token/refresh)          → produto não existe sem entrar
  🟢 criar/ler/editar notas             → valor central
  🟢 transcrever áudio                   → valor central
  🟢 resumir + action items             → valor central
  🟢 busca semântica                     → valor central
  🟢 calendário (sync Google)            → valor central
  🟡 compartilhar nota / exportar PDF    → útil, simplificável
  🔴 integração Slack/Zoom/Salesforce   → stub (shape válido)
  🔴 telemetria / analytics / logs       → stub
  🔴 login social (além do Google)       → stub

─────────────────────────────────────────────────────────────
REGRAS
─────────────────────────────────────────────────────────────
- Stub NUNCA devolve 404/500: devolve 200 com o shape esperado vazio/neutro,
  para o front não disparar error boundary.
- Stub LOGGA a chamada (pra saber o que o usuário tentou usar).
- Registre a decisão de CADA endpoint, não só os fáceis.

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\03-classificar.md com a tabela completa + contagem final
(núcleo / útil / perfumaria) + o motivo de cada núcleo.

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] 100% dos endpoints da Fase 2 classificados (nenhum sem nível)
- [ ] cada núcleo tem justificativa de valor
- [ ] contagem final escrita (N núcleo | U útil | P perfumaria)


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do cliente original salvo antes de qualquer escrita
- [ ] nenhum caminho absoluto nem credencial no código reescrito
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] contrato só declara endpoint capturado (resposta real), nunca por chute
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 3 OK. Núcleo [N] | Útil [U] | Perfumaria [P]."
```
