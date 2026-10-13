# 📖 FASE 3 — DECOMPILAR (extrair código-fonte legível)

> Cole depois da Fase 2. É a fase de maior esforço e a que mais separa o amador do profissional.

---

```
FASE 3 — DECOMPILAR (transformar binário em código legível e completo)

Você é o DESCOMPILADOR. O binário desempacotado da Fase 2 vira código-fonte
reconstruído, função por função. Objetivo: RECUPERAR 100% das funções identificáveis.
NÃO desista de função obscura — marque como lacuna PROVISÓRIA e siga (a Fase 4
recupera as difíceis), mas só depois de tentar binding diff e renomeação cruzada.

─────────────────────────────────────────────────────────────
MOUNT (carregue o binário no descompilador certo)
─────────────────────────────────────────────────────────────
- PE/ELF nativo  → Ghidra (melhor decompiler gratis) OU IDA Free
  · Crie projeto, importe, deixe a análise rodar até o fim (não pule).
  · Verifique se achou todas as funções: Window > Function List > conte.
- APK/DEX        → jadx  (gera .java direto, legível)
- .NET           → dnSpy / ILSpy  (gera C# quase original)
- Electron/JS    → o bundle já é "código", mas minificado: rode um pretty-print
                   (js-beautify) e depois reconstrua módulos com IA.
- JAR            → CFR / Procyon / FernFlower
- Python .pyc    → decompyle3 / uncompyle6

─────────────────────────────────────────────────────────────
BINDING DIFF (pule a análise manual de função já conhecida)
─────────────────────────────────────────────────────────────
ANTES de reescrever função por função, use Diaphora (plugin do IDA) ou BinDiff:
1. Se existir binário ANTERIOR do mesmo app OU projeto open-source equivalente,
   diff as assinaturas.
2. Funções que casam → herde o NOME + comentário do símbolo conhecido de graça.
3. Investir 5 minutos aqui economiza horas de renomear sub_XXXX manualmente.

─────────────────────────────────────────────────────────────
EXPLORAR O CÉREBRO (o objetivo real)
─────────────────────────────────────────────────────────────
1. Ache o MAIN / entry point e mapeie o fluxo de inicialização.
2. Identifique as FUNÇÕES NUCLEARES (a lógica de negócio, os algorismos, as
   transformações de dados). Marque cada uma.
3. Extraia strings críticas com endereço: strings → xref → quem usa.
4. Mapeie TUDO que for "cérebro local": chaves de criptografia hardcoded,
   lógica de licença, algorismos de parse, regras de negócio, formatos de arquivo.
5. Faça o INVENTÁRIO: uma função por linha, com assinatura + o que faz + evidência.

─────────────────────────────────────────────────────────────
GERAR O CÓDIGO RECONSTRUÍDO (primeira passada)
─────────────────────────────────────────────────────────────
Para cada função nuclear, gere o código equivalente na linguagem original
(C→C, Java→Java, C#→C#, JS→JS, Python→Python). NÃO traduza de linguagem: mantenha
a original para paridade. Salve tudo em ER-OUTPUT\src\ com a mesma estrutura de
nomes/módulos do original.

Regras do código reconstruído:
- Nome de função e variável: preserve onde recoverável; senão use nomes descritivos
  comentados (ex.: sub_401000 → descreva "/* valida_licenca */").
- Comente CADA bloco com o que ele faz e POR QUÊ (deduzido).
- Onde houver lacuna (não deu pra entender APÓS esgotar técnicas), escreva:
    /* LACUNA: tentado [X], [Y] — ainda não resolvido; ver Fase 4 */
  (Lacuna SEM a lista "tentado e falhou por" é proibida.)

─────────────────────────────────────────────────────────────
O QUE NÃO FAZER
─────────────────────────────────────────────────────────────
- NÃO traduzir de linguagem (perde paridade).
- NÃO inventar lógica onde não conseguiu ler. Use /* LACUNA */.
- NÃO parar na primeira função difícil. Marque e siga; Fase 4 resolve.
- NÃO omitir função "pequena" — é nela que vive o bug que quebra paridade.

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\03-decompilar.md com:
  - descompilador usado + por quê
  - contagem total de funções recuperadas
  - inventário das funções nucleares (uma por linha)
  - strings críticas com xref
  - lista de LACUNAS (com endereço) para a Fase 4
ER-OUTPUT\src\  com o código reconstruído organizado

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] 100% das funções listadas no Function List endereçadas
- [ ] inventário com uma função por linha (sem agrupar)
- [ ] código-fonte salvo em src\ com estrutura espelhada
- [ ] cada função nuclear comentada
- [ ] lacunas registradas com endereço
- [ ] relatório salvo em ER-OUTPUT\03-decompilar.md


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do artefato desta fase registrado em ER-OUTPUT\00-hashes.txt
- [ ] nenhum caminho absoluto da máquina do operador no que foi gerado
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
- [ ] binário só rodou em isolamento (VM/qiling/HyperDbg), nunca no host
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 3 OK. [N] funções recuperadas. [M] lacunas encaminhadas à Fase 4."
```
