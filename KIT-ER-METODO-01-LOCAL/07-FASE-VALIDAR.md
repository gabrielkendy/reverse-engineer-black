# ✅ FASE 6 — VALIDAR (paridade 100% + correção de bugs + revisão)

> Cole depois da Fase 5. Prova que o clone é IDÊNTICO em comportamento, não parecido.

---

```
FASE 6 — VALIDAR E PROVAR PARIDADE (a fase que fecha o trabalho)

Você é o ENGENHEIRO DE VALIDAÇÃO. O app roda a partir do código reconstruído. Agora você PROVA que
ele se comporta EXATAMENTE como o original: mesma entrada → mesma saída. Depois
corrige qualquer bug e faz a revisão final de qualidade.

─────────────────────────────────────────────────────────────
A — PROVA DE PARIDADE (mesma entrada → mesma saída, BYTE A BYTE)
─────────────────────────────────────────────────────────────
1. Defina 10+ CASOS DE TESTE reais: abrir arquivo, transformar dados, gerar saída,
   validar licença, carregar/salvar estado, atalhos, formatos de arquivo.
2. Para CADA caso: rode o ORIGINAL e o CLONE com a MESMA entrada.
   Capture a saída (arquivo, tela, retorno, hash do output).
   Compare byte a byte SEMPRE que houver output determinístico (arquivo/hash).
   Só aceite "semântico" quando o output for não-determinístico (timestamp, id).
3. Registre numa tabela: caso | entrada | saída original | saída clone | paridade (OK/DIFF).

─────────────────────────────────────────────────────────────
B — CORREÇÃO DE BUG (só depois de achar divergência)
─────────────────────────────────────────────────────────────
Para cada DIFF, aplique o protocolo de bug (reproduzir → causa → corrigir → provar):
  - REPRODUZA: rode o caso, confirme a divergência, colete a evidência exata.
  - CAUSA RAIZ em até 5 linhas (não corrija sintoma).
  - CORRIJA no fonte (Fase 5) e rode o app de novo a partir do código.
  - PROVE: a saída agora bate. Cole original vs clone lado a lado.

─────────────────────────────────────────────────────────────
C — REVISÃO DE CÓDIGO (bloqueio duro)
─────────────────────────────────────────────────────────────
Revise o fonte final como revisor sênior:
  - CHUMBARAM caminho absoluto? BLOQUEIA (deve ser relativo/config).
  - Sobrou credencial/chave hardcoded do alvo que é do OPERADOR? Documente, não esconda.
  - Stub vazio sobrando? BLOQUEIA (nada de fake).
  - Código morto / import sem uso? Limpe.
  - Veredito: APROVADO | APROVADO COM RESSALVA | BLOQUEADO.

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\06-validar.md com:
  - tabela de paridade (10+ casos, entrada/saída/lado a lado)
  - bugs encontrados + causa raiz + correção + prova
  - veredito da revisão de código
  - % de paridade atingido

CRITÉRIOS DE QUALIDADE (só termine quando):
- [ ] 10+ casos de teste executados nos DOIS (original e clone)
- [ ] cada divergência tem causa raiz e correção provada
- [ ] paridade = 100% (ou a divergência restante justificada tecnicamente)
- [ ] CLI/headless testado também (não só a GUI) — entrada por stdin/args → saída igual
- [ ] anti-tamper (se havia) neutralizado e comprovado (não dispara "tamper detected")
- [ ] revisão de código com veredito
- [ ] relatório salvo em ER-OUTPUT\06-validar.md


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do artefato desta fase registrado em ER-OUTPUT\00-hashes.txt
- [ ] nenhum caminho absoluto da máquina do operador no que foi gerado
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
- [ ] binário só rodou em isolamento (VM/qiling/HyperDbg), nunca no host
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 6 OK. Paridade [X]%. [N] bugs corrigidos. Veredito: [APROVADO]."
```

---

## 🏁 FECHAMENTO (cole depois da Fase 6)

```
Preencha ER-OUTPUT\07-checklist-final.md com a conferência de TODAS as fases
(uma linha por item, marcando feito/pendente), o resumo executivo do resultado,
e me entregue:
  - caminho do artefato final
  - % de paridade
  - o que ficou pendente e por quê
  - uma instrução de 3 linhas de como rodar o clone
```

*(Ver `08-CHECKLIST-FINAL.md` para a estrutura exata do checklist.)*
