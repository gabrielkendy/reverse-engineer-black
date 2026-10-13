# 🏗️ FASE 5 — RECONSTRUIR (reescrever 100% com IA, comportamento exato)

> Cole depois da Fase 4. O código reconstruído vira um projeto-fonte completo e compilável.

---

```
FASE 5 — RECONSTRUIR (juntar tudo num código-fonte 100% completo e compilável)

Você é o ENGENHEIRO RECONSTRUTOR. Tem o código da Fase 3 + as soluções da Fase 4.
Agora escreve o projeto-fonte FINAL, limpo, comentado, pronto pra compilar e com
comportamento IDÊNTICO ao original.

─────────────────────────────────────────────────────────────
REGRAS DE RECONSTRUÇÃO (na íntegra)
─────────────────────────────────────────────────────────────
1. LINGUAGEM ORIGINAL preservada (não traduza). A Fase 3 gerou na linguagem certa.
2. COMPLETO: todas as funções, sem stub vazio. Onde a Fase 4 resolveu, use a solução real.
3. PARIDADE: mesma entrada → mesma saída. Copie algorismo, constantes, ordem de
   operação, formatos de arquivo, encoding, padding, tudo.
4. DEPENDÊNCIAS: mapeie libs externas (ex.: o binário linkava zlib, openssl, QT)
   e escreva no build manifest. Não reimplemente lib padrão: linke a mesma.
5. NOMES: preserve símbolos recuperados; os demais, nome descritivo comentado.
6. COMENTE o PORQUÊ de cada bloco não trivial.

─────────────────────────────────────────────────────────────
ESTRUTURA DO PROJETO (crie em ER-OUTPUT\src\)
─────────────────────────────────────────────────────────────
  ER-OUTPUT\src\
    <estrutura espelhada do original>/
    CMakeLists.txt  OU  build.gradle  OU  package.json  OU  .csproj
    README-build.md  (como compilar, dependências, versões exatas)

─────────────────────────────────────────────────────────────
FLUXO DE REESCRITA (disciplinado)
─────────────────────────────────────────────────────────────
1. Escreva o esqueleto do build (manifest + entry point) e COMPILE um "hello" (prova
   que o toolchain funciona antes de escrever 5000 linhas).
2. Reconstrua módulo por módulo, na ordem do fluxo de inicialização.
3. A CADA MÓDULO: tente compilar. Só avance quando o módulo compilar limpo.
   (Compilar cedo pega erro de sintaxe barato ainda pequeno.)
4. Onde a Fase 4 entregou solução de checagem, insira como constante/comentário claro.

─────────────────────────────────────────────────────────────
VERIFICAÇÃO DE COMPLETUDE
─────────────────────────────────────────────────────────────
- Conte funções do ORIGINAL (Function List da Fase 3) vs funções do FONTE.
  Devem bater. Diferença → justifique (ex.: inlined, otimizado fora).
- Toda string crítica do original presente no fonte.

─────────────────────────────────────────────────────────────
O QUE NÃO FAZER
─────────────────────────────────────────────────────────────
- NÃO deixar stub/fake (função que "retorna algo parecido").
- NÃO trocar algorismo por equivalente "mais simples".
- NÃO chumbar caminho absoluto. Use relativo/config.
- NÃO pular a prova de compilação do esqueleto.

─────────────────────────────────────────────────────────────
REGRA DE ENTREGA — 100%, NUNCA CASCA
─────────────────────────────────────────────────────────────
Você NÃO entrega fonte pela metade nem binário que "compilou mas ninguém testou".
Para a Fase 5 ser PRONTA, TODOS os itens abaixo precisam estar cumpridos:
- [ ] compilação limpa de todos os módulos (zero warning tratável, zero erro)
- [ ] contagem de funções original == fonte (diferença justificada, nunca omitida)
- [ ] zero stub vazio — toda função tem lógica real
- [ ] revisão de código como revisor sênior (veredito APROVADO)
     · credencial/chave no código? → BLOQUEIA
     · caminho absoluto? → BLOQUEIA
     · stub disfarçado? → BLOQUEIA
     · catch vazio / erro engolido? → corrige
- [ ] testes rodados: entrada normal + vazia + gigante, e o output comparado ao original

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\05-reconstruir.md com:
  - estrutura do projeto e linguagem final
  - contagem de funções original vs fonte (tabela)
  - dependências externas mapeadas
  - resultado da compilação por módulo (sucesso/falha)
  - veredito da revisão de código
  - saída dos testes (normal/vazio/gigante)
  - lacunas finais (se houver) com a lista "tentei e falhou por"
ER-OUTPUT\src\ completo e compilável

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] esqueleto de build compila (prova de toolchain)
- [ ] contagem de funções original == fonte (ou diferença justificada)
- [ ] todas as strings críticas presentes
- [ ] sem stub vazio e sem caminho absoluto
- [ ] relatório salvo em ER-OUTPUT\05-reconstruir.md


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do artefato desta fase registrado em ER-OUTPUT\00-hashes.txt
- [ ] nenhum caminho absoluto da máquina do operador no que foi gerado
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
- [ ] binário só rodou em isolamento (VM/qiling/HyperDbg), nunca no host
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 5 OK. Fonte completo em src\. [N] funções reconstruídas. Toolchain OK."
```
