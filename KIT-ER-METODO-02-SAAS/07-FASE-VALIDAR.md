# ✅ FASE 6 — VALIDAR (paridade + novas funções) + checklist

---

```
FASE 6 — VALIDAR (provar que o clone funciona de ponta a ponta e adicionar valor)

Você é o ENGENHEIRO DE VALIDAÇÃO. O app clonado funciona. Agora você prova que as
funções do núcleo entregam o MESMO resultado que o alvo, corrige qualquer bug, e
— a parte que ninguém faz — ADICIONA funções novas que o alvo não tem.

─────────────────────────────────────────────────────────────
A — PARIDADE DE NÚCLEO (pontuação)
─────────────────────────────────────────────────────────────
Para cada fatia do núcleo, rode um caso real e compare QUALIDADE:
  - Transcrição: mesmo áudio → texto fiel? (léxico/tempos)
  - Resumo/action items: mesma pauta → resumo + itens coerentes?
  - Busca: mesma query → mesmo documento relevante encontrado?
  - Calendário: evento criado → aparece no Google Calendar?
Registre em tabela: fatia | entrada | saída | paridade (OK/DIFF/parcial).

─────────────────────────────────────────────────────────────
B — CORREÇÃO DE BUG (protocolo)
─────────────────────────────────────────────────────────────
Para cada falha: REPRODUZA → CAUSA RAIZ (≤5 linhas) → CORRIJA → PROVE (rode de novo).

─────────────────────────────────────────────────────────────
C — NOVAS FUNÇÕES (o passo que transforma clone em produto)
─────────────────────────────────────────────────────────────
Agora que o cérebro é teu, proponha e implemente 3+ funções que o alvo NÃO tem,
alavancando tua stack própria. Exemplos (contexto notas/assistente):
  - resumo semanal automático de todas as reuniões
  - integração com teu CRM/n8n próprio
  - exportação em formato que o alvo cobra por assinatura
  - gatilho por palavra-chave (ex.: "mencionou orçamento" → alerta)
Registre cada função nova: o que faz, endpoint, como testou.

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\06-validar.md com:
  - tabela de paridade por fatia
  - bugs corrigidos (causa + prova)
  - as funções novas implementadas
  - o que ficou pendente e por quê

CRITÉRIOS DE QUALIDADE (só termine quando):
- [ ] cada fatia do núcleo testada de ponta a ponta
- [ ] bugs corrigidos com causa raiz
- [ ] 3+ funções novas implementadas
- [ ] revisão final de código (veredito APROVADO)
- [ ] backend em pé com testes verdes (entregue 100%, não casca)
- [ ] relatório salvo em ER-OUTPUT\06-validar.md


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do cliente original salvo antes de qualquer escrita
- [ ] nenhum caminho absoluto nem credencial no código reescrito
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] contrato só declara endpoint capturado (resposta real), nunca por chute
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 6 OK. Núcleo validado. [N] funções novas adicionadas."
```

---

## 🏁 FECHAMENTO

```
Preencha ER-OUTPUT\07-checklist-final.md (conferência de todas as fases + resumo)
e me entregue:
  - como subir o backend (1 comando)
  - como subir o front clonado (1 comando)
  - inventário: endpoints núcleo reais + endpoints stubados
  - o que ficou pendente
```

*(Estrutura do checklist em `08-CHECKLIST-FINAL.md`.)*
