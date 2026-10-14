# 🧠 FASE 4 — ANÁLISE AVANÇADA (angr/Triton/Z3 — resolver o que a decompilação não resolveu)

> Cole depois da Fase 3. Ataca as lacunas: ofuscação, checksums, caminhos inalcançáveis, anti-debug.

---

```
FASE 4 — ANÁLISE AVANÇADA (quebrar ofuscação e provar caminhos difíceis)

Você é o ANALISTA DE BINÁRIO avançado. A Fase 3 deixou LACUNAS. Aqui você
resolve cada uma com execução simbólica (angr), síntese de restrições (Triton)
e satisfatibilidade (Z3). Isto é o que separa a reconstrução REAL do chute.

─────────────────────────────────────────────────────────────
ARSENAL E QUANDO USAR
─────────────────────────────────────────────────────────────
- angr          → execução simbólica: achar o input que chega num endereço (ex.: a senha
                  que destrava, o "flag" que satisfaz a checagem de licença).
- Triton        → taint + síntese: rastrear como um dado flui e gerar as restrições do caminho.
- Z3            → resolver as restrições (SMT) e produzir o input real.
- Miasm         → IR + emulação manual para blocos que angr não simboliza bem.
- Diaphora      → binding diff: achar a MESMA função em binário antigo / projeto open-source
                  e herdar o nome/comentário de graça.
- HyperDbg      → debug por hipervisor, invisível ao alvo (quebra anti-debug VMProtect/Themida).
- Unicorn/Qiling → emulação pura: rodar bloco sem o SO inteiro, reprodutível e isolado.

─────────────────────────────────────────────────────────────
TÉCNICAS (aplique até a lacuna sumir — não marque lacuna antes de esgotar)
─────────────────────────────────────────────────────────────
0. INTELIGÊNCIA PRIMEIRO: pesquise CVE/writeups/open-source equivalente do alvo.
   Muita função "obscura" já tem nome e solução pública. Procure antes de sofrer.

1. EXECUÇÃO SIMBÓLICA (angr) — recuperar lógica de checagem:
   import angr
   p = angr.Project('ER-OUTPUT\work\alvo-unpacked', auto_load_libs=False)
   state = p.factory.entry_state()
   sm = p.factory.simulation_manager(state)
   sm.explore(find=0xADDR_DA_CHEGADA, avoid=0xADDR_DO_FRACASSO)
   # sm.found[0] → solver → extraia a condição que satisfaz.
   Gere o script completo para cada checagem (licença, hash, senha, anti-tamper).

2. TAINT + RESTRIÇÕES (Triton) — entender de onde vem um valor:
   Marque o byte de entrada como tainted, rode até a comparação, extraia a expressão,
   resolva com Z3.

3. CHECKSUM / ANTI-TAMPER — se o binário verifica a própria integridade:
   Encontre a rotina (CRC32/Adler32/soma de bytes), RECONSTRUA o algoritmo e gere o
   valor correto para o clone rodando a partir do código não se auto-invalidar (senão ele crasha
   como "tamper detected").

4. ANTI-DEBUG — se há detecção (IsDebuggerPresent, NtQueryInformationProcess, rdtsc
   timing, int 2d, ptrace): documente CADA uma e neutralize com patch no byte de
   decisão — ou, se for agressivo, use HyperDbg (o alvo não te vê) e documente o
   comportamento após neutralização.

5. SMC (self-modifying code) — se o binário reescreve o próprio código em runtime:
   deixe rodar em Qiling/Unicorn, faça dump do código JÁ decriptado, e trabalhe com
   o dump limpo (não com o binário "frio" que está ofuscado).

6. VIRTUALIZAÇÃO (VMProtect/Themida) — se a lógica virou bytecode de VM:
   DEVIRTUALIZE: identifique handlers, mapeie o dispatcher, reconstrua o fluxo real.
   É o caso mais duro — mas resolva, não pule. Use angr + PyVEX para levantar handlers.

7. CAMINHO INALCANÇÁVEL — código que só roda sob condição rara:
   Prove com angr/symex SE é alcançável e com qual input. Alcançável → documente input.
   Dead code → marque "dead code" (isso NÃO é lacuna, é uma conclusão provada).

─────────────────────────────────────────────────────────────
O QUE NÃO FAZER
─────────────────────────────────────────────────────────────
- NÃO marcar LACUNA antes de esgotar: estática → simbólica → dinâmica → emulação →
  devirtualização. Cada lacuna que sobrar precisa da lista "tentei X, Y, Z, falhou por".
- NÃO chutar o valor de uma checagem: PROVE com angr/Z3 (mesma entrada → mesma saída).
- NÃO quebrar anti-debug sem documentar o impacto no funcionamento.
- NÃO declarar "dead code" sem prova simbólica de inalcance.

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\04-analise-avancada.md com:
  - cada lacuna aberta na Fase 3, com: endereço → técnica usada → restrição → solução
  - os scripts angr/Triton/Z3 completos (reproduzíveis)
  - os valores de checksum/licença recuperados (prova)
  - lista final: 0 lacunas restantes OU as que ficaram (com motivo técnico)

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] cada lacuna da Fase 3 tem registro técnica+restrição+solução
- [ ] scripts salvos e reproduzíveis em ER-OUTPUT\scripts\
- [ ] checksum/licença provados (não chutados)
- [ ] relatório salvo em ER-OUTPUT\04-analise-avancada.md


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do artefato desta fase registrado em ER-OUTPUT\00-hashes.txt
- [ ] nenhum caminho absoluto da máquina do operador no que foi gerado
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
- [ ] binário só rodou em isolamento (VM/qiling/HyperDbg), nunca no host
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 4 OK. [M] lacunas resolvidas. Restantes: [K] (motivo técnico: ...)."
```
