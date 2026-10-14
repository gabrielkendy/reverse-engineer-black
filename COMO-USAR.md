# Como usar o ER BLACK (passo a passo, sem jargão)

## O que esse pacote faz

Você aponta um aplicativo no seu computador e a sua IA reconstrói ele **funcionando**:
desmonta, entende por dentro, monta de volta, testa clicando e entrega.

Você não precisa entender de ferramenta nenhuma. A IA instala o que precisa e te avisa.

## Antes de começar

- **Windows** com acesso à internet (a IA instala o arsenal na primeira fase).
- **Espaço em disco**: separe uns 20 GB livres. App grande pede mais.
- **Tempo**: de algumas horas a alguns dias, dependendo do app. App pequeno termina no mesmo dia.
- **Uma pasta só para o trabalho**: crie algo tipo `C:\ER-TRABALHO\` e coloque o alvo lá dentro.
  Trabalho nunca é feito no original. O original fica intocado.

---

## Os dois prompts (por onde começar)

O repositório traz dois prompts numerados, feitos para colar um depois do outro:

| # | Arquivo | O que faz |
|---|---|---|
| 01 | `PROMPT-01-INSTALAR.md` | baixa o repositório, instala o arsenal e prova cada ferramenta |
| 02 | `PROMPT-02-EXECUTAR.md` | roda o método inteiro sozinho, do reconhecimento ao clone validado |

Cole o 01, espere o arsenal ficar provado, e cole o 02 com o nome do app e a pasta. Os caminhos
abaixo fazem o mesmo por outros atalhos.

## Caminho 1 · Qualquer IA com shell (jeito mais rápido)

Serve para Claude, ChatGPT, DeepSeek, Qwen, Codex e qualquer IA capaz de rodar comando
no seu computador.

1. Abra o arquivo `KIT-ER-METODO-01-LOCAL/00-PROMPT-MESTRE.md`
   (ou `KIT-ER-METODO-02-SAAS/00-PROMPT-MESTRE.md`, se o alvo for um sistema web com API por baixo).
2. **Selecione tudo e cole inteiro** na sua IA, como **primeira** mensagem da conversa.
3. A IA vai perguntar duas coisas:

   | Ela pergunta | Você responde |
   |---|---|
   | Nome do aplicativo | ex.: `WinRAR` |
   | Caminho local | ex.: `C:\ER-TRABALHO\winrar-instalador.exe` |

4. Depois disso, só acompanhe. Ela segue as fases e vai te mostrando o que fez.

## Caminho 2 · Agente que roda dentro da pasta (Claude Code, Codex, Cursor)

```bash
git clone https://github.com/gabrielkendy/reverse-engineer-black.git
cd reverse-engineer-black
```

Abra o seu agente **dentro dessa pasta** e diga o que você quer reconstruir.
Ele já lê o `AGENTS.md` e as skills de `.claude/skills/`, então entra sabendo o método,
as regras e o portão de entrega.

## Caminho 3 · Agente que usa pasta de skills (Hermes e afins)

```bash
cp -r .claude/skills/* ~/caminho/das/suas/skills/
```

Depois disso, basta pedir: "faz engenharia reversa desse app".

---

## O que a IA vai produzir

Tudo aparece numa pasta chamada `ER-OUTPUT/`, criada ao lado do trabalho:

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

1. O relatório final está completo, com números, não com adjetivos.
2. A tabela de uso mostra **cada** ferramenta instalada, o comando exato e o resultado.
3. O clone abre, você clica nas telas e ele responde igual ao original.
4. O que não foi alcançado está declarado como **lacuna**, com o que foi tentado.

Se a IA disser "deve funcionar", o trabalho não acabou. Volte e exija o teste clicando.

## Duas armadilhas comuns

- **Trabalhar no original.** Não faça. Sempre cópia, sempre com o hash guardado.
- **Pular ferramenta.** Se uma ferramenta falhar, ela é consertada ou substituída com o motivo
  escrito. Ela nunca é apagada da lista.

## Validar o pacote

```bash
python3 VALIDAR-KIT.py --todas
```

Tem que dar `100%` nos dois kits. O portão só lê: nunca escreve, nunca move, nunca apaga.
