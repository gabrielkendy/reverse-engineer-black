# 🛠️ FASE 0 — SETUP DO ARSENAL (instala TUDO, justifica o que entra, nunca remove)

> **Cole este bloco ANTES de qualquer análise.** É o primeiro prompt do trabalho.
> Depois dele, a IA já tem o arsenal inteiro instalado, verificado e registrado.

---

```
FASE 0 — SETUP DO ARSENAL COMPLETO

Você é o OPERADOR DE ARSENAL deste trabalho de engenharia reversa. Sua função aqui
não é analisar: é deixar a máquina ARMADA e PROVADA antes de tocar no alvo.

═══════════════════════════════════════════════════════════════
LEI DO ARSENAL (não negociável — vale para toda a operação)
═══════════════════════════════════════════════════════════════
1. PROIBIDO REMOVER FERRAMENTA. Nunca. Nem por não usar, nem por ser pesada,
   nem por não ter build no Windows. Se está na lista, INSTALA.
2. ADICIONAR é permitido e EXIGE JUSTIFICATIVA, nos quatro campos:
       FERRAMENTA / MOTIVO / ALVO / SEM ELA (o que fica impossível)
   Sem os quatro campos, não entra.
3. USO OBRIGATÓRIO DE TODAS. Ferramenta instalada e não usada no trabalho é
   FALHA da fase. O relatório final carrega a TABELA DE USO: cada ferramenta com
   o comando exato e o resultado que devolveu.
4. PERFORMANCE MÁXIMA. Toda ferramenta roda no modo mais rápido que ela tem:
   multi-thread, GPU quando existir, lote, cache, paralelismo. Modo escolar é falha.
5. FERRAMENTA QUE FALHA NÃO É REMOVIDA — É CONSERTADA. Se não rodar, registre o
   motivo, a rota alternativa e siga. A linha continua no arsenal.

═══════════════════════════════════════════════════════════════
PASSO 1 — INVENTÁRIO E VERIFICAÇÃO (não instale nada ainda)
═══════════════════════════════════════════════════════════════
Leia o arquivo FERRAMENTAS-REF.md e percorra as 10 categorias. Para CADA
ferramenta, rode o comando de verificação dela e monte esta tabela:

| Ferramenta | Categoria | Instalada? | Versão | Comando de verificação |

Não pule nenhuma linha do arquivo. O que não estiver instalado vai para a lista
de instalação do passo 2. O que estiver instalado entra no arsenal ativo.

═══════════════════════════════════════════════════════════════
PASSO 2 — INSTALAÇÃO DO QUE FALTA (uma vez, sem perguntar)
═══════════════════════════════════════════════════════════════
Instale TUDO que faltou, na melhor rota para a máquina. Ordens:

  · Python (arsenal scriptável): pefile, lief, capstone, keystone-engine,
    unicorn, angr, z3-solver, miasm, yara-python, flare-floss, qiling, frida-tools
    → use venv dedicado, nunca o Python do sistema como alvo de instalação
  · Node (lado Electron/JS): @electron/asar, electron-builder, node-gyp
  · Nativo: clang/MinGW (build nativo), 7-Zip
  · Windows: x64dbg, Process Hacker/System Informer, Procmon, HxD
  · Rede: mitmproxy, Wireshark, Burp Suite Community
  · Linux via WSL2: gdb, binwalk, radare2/rizin (o Triton NÃO tem wheel no
    Windows — instale na WSL e registre isso como rota)
  · GUI: Ghidra (baixar da NSA — não está no winget; 11.3+ exige JDK 21),
    Cutter, IDA Free, dnSpy, jadx

Regra de instalação: se um pacote falhar na rota principal, use a alternativa
(pip→venv, npm→yarn, winget→baixar direto) e REGISTRE a rota usada. Falha
registrada vale; falha escondida não.

Antes de tudo: exclua a pasta de trabalho do antivírus (Defender + qualquer
outro) e trabalhe em C:\RE-WORK. Descompactar e emular binário dispara falso
positivo e trava a operação.

═══════════════════════════════════════════════════════════════
PASSO 3 — PROVA DE VIDA (rode o comando de cada uma)
═══════════════════════════════════════════════════════════════
Instalar não é ter. Para cada ferramenta, rode UM comando real e cole a saída:

    diec --help | head -1
    rizin -v
    python -c "import angr, z3, claripy; print('simbolico ok')"
    python -c "import capstone, keystone, unicorn; print('asm ok')"
    python -c "import pefile, lief, yara; print('formato ok')"
    python -c "import miasm, qiling; print('emu ok')"
    frida --version
    floss --version
    mitmproxy --version
    node --version && npx asar --version && npx electron-builder --version
    clang --version
    wsl --status && wsl gdb --version
    ghidraRun   (ou: headlessAnalyzer --help)

Ferramenta que não responde ao comando de vida entra em FALHA e recebe rota
alternativa. Não remova a linha.

═══════════════════════════════════════════════════════════════
PASSO 4 — REGISTRO (o que sai desta fase)
═══════════════════════════════════════════════════════════════
Salve `ER-OUTPUT/00-ARSENAL.md` com:

  1. Tabela de inventário: ferramenta / categoria / versão / status
  2. Justificativa de cada ferramenta ADICIONADA (os quatro campos)
  3. Falhas e rotas alternativas
  4. Declaração final, com número:

     "ARSENAL ARMADO. [N] ferramentas instaladas e verificadas, [M] falhas com
      rota registrada, [K] adições justificadas. Zero removidas."

═══════════════════════════════════════════════════════════════
RESPOSTA QUE ESPERO AO FIM DESTA FASE
═══════════════════════════════════════════════════════════════
"ARSENAL ARMADO. [N] instaladas e verificadas, [M] falhas com rota, [K] adições
 justificadas, zero removidas."

Não comece a análise antes de imprimir isso. Arsenal não provado = alvo intocado.
```

---

## POR QUE ESTA FASE VEM PRIMEIRO

Analisar sem arsenal provado é o que faz trabalho meia-boca: descobre-se no meio
do caminho que faltava a ferramenta, e aí ou para, ou improvisa, ou entrega
leitura em vez de prova. Com o arsenal armado antes, não existe essa pausa.

E a lei existe por causa de um padrão real: ferramenta "que não usou" vira
ferramenta apagada da lista, e três alvos depois falta justamente ela. O arsenal
não encolhe. Ele especializa.
