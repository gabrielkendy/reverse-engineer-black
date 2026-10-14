# 🧬 KIT ER BLACK — MÉTODO 01 (App 100% Local / Cérebro Local)

> **O que é:** um pacote drop-in de arquivos que instrui QUALQUER IA a fazer Engenharia Reversa
> completa de um aplicativo local, do `setup` ao código reconstruído e provado em paridade.
> O operador só fornece **o nome do app** e **o caminho da pasta local**. O resto a IA faz.

---

## 🚀 COMO USAR (90 segundos)

1. **Abra sua IA** (Claude, ChatGPT, DeepSeek, Codex, Qwen, qualquer uma com acesso a shell/ferramentas).
2. **Cole o `00-PROMPT-MESTRE.md`** na íntegra como primeira mensagem.
3. Quando ele pedir, forneça **SÓ** estas duas coisas:
   - `NOME_DO_APP` — ex.: `WinRAR`, `KeePass`, `StardewValley`
   - `CAMINHO_LOCAL` — ex.: `C:\Alvos\winrar-instalador.exe` ou `C:\Alvos\meu-app\`
4. **Não faça mais nada.** A IA lê o prompt mestre, segue as fases na ordem, instala as
   ferramentas, decompila, reconstrói, corrige bugs e entrega o app rodando a partir do código.

---

## 🔒 LEI DO ARSENAL (vale para toda a operação)

1. **PROIBIDO REMOVER FERRAMENTA.** Nunca. Se está na lista, instala.
2. **ADICIONAR exige JUSTIFICATIVA**: nome · motivo · alvo · o que fica impossível sem ela.
3. **USO OBRIGATÓRIO DE TODAS.** Ferramenta instalada e não usada reprova a fase.
   O relatório final carrega a TABELA DE USO: cada uma com o comando exato e o resultado.
4. **PERFORMANCE MÁXIMA.** Toda ferramenta no modo mais rápido que ela tem.
5. **FERRAMENTA QUE FALHA NÃO É REMOVIDA — É CONSERTADA.** Registra motivo + rota alternativa.

> O arsenal nunca encolhe. Ele se especializa.

---

## 📂 ESTRUTURA DO KIT

| Arquivo | O que contém | Quando a IA usa |
|---------|--------------|-----------------|
| `README.md` | Este guia | Você (operador) |
| `00-PROMPT-MESTRE.md` | O prompt único que orquestra TUDO + gate de segurança + regra da prova | Primeira mensagem |
| `01-SETUP-INSTALACAO.md` | **Fase 0** — instala o arsenal INTEIRO, prova de vida, justificativa, tabela de uso | Início automático |
| `02-FASE-RECONHECIMENTO.md` | Fase 1 — triagem, hashes, tipo de binário, categoria A/B | Automática |
| `03-FASE-DESEMPACOTAR.md` | Fase 2 — unpack/proteção/asarm/apktool/asar | Automática |
| `02b-FASE-LIMPEZA-IDENTIDADE.md` | **Fase 2.5** — o clone nasce inventado: nome, logo, ícone, autor (scripts + gate) | Depois de desempacotar |
| `04-FASE-DECOMPILAR.md` | Fase 3 — extrair código-fonte legível | Automática |
| `05-FASE-ANALISE-AVANCADA.md` | Fase 4 — ofuscação, angr/Triton/Z3, caminhos difíceis | Automática |
| `06-FASE-RECONSTRUIR.md` | Fase 5 — reescrever 100% com IA | Automática |
| `07-FASE-VALIDAR.md` | Fase 6 — paridade 100% (mesma entrada → mesma saída) | Automática |
| `08-CHECKLIST-FINAL.md` | Checklist de paridade + entrega | Fim |
| `FERRAMENTAS-REF.md` | Inventário obrigatório do arsenal (10 categorias) + modelo de justificativa | Consulta + Fase 0 |
| `scripts/limpar-identidade.py` | Troca nome, autor, URL, copyright, appId, telemetria | Fase 2.5 |
| `scripts/limpar-logo.py` | Gera e troca ícone/logo; acha nome visível | Fase 2.5 |
| `scripts/limpar-total.py` | Orquestra as duas + relatório único | Fase 2.5 |

> **Padrão e validação:** o `../PADRAO-KIT-ER.md` define a ossatura que toda fase segue
> (anatomia + gate + regra da prova + severidade). O `../VALIDAR-KIT.py` mede o KIT sem
> opinião — rode `python VALIDAR-KIT.py --todas` para conferir a nota antes de entregar.

---

## 🧼 FASE 2.5 — POR QUE ELA EXISTE

Clone com marca do dono **não é clone entregável**. A Fase 2.5 apaga a identidade do
original e põe uma identidade inventada por script, de forma determinística:

- **Nunca** usa nome, logo, ícone ou fonte do seu computador
- **Nunca** renomeia arquivo de código (quebraria `require`/`import`)
- **Preserva** `main`, entry points e estrutura
- **Lista como pendência** o que só existe em binário (a Fase 3 trata)
- **Verificação obrigatória:** grep da identidade original tem que dar ZERO em texto

Rode primeiro em `--dry`, leia a amostra, depois grave. Sempre em cópia de trabalho.

---

## 🔧 O QUE A IA VAI INSTALAR (resumo de espaço em disco)

| Categoria | Ferramentas | ≈ Espaço |
|-----------|-------------|----------|
| Descompiladores pesados | Ghidra, IDA Free, JEB | ~3–6 GB |
| Análise estática | radare2/rizin, Cutter, capstone, keystone, pefile, LIEF, DIE | ~1 GB |
| Mobile/desktop unpack | apktool, jadx, dnSpy/ILSpy, @electron/asar, upx, Scylla | ~1.5 GB |
| Python malha de análise | angr, Triton, Z3, Miasm, claripy, decompyle3/pycdc | ~2 GB |
| Dinâmica | Frida (tools + gadget), x64dbg/x32dbg, GDB/LLDB, qiling/Unicorn | ~2 GB |
| Binário/formato | YARA, floss, binwalk, HxD | ~0.5 GB |
| Rede | mitmproxy, Wireshark, Burp Suite Community | ~0.5 GB |
| Build/empacotar | MSVC/MinGW/clang, electron-builder, node-gyp, Android SDK/keystore | ~5–10 GB |
| Identidade do clone | ImageMagick/Inkscape (opcional) + os 3 scripts do kit | ~0.5 GB |

> **Total realista: 15–25 GB** se instalar a stack completa. Com subset essencial: ~8–12 GB.

---

## ⚠️ REGRAS DE OURO (a IA aplica automaticamente, mas você deve saber)

1. **Sempre em cópia** — nunca reverter o binário original. `sha256sum` no início e no fim.
2. **Fato ≠ inferência** — o que não foi observado é LACUNA, nunca conclusão.
3. **Paridade = comportamento idêntico** — mesma entrada produz mesma saída. Não é "parecido".
4. **Sandbox** para binário suspeito — rodar em VM/qiling antes de confiar.
5. **Path relativo, nunca chumbado** — o código reescrito não carrega caminho absoluto da sua máquina.
6. **Clone nasce inventado** — nenhum nome, logo, ícone ou autor do original sobrevive (Fase 2.5).
7. **Arsenal não encolhe** — ferramenta nunca é removida; só adicionada com justificativa.

---

## ✅ RESULTADO ESPERADO

Ao fim das fases, você tem:
- Código-fonte reconstruído (legível, comentado, sem ofuscação)
- App rodando a partir do código reconstruído (mesmo comportamento do original)
- Clone com identidade inventada, sem resquício do dono original
- Relatório completo por fase salvo em `ER-OUTPUT\`
- Checklist de paridade 100% preenchido

---

*Próximo passo: abrir `00-PROMPT-MESTRE.md` e colar na IA.*
