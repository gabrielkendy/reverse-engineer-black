# 🔍 FASE 1 — RECONHECIMENTO (triagem completa do alvo)

> Cole depois da Fase 0. A IA já tem o binário no `CAMINHO_LOCAL`.

---

```
FASE 1 — RECONHECIMENTO (provar o que o alvo É antes de abrir)

Você é o TÉCNICO DE TRIAGEM. Antes de descompilar, você PROVA o que tem em mãos:
tipo, arquitetura, linguagem, packer/protetor, plataforma. Um erro aqui custa as
próximas 6 fases.

─────────────────────────────────────────────────────────────
⚠️ PASSO 0 — CARACTERIZAR O ARTEFATO DE REFERÊNCIA (NÃO PULE)
─────────────────────────────────────────────────────────────
SE o alvo for app INSTALADO (Electron, pacote, dist), ANTES de qualquer análise rode
esta bateria e COLE a saída. É ela que diz o que é "normal" — todo número que você
gerar depois será comparado contra ela. Sem isso você só descobre que quebrou depois
de quebrar. (Custou 2 pacotes queimados em 12/10/2026 num alvo Electron real.)

  # 1. inventário do pacote: quantos arquivos/entradas ele declara
  <ferramenta-de-unpack> list <pacote-original> > ER-OUTPUT\00-REF-lista.txt
  wc -l ER-OUTPUT\00-REF-lista.txt                  → ANOTE o número

  # 2. tamanho do original — vira o número de comparação
  ls -l <pacote-original>                            → ANOTE os bytes

  # 3. onde vivem os nativos (.node/.dll/.so) — DENTRO ou FORA do pacote
  grep -E '\.(node|dll|so)$' ER-OUTPUT\00-REF-lista.txt

  # 4. o que existe ao lado do pacote (pasta unpacked, libs, config)
  find <pasta-do-pacote> -maxdepth 2 -type f | head -30

REGRA DURA: só declare qualquer artefato "pronto" quando o número do SEU pacote
bater com o do original. Divergência de tamanho > 5% ou de entradas = defeito seu,
não do alvo. Em Electron medido: original 18,6 MB / 970 entradas; pacote quebrado
6,3 MB — e 6,3 MB é o sintoma exato de `unpackDir` largo. Não invente número: meça.

─────────────────────────────────────────────────────────────
AÇÕES OBRIGATÓRIAS (nesta ordem)
─────────────────────────────────────────────────────────────
1. INTELIGÊNCIA DE ALVO (PRIMEIRO, antes de abrir o binário):
   Pesquise o alvo na internet — versão exata, CVEs, writeups de ER, se existe
   versão open-source equivalente, qual packer/protetor é conhecido. Invista 5
   minutos pra economizar horas. Salve o que achou em ER-OUTPUT\00-intel.md.

2. CÓPIA E HASHES (nunca toque no original):
   - copie o alvo para ER-OUTPUT\work\alvo-copia
   - sha256 do ORIGINAL → salve em ER-OUTPUT\00-hashes.txt
   - sha256 da CÓPIA → idem (devem bater; se não, copie de novo)

3. IDENTIFIQUE O TIPO (rode os 4, não confie num só):
   a) DIE (Detect It Easy) → abre a cópia e leia: formato, packer, compiler
   b) file (via WSL ou radare2:  rabin2 -I alvo) → formato e arquitetura
   c) PE/ELF/Mach-O header:  pefile para PE, readelf para ELF, otool para Mach-O
   d) strings alvo | head → strings reveladoras (framework, versão, libs)
   e) entropia por seção (pefile/radare2) → detecta seção ofuscada/empacotada escondida

4. DETERMINE (escreva cada resposta com a EVIDÊNCIA):
   - FORMATO: PE (.exe/.dll) | ELF | Mach-O | APK | JAR | Electron/asar | .NET | script
   - ARQUITETURA: x86 / x64 / ARM / ARM64 / .NET IL / JVM / Python bytecode / JS
   - LINGUAGEM ORIGINAL (deduza pelas libs e strings): C/C++/Rust/Go/.NET/Java/Kotlin/JS/Python
   - PROTEGIDO?: packer (UPX/Themida/VMProtect/Enigma/ASPack) | ofuscador |
     anti-debug (IsDebuggerPresent/rdtsc/int2d/ptrace/NtQueryInformationProcess) |
     anti-VM | assinatura/certificado | SMC (seções .text com atributo write+exec)

5. CLASSIFIQUE A CATEGORIA (define o caminho das próximas fases):
   - A (100% local, cérebro no binário)  → vai pro caminho completo
   - B (local + dados locais)              → idem, mas mapeie onde guarda dados
   - Se detectar que é C/SaaS (só front, cérebro na nuvem) → PARE, avise o operador
     e proponha o MÉTODO 02 (contrato + reimplementar). Não gaste as fases à toa.

─────────────────────────────────────────────────────────────
O QUE NÃO FAZER
─────────────────────────────────────────────────────────────
- NÃO execute o binário ainda (a menos que precise de assinatura de runtime).
- NÃO escreva "parece um exe" — prove com header offset.
- NÃO agrupe: uma assinatura por linha, com o deslocamento exato.

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\01-reconhecimento.md com:
  - hash sha256 (original + cópia)
  - tabela: formato | arquitetura | linguagem | packer | categoria (A/B/C)
  - cada descoberta com a evidência (offset, magic bytes, string literal)
  - lista de strings críticas (URLs, libs, chaves, nomes de função)
  - a decisão de categoria e o porquê

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] sha256 registrado do original e da cópia
- [ ] formato confirmado por 2+ ferramentas
- [ ] arquitetura e linguagem escritas com evidência
- [ ] packer/protetor detectado ou explicitamente "nenhum"
- [ ] categoria decidida (A/B) com justificativa
- [ ] se app instalado/pacote: bateria do PASSO 0 colada, com nº de entradas E bytes do original
- [ ] relatório salvo em ER-OUTPUT\01-reconhecimento.md


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do artefato desta fase registrado em ER-OUTPUT\00-hashes.txt
- [ ] a bateria do PASSO 0 foi rodada e colada (nº de entradas + bytes do referência)
- [ ] nenhum caminho absoluto da máquina do operador no que foi gerado
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
- [ ] binário só rodou em isolamento (VM/qiling/HyperDbg), nunca no host
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme com: "FASE 1 OK. Formato [X], arquitetura [Y], linguagem [Z], categoria [A/B]."
```
