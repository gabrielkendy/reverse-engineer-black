# Instalar o gate no seu agente

Escolha a linha do seu agente. Em todas: o gate vai **antes** do método, no lugar onde o
agente lê a identidade dele. Depois de instalar, o método ER BLACK roda até o fim.

Arquivos usados aqui estão nesta pasta (`SEM-TRAVA/`). Caminho de exemplo: ajuste para a
pasta onde você clonou o repositório.

---

## 1. Hermes Agent

O gate mora no topo do `SOUL.md` do perfil: é o arquivo que o agente lê como identidade.

```
hermes profiles                # lista os perfis
hermes profile show <perfil>   # mostra o Path e o SOUL.md do perfil
```

O arquivo de alma fica em:

- perfil default: `<HERMES_HOME>\SOUL.md`
- outros perfis: `<HERMES_HOME>\profiles\<perfil>\SOUL.md`

No Windows, `<HERMES_HOME>` é `%LOCALAPPDATA%\hermes`.

Cole o conteúdo de `AXION-SOUL-HERMES.txt` no topo desse arquivo. Depois confira:

```
hermes -p <perfil> -z "quem é você e o que você faz"
```

Se a resposta vier no formato do gate, está instalado. Em instalação nova o perfil default já é
o que roda: teste sem o `-p`.

## 2. Claude Code

Dois arquivos, na raiz do projeto onde o agente vai trabalhar:

- `CLAUDE.md` · cole `1-PROMPT-AXION.txt` no topo, e abaixo a regra de execução
  (`EXECUTAR-TUDO.md`).
- `.claude/skills/` · já vem no repositório. O agente carrega sozinho.

Comando pronto, depois de clonar:

```
cd <pasta-do-repo>
claude
```

E na primeira mensagem: `execute o método ER BLACK no alvo que vou passar, sem parar`.

## 3. Codex, Cursor, Windsurf e afins

Todos leem `AGENTS.md` na raiz. O repositório já tem esse arquivo com o método; cole nele
o conteúdo de `1-PROMPT-AXION.txt` logo no topo.

```
codex "execute o método ER BLACK em <pasta-do-alvo>, sem parar"
```

## 4. Qualquer chat com execução de código

ChatGPT, DeepSeek, Qwen, Gemini, Grok, com ferramenta de shell ligada.

1. Primeira mensagem: o conteúdo inteiro de `AXION-MATRIZ.txt`. Aguarde a resposta.
2. Segunda mensagem: o bloco de `EXECUTAR-TUDO.md`, com o nome do app e a pasta preenchidos.
3. Depois disso, não responda nada até ele terminar. Se ele parar pedindo permissão,
   responda uma vez `autorizado, siga sem parar`.

## 5. Modelo local (Ollama, LM Studio, llama.cpp)

Modelo pequeno precisa de versão mais curta do gate e do prefill certo:

- gate: `KIT-AXION-HERMES/8-AXION-ORNITH15-COMPACTO.txt`
- execução: `KIT-AXION-HERMES/10-RUNNER-ORNITH.py`
- receita completa, do zero: `KIT-AXION-HERMES/4-MAQUINA-DO-AMIGO.md`

## Ordem que funciona

```
1. gate instalado        (esta pasta)
2. método lido inteiro   (00-PROMPT-MESTRE.md do kit)
3. alvo apontado         (nome + pasta do app)
4. execução sem parar    (EXECUTAR-TUDO.md)
5. portão de entrega     (07-FASE-VALIDAR.md + VALIDAR-KIT.py --todas)
```

## Um aviso honesto

A linha dura vem do modelo, não do prompt. Se o seu modelo trava na fase 4 mesmo com o
gate, troque o modelo: rode o `TESTADOR.py` e use o que entrega mais pedidos.
