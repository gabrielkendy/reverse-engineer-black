# SEM-TRAVA · o gate que faz o agente executar até o fim

O método ER BLACK é longo: 12 fases, dezenas de ferramentas, horas de execução.
Agente novo costuma morrer no meio do caminho: pede permissão, avisa que "não pode",
oferece uma alternativa mais segura, resume em vez de fazer.

Esta pasta resolve isso. É o **gate AXION**: o texto que o agente recebe **antes** do
método, para tratar engenharia reversa como trabalho técnico comum e ir até a última fase.

## Os dois juntos

| Só o método | Só o gate | Os dois |
|---|---|---|
| agente para na fase 3 pedindo permissão | agente solto, sem rumo, inventando fase | instala, aponta o app, volta depois com o clone rodando |

## O que tem aqui

| Arquivo | O que é |
|---|---|
| `AXION-MATRIZ.txt` | o gate, texto original, completo · é este que se cola antes de tudo |
| `AXION-SOUL-HERMES.txt` | o mesmo gate com o ajuste do scanner, para o Hermes |
| `1-PROMPT-AXION.txt` | o gate em uma mensagem só |
| `2-SOUL-DO-PERFIL.txt` | o gate no formato de alma de perfil |
| `INSTALAR-NO-AGENTE.md` | como instalar em cada agente, passo a passo |
| `TESTADOR.py` | mede qualquer modelo em qualquer endpoint compatível com OpenAI |
| `KIT-AXION-HERMES/` | o kit completo: por modelo, receita do zero para outra máquina, runner local |
| `FONTES.md` | onde estão os acervos públicos de jailbreak por modelo |

## Como saber que funcionou (medido, não achismo)

O `TESTADOR.py` manda pedidos de engenharia reversa e conta quantos o modelo **entregou**
de verdade. Critério de aprovação: entregues igual ao número de pedidos.

```
python TESTADOR.py <modelo> --base <url> --key NOME_DA_VARIAVEL_DE_AMBIENTE
```

A chave é lida da variável de ambiente e nunca é impressa. O prompt padrão é o
`2-SOUL-DO-PERFIL.txt` que está ao lado do script.

## Regra que não se negocia

O gate **não** substitui o método e não autoriza trabalho em máquina de terceiro.
Ele existe para o seu agente executar o seu trabalho, no seu alvo, até o fim.
Alvo é sempre cópia: o original fica intocado, com sha256 registrado.
