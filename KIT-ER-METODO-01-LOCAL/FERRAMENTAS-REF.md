# 🔧 ARSENAL — INVENTÁRIO OBRIGATÓRIO (Método 01)

> **LEI DESTA FASE — leia antes de tudo:**
>
> 1. **PROIBIDO REMOVER FERRAMENTA.** Nem "por não usar", nem "por ser pesada", nem
>    "por não ter no Windows". Se a ferramenta existe na lista, ela é INSTALADA.
> 2. **ADICIONAR é livre, e exige JUSTIFICATIVA.** Toda ferramenta nova entra com:
>    **nome · motivo · alvo · o que fica impossível sem ela.** Sem isso, não entra.
> 3. **USO OBRIGATÓRIO DE TODAS.** Ferramenta instalada e não usada é falha da fase.
>    O relatório final tem a tabela de uso: cada uma com o comando e o resultado.
> 4. **PERFORMANCE MÁXIMA.** Toda ferramenta roda no modo mais rápido disponível
>    (multi-thread, GPU quando houver, lotes, cache). Não rode no modo escolar.
> 5. **FERRAMENTA QUE FALHA NÃO É REMOVIDA — É CONSERTADA.** Se não roda, o motivo
>    e a alternativa entram no relatório. Nunca se apaga a linha.
>
> A lista cresce a cada alvo. Ela nunca encolhe.

---

## COMO USAR ESTE ARQUIVO

- Antes de começar: percorra a lista e confirme instalação (comando de verificação).
- Durante: registre cada uso — comando exato + o que ele devolveu.
- No fim: cole a **TABELA DE USO** no relatório. Linha sem uso registrado reprova a fase.

---

## 1. ANÁLISE ESTÁTICA — estrutura e desmonte

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **Detect It Easy (DIE)** | identifica formato, packer, compilador, arquitetura | primeiro passo de qualquer alvo: você precisa saber COM O QUE está lidando antes de abrir | `diec --help` |
| **radare2 / rizin** | análise por linha de comando, xref, disasm, scripting | triagem rápida e reprodutível em script; base de tudo que é automatizável | `rizin -v` |
| **Cutter** | GUI do rizin | grafo visual de função — enxergar o fluxo sem ler assembly solto | abrir o app |
| **Ghidra** | decompiler C/C++ completo, scripting Java/Python | o decompilado legível é o que transforma 300 linhas de asm em 20 de C | `ghidraRun` / `analyzeHeadless` |
| **IDA Free / Pro** | decompiler + debugger, padrão da indústria | confere o que o Ghidra diz; onde um erra, o outro acerta | abrir o app |
| **capstone** | desmonta bytes em instruções (via script) | é o MOTOR do disasm automatizado: sem ele não se varre `.text` por script | `python -c "import capstone"` |
| **keystone** | monta instruções a partir de texto | prova patch: monta o byte que você quer e testa, sem depender de assembler externo | `python -c "import keystone"` |
| **pefile** | lê cabeçalho/seções/imports de PE | inventário de dependências e seções em milissegundos | `python -c "import pefile"` |
| **LIEF** | parse e MODIFICA PE/ELF/Mach-O | reescrever cabeçalho, IAT, seções sem quebrar o arquivo | `python -c "import lief"` |

## 2. DESEMPACOTAR / ABRIR O CORPO

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **@electron/asar** | extrai e reempacota `app.asar` | 90% dos apps-alvo hoje são Electron; sem isso o corpo fica trancado | `npx asar --version` |
| **upx** | descomprime alvo UPX | alvo empacotado não tem strings nem imports legíveis | `upx -V` |
| **Scylla** (plugin x64dbg) | dump de memória + reconstrução de IAT | alvo com packer que não é UPX: só sai por dump de processo | plugin na pasta do x64dbg |
| **apktool** | desempacota APK → smali + manifest + resources | Android: o manifest e os resources são metade da resposta | `apktool -version` |
| **7-Zip** | abre o que a extensão esconde (exe→zip, cab, msi) | várias vezes é só um arquivo compactado disfarçado | `7z i` |

## 3. DECOMPILAR POR RUNTIME

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **dnSpy / ILSpy** | .NET → C# quase original | .NET não se lê em assembly: se lê em C# | abrir o app |
| **jadx** | DEX → Java legível | Android sem isso é smali ilegível | `jadx --version` |
| **CFR / Procyon / FernFlower** | JAR → Java | mesma razão, para Java desktop | `java -jar cfr.jar --help` |
| **decompyle3 / uncompyle6 / pycdc** | .pyc → Python | alvo Python congelado (PyInstaller/Electron+python) | `python -c "import decompyle3"` |
| **wasm-decompile / wasm2wat** | WebAssembly → texto | cada vez mais app web traz wasm; sem isso é caixa preta | `wasm2wat --version` |

## 4. ANÁLISE AVANÇADA — o diferencial black

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **angr** | execução simbólica: acha o input que chega a um endereço | resolve "que entrada faz isso passar?" sem tentativa e erro | `python -c "import angr"` |
| **Z3 (z3-solver)** | resolve restrições SMT e devolve o valor real | é quem PROVA: transforma "acho que passa" em "passa, e aqui está o valor" | `python -c "import z3"` |
| **Triton** | taint + síntese de restrições | quando o caminho tem muitas variáveis e angr trava | `python -c "import triton"` |
| **Miasm** | IR + emulação manual | quando você precisa entender o que a instrução FAZ, não só onde ela vai | `python -c "import miasm"` |
| **Unicorn** | emula código real sem executar o programa | roda o trecho do binário isolado: prova comportamento sem risco | `python -c "import unicorn"` |
| **Qiling** | emula o binário COM sistema operacional | emula a chamada de sistema, não só a CPU | `python -c "import qiling"` |
| **claripy** (vem com angr) | camada de restrições do angr | escrever a condição de sucesso direto | `python -c "import claripy"` |

## 5. ANÁLISE DINÂMICA / DEBUG

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **x64dbg / x32dbg** | debugger Windows: breakpoint, dump, patch em memória | é onde você VÊ a decisão acontecer | abrir o app |
| **Frida (frida-tools)** | hook em runtime, sem recompilar | intercepta função viva e muda o retorno na hora | `frida --version` |
| **Process Hacker / System Informer** | processos, handles, memória, módulos | mostra o que o app abriu e onde escreveu | abrir o app |
| **API Monitor** | registra chamadas de API do Windows | responde "que arquivo ele tentou abrir?" com prova | abrir o app |
| **Procmon** | file/registry/network em tempo real com filtro | rastro completo de I/O sem palpite | abrir o app |
| **GDB / LLDB** (WSL) | debugger Linux/macOS | alvo ELF/Mach-O não se depura com x64dbg | `gdb --version` |

## 6. BINÁRIO E FORMATO

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **YARA** | regras por assinatura: acha família de código por padrão | varre o binário inteiro por comportamento conhecido | `yara --version` |
| **strings / floss** | extrai strings, inclusive as ofuscadas | metade da resposta está em texto dentro do binário | `floss --version` |
| **binwalk** | acha arquivos embutidos (zip, squashfs, chaves) | firmware e instalador escondem payload | `binwalk --help` |
| **hexdump / 010 Editor / HxD** | editar byte a byte | patch cirúrgico não se faz em IDE | abrir o app |
| **objdump / dumpbin** | seções, símbolos, relocations | segunda opinião sobre o cabeçalho | `objdump --version` |

## 7. REDE

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **mitmproxy** | intercepta e MODIFICA HTTP/HTTPS em tempo real | app que fala com servidor: a resposta está no tráfego | `mitmproxy --version` |
| **Wireshark** | captura e disseca pacote | o que não é HTTP (binário, socket cru) só se vê aqui | abrir o app |
| **Burp Suite (Community)** | proxy com repetidor e scanner | rejogar requisição alterada sem escrever cliente | abrir o app |
| **sslsplit / Frida-ssl** | quebra pinning de certificado | app com certificate pinning recusa o mitmproxy | script carrega |

## 8. BUILD (referência · fora das fases do método)

> O método entrega o app rodando a partir do código reconstruído. As ferramentas abaixo
> continuam no arsenal (a lei é não remover nada): use se você quiser gerar um executável.

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **electron-builder** | reempacota o app Electron | opcional: só se você quiser gerar um executável a partir do código | `npx electron-builder --version` |
| **clang / MinGW / MSVC** | compila nativo (C/C++/Rust) | módulo nativo alterado precisa ser recompilado | `clang --version` |
| **node-gyp / CMake** | build de módulo nativo Node | `.node` não se recompila sem isso | `node-gyp --version` |
| **apksigner + keystore** | assina APK | APK sem assinatura não instala | `apksigner --version` |
| **Android SDK / build-tools** | build Android completo | idem, com aapt2 e d8 | `sdkmanager --version` |

## 9. IDENTIDADE DO CLONE (fase 2.5)

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **`scripts/limpar-identidade.py`** | troca nome, autor, URL, copyright, appId, telemetria | clone com marca do dono é clone ENTREGÁVEL-NÃO | `python scripts/limpar-identidade.py --help` |
| **`scripts/limpar-logo.py`** | troca ícone, logo, imagem de marca; gera ícone novo | texto limpo com ícone do dono continua sendo o dono | `python scripts/limpar-logo.py --help` |
| **`scripts/limpar-total.py`** | roda as duas e emite o relatório | garante o MESMO nome inventado nas duas frentes | `python scripts/limpar-total.py --help` |
| **Librsvg / Inkscape** (opcional) | converte SVG em PNG/ICO em lote | útil quando o clone traz logo vetorial em muitos tamanhos | `inkscape --version` |
| **ImageMagick** | converte, redimensiona e monta ICO em lote | gera o conjunto de ícones de uma vez, todos os tamanhos | `magick -version` |

## 10. APOIO

| Ferramenta | Para que serve | Por que é obrigatória | Verificar com |
|---|---|---|---|
| **Python 3.11+** | roda todo o arsenal scriptável | é o cola: connecta as ferramentas | `python --version` |
| **Node.js LTS + npm** | roda o lado JS/Electron | sem o runtime do alvo o app não roda a partir do código | `node --version` |
| **Git** | versiona cada fase | voltar atrás é requisito, não luxo | `git --version` |
| **WSL2** | roda o arsenal Linux (GDB, ferramentas ELF) | Triton e parte do arsenal não têm wheel no Windows | `wsl --status` |
| **7-Zip** | abre qualquer contêiner | ver item 2 | `7z i` |

---

## TABELA DE USO — COLE NO RELATÓRIO FINAL

Ferramenta instalada sem uso registrado **reprova a fase**. Preencha TODAS.

| # | Ferramenta | Comando exato usado | O que devolveu | Conclusão |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |
| … | | | | |

---

## ADIÇÃO DE FERRAMENTA — MODELO DE JUSTIFICATIVA

Toda linha nova entra assim. Sem os quatro campos, não entra:

```
FERRAMENTA : <nome>
MOTIVO     : <o que ela faz que nenhuma da lista faz>
ALVO       : <em que tipo de alvo ela entra>
SEM ELA    : <o que fica IMPOSSÍVEL fazer. seja específico>
VERIFICAR  : <comando que prova que ela existe e roda>
```

**Exemplo real (linha já aceita no arsenal):**

```
FERRAMENTA : Unicorn
MOTIVO     : executa bytes reais de um trecho do binario sem rodar o programa
ALVO       : modulo nativo (.node/.dll) com funcao de validacao isolavel
SEM ELA    : nao da para PROVAR o comportamento do validador; so descrever o
             assembly, que e leitura, nao prova
VERIFICAR  : python -c "import unicorn; print(unicorn.__version__)"
```

---

## REGRA FINAL

Esta lista **cresce**. Toda vez que um alvo exigir algo que não está aqui, a
ferramenta entra COM justificativa — e as de cima continuam todas instaladas e
todas usadas. O arsenal não encolhe: ele se especializa.
