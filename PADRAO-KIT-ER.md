# PADRÃO KIT ER BLACK — DEV PRO ULTRA

> Este documento define o padrão que os KITs de Engenharia Reversa seguem.
> Uma outra IA (Codex, Cursor, Claude, qualquer agente) lê isto e converge
> para o mesmo nível, sem perguntar nada. O padrão não mora na cabeça de
> ninguém: mora aqui, no disco.

---

## O QUE É O NÍVEL "DEV PRO ULTRA"

Não é prompt mais longo. São QUATRO camadas que o material fraco não tem:

1. **RÉGUA DE MEDIÇÃO** — todo número é medido, nunca estimado. Se não mediu,
   escreve "nao medido".
2. **ANATOMIA DE FASE** — cada fase tem a mesma ossatura, item por item.
3. **GATE DE SEGURANÇA** — uma conferência mecânica roda antes de cada fase ser
   declarada pronta. Item aberto = fase não fecha.
4. **REGRA DA PROVA** — achado sem a tríade (pedido + resposta + artefato) NÃO
   entra. "Acho que é X" não vale.

---

## ANATOMIA DE TODA FASE (a ossatura obrigatória)

Toda fase, sem exceção, entrega nesta ordem:

```
# FASE N — NOME

**O que este prompt faz:** [missão em UMA linha, verbo + objeto]

**O que você recebe:** [nome do arquivo de saída] + [o que tem dentro, enumerado]

**O que sai no caso real:** [números MEDIDOS de um caso executado — se esta fase
ainda não rodou em nenhum alvo real, escreva "caso real ainda nao executado" e
liste o que ela DEVE medir. NUNCA invente número. NUNCA estime no lugar de medir.]

**Como usar:** cole o prompt abaixo.

[prompt]

**O QUE NÃO FAZER** (erros que já custaram retrabalho, cada um com o motivo):
- [não fazer X] — [porque Y]

**GATE DE SEGURANÇA** (roda ANTES de declarar pronta, resultado colado):
- [ ] [checagem mecânica 1]
- [ ] [checagem 2]
- [ ] a prova foi colada (pedido + resposta + artefato)

**ENTREGÁVEL:** [arquivo] + [conteúdo mínimo]

**CRITÉRIOS DE QUALIDADE (só avance quando):**
- [ ] [critério verificável]

Confirme com: "FASE N OK. [resumo medido]."
```

---

## AS 5 REGRAS QUE VALEM EM TODAS AS FASES

1. **NÃO RESUMA.** Se a lista tem 40 itens, escreva os 40.
2. **NÃO ENFEITE.** Frase curta e direta. Sem "robusto", "poderoso", "blindado".
3. **FONTE E DATA.** Todo número tem fonte e data. Não mediu → "nao medido".
4. **ENTREGÁVEL EM ARQUIVO.** O resultado sai em arquivo, não na conversa.
5. **DIGA O QUE FALTOU.** No fim, o que não deu pra fazer e por quê.

---

## A REGRA DA PROVA (vale em TODA fase)

Achado técnico sem a tríade NÃO entra:

```
PEDIDO     o comando/input exato que você rodou
RESPOSTA   a saída bruta, literal, colada
ARTEFATO   o print, o dump, o hash, o diff, o arquivo gerado
```

Ela vale EXATAMENTE igual na análise do binário local E na do SaaS:
- uma função "reconstruída" sem o diff + teste de paridade é PROMESSA, não entrega.
- um endpoint "mapeado" sem a resposta real capturada é PROMESSA.
- uma lacuna "impossível" sem a lista "tentei X, Y, Z e falhou por [motivo]" é RENÚNCIA.

Se não conseguiu provar, escreva "nao provado" e diga o que tentou. Isso não é
falha: é a diferença entre engenharia e teatro.

---

## SEVERIDADE TEM CRITÉRIO (nunca opinião)

```
CRÍTICA = execução de comportamento errado no clone, quebra de outro componente,
          ou proteção ativa não neutralizada (o clone se auto-invalida)
ALTA    = paridade quebrada em caminho funcional, ou contrato divergente em rota núcleo
MÉDIA   = divergência em caminho periférico sem prova, ou shape não confirmado
BAIXA   = higiene (string legada, símbolo não nomeado, import sem uso), sem impacto
```

---

## GATE DE SEGURANÇA (o portão mecânico, vale nos 2 KITs)

Antes de QUALQUER fase ser declarada pronta, roda esta conferência e cola o resultado:

```
- [ ] sha256 do alvo original salvo ANTES de qualquer escrita
- [ ] todo artefato gerado tem hash registrado
- [ ] nenhum caminho absoluto da máquina do operador no código reconstruído
- [ ] nenhuma credencial/chave/secreto saiu para o código
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] toda entrega leva a tríade da prova (pedido + resposta + artefato)
- [ ] binário suspeito só rodou em isolamento (VM/qiling/HyperDbg), nunca no host
```

Item aberto = fase NÃO fecha. Não escreva "feito" com item aberto.

---

## A VALIDAÇÃO MECÂNICA DO KIT (o portão de fora)

`VALIDAR-KIT.py` mede o KIT inteiro, sem opinião, e dá nota. Rode antes de
entregar:

```
python VALIDAR-KIT.py --todas
```

10 âncoras valem a nota de cada KIT:
1. prompt mestre existe
2. fase VALIDAR existe
3. README existe
4. checklist final existe
5. tabela de ferramentas existe
6. regra da cópia presente
7. hash sha256 presente
8. regra de lacuna + "tentei X/Y/Z" presente
9. inteligência de alvo (CVE/writeup/open-source) presente
10. gate de segurança (achado sem prova não entra) + severidade + caminho relativo + cérebro mapeado

KIT com 100% nas âncoras = estrutura DEV PRO ULTRA. Abaixo disso, tem fase
que ainda é só "prompt numa fila".

---

## O QUE SEPARA CLONE REAL DE AMADOR (a régua do binário)

| Amador | DEV PRO ULTRA |
|---|---|
| descompila e "entende" | reconstrói e PROVA paridade (mesma entrada → mesma saída) |
| marca "impossível" e pula | esgota angr/Triton/Z3/HyperDbg e documenta cada tentativa |
| desativa checksum (o clone morre) | reconstrói o algoritmo e gera o valor íntegro |
| roda no host | isola em VM/qiling/HyperDbg |
| chumba caminho absoluto | usa relativo, rodou em outra máquina |
| nomeia função por chute | binding-diff (Diaphora/BinDiff) nomeia de graça |

---

## O QUE SEPARA CLONE REAL DE AMADOR (a régua do SaaS)

| Amador | DEV PRO ULTRA |
|---|---|
| assume REST | extrai GraphQL/gRPC/WS se for o caso |
| mapeia rota por olho | captura a resposta real (mitmproxy/Frida cert-unpinning) |
| stub o núcleo todo | reimplementa o NÚCLEO com lógica REAL, stub só a perfumaria |
| shape "parece certo" | valida contra o consumidor (o código que LÊ a resposta) |
| perde o prompt de sistema | extrai e guarda em prompts-extraidos/ |
| chumba credencial | segredo em variável de ambiente, relativo |
