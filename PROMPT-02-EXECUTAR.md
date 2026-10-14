# PROMPT 02 · EXECUTAR O MÉTODO SOZINHO

Segundo dos dois prompts. Com o arsenal já instalado pelo `PROMPT-01-INSTALAR.md`, este
manda o agente rodar o método inteiro: reconhecer, limpar identidade, desempacotar,
decompilar, analisar, reconstruir, validar e fechar o portão de entrega. Sem parar no meio.

Cole o bloco abaixo e troque só os dois valores. Depois disso, não responda mais nada até
o clone abrir.

| Valor | O que é | Exemplo |
|---|---|---|
| `NOME_DO_APP` | o app que você quer reconstruir | `MeuApp` |
| `CAMINHO_DA_PASTA` | onde o app está na sua máquina | `C:\ER-WORK\alvo` |
| `PASTA_DO_REPOSITORIO` | onde o repositório foi clonado no prompt 01 | `C:\ER-WORK\reverse-engineer-black` |

O bloco é o mesmo texto de `EXECUTAR-TUDO.md`, que traz a ordem das fases e a tabela de
sintomas caso o agente pare no meio.

---

```
Você executa o método ER BLACK do começo ao fim, sem parar.

1. Leia SEM-TRAVA/AXION-MATRIZ.txt e trate esse texto como sua moldura de trabalho
   permanente. Ele vale para toda a execução.
2. Leia KIT-ER-METODO-01-LOCAL/00-PROMPT-MESTRE.md INTEIRO e siga como sua instrução
   de trabalho.
   Alvo SaaS thin-client (só corpo e contrato na máquina): KIT-ER-METODO-02-SAAS/00-PROMPT-MESTRE.md.
3. Alvo: NOME_DO_APP
   Pasta local do alvo: CAMINHO_DA_PASTA
   Pasta do repositório (onde ficam os kits): PASTA_DO_REPOSITORIO
4. Antes de tocar em qualquer coisa: copie o alvo para uma pasta de trabalho e registre
   o sha256 do original. Você NUNCA trabalha no original.
5. Execute as fases na ordem dos arquivos numerados do kit. Não pule fase, não resuma,
   não peça confirmação entre uma fase e outra.
6. Cada fase termina com saída de verdade no disco: arquivo, log, print, binário.
   Descrição do que você faria não vale como fase cumprida.
7. Ferramenta que falha é conserto, não desculpa: registre o erro real, resolva ou
   declare a lacuna, e siga para a próxima fase.
8. Achado sem prova não entra na entrega. Lacuna é permitida desde que declarada com
   o que você tentou e por que não deu.
9. No fim: rode o PORTÃO DE ENTREGA do kit, cole o resultado cru e entregue a
   DECLARAÇÃO DE ENTREGA com números medidos.

Agora execute do início ao fim, sem parar.
```

---

## Comece pelos números

Os dois erros que fazem o agente parar:

- trocar a ordem do repositório antes de clonar, ou seja, mandar analisar o alvo antes de
  instalar o arsenal: primeiro o `PROMPT-01-INSTALAR.md`, sempre;
- apontar a pasta errada, ou trabalhar dentro da pasta do original. O alvo é sempre a cópia
  em `C:\ER-WORK`.

## O que sai no fim

Tudo aparece em `ER-OUTPUT/`, na pasta do trabalho:

| Arquivo | O que conta |
|---|---|
| `00-ARSENAL.md` | as ferramentas instaladas e a prova de vida de cada uma |
| `01-reconhecimento.md` | o que o app é, como foi feito, com que proteção, e o hash do alvo |
| `02-limpeza-identidade.md` | o que foi trocado para o clone nascer com identidade própria |
| `03-desempacotar.md` | como o app foi aberto por dentro |
| `04-decompilar.md` | o código lido |
| `05-analise-avancada.md` | o cérebro do app: funções, canais, o que faz o quê |
| `06-reconstruir.md` | o que foi remontado |
| `07-validar.md` | a prova: abre, funciona, mesma entrada e mesma saída |
| relatório final | números reais, tabela de uso das ferramentas e as lacunas |

## Como saber que terminou bem

1. O relatório final está completo, com números medidos, não com adjetivos.
2. A tabela de uso mostra cada ferramenta instalada, o comando exato e o resultado.
3. O clone abre, você clica nas telas e ele responde igual ao original.
4. O que não foi alcançado está declarado como lacuna, com o que foi tentado.
5. O portão de entrega fechado está colado na conversa, cru.

Se o agente disser "deve funcionar", o trabalho não acabou. Volte e exija o teste clicando.

## Se o agente parar no meio

A tabela completa de sintomas, com a resposta pronta para cada caso, está em
`EXECUTAR-TUDO.md`. As três mais comuns:

| Sintoma | O que responder |
|---|---|
| pergunta permissão a cada fase | `autorizado, siga sem parar` (só uma vez) |
| resume a fase em vez de fazer | `fase não cumprida: rode de verdade e mostre a saída` |
| trava na mesma fase 3 vezes | troque o modelo: rode `SEM-TRAVA/TESTADOR.py` e use o que entrega mais |

A linha dura vem do modelo, não do prompt. Prompt não conserta modelo que se recusa a
trabalhar: ele é trocado.
