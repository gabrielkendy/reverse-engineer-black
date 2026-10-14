# 📦 FASE 2 — DESEMPACOTAR (unpack / remover proteção / extrair payload)

> Cole depois da Fase 1. Adapta-se automaticamente ao tipo detectado.

---

```
FASE 2 — DESEMPACOTAR (chegar ao binário REAL, sem packer nem camada)

A Fase 1 disse o que o alvo é. Esta fase remove a casca até sobrar o binário/
código verdadeiro. Um packer não removido agora vira lixo ilegível nas próximas.

─────────────────────────────────────────────────────────────
ROTAS POR TIPO (siga a que a Fase 1 apontou)
─────────────────────────────────────────────────────────────
══ ROTA PE (exe/dll) ══
1. Se UPX:  upx -d alvo-copia -o alvo-unpacked
   Verifique:  sha256 antes/depois e  rabin2 -I  para confirmar section headers limpos.
2. Se Themida/VMProtect (protetores comerciais):
   - NÃO tente desmontar manualmente de cara. Use:
     · Scylla (x64dbg plugin) para dumped + IAT reconstruction
     · ou o modo "dump + fix import" do x64dbg no OEP (Original Entry Point)
   - Receita: sobe no x64dbg → breakpoint em VirtualProtect/WriteProcessMemory →
     segue até o OEP → dump do processo → Scylla reconstrói a IAT → salva unpacked.
   - CASO DURO (VMProtect com VIRTUALIZAÇÃO / Themida Code Virtualizer):
     o dump no OEP devolve seções ainda bytecode de VM. Aqui o unpack tradicional
     NÃO basta. Anote que o alvo tem seções virtualizadas, extraia o que der (IAT,
     imports, entry flow) e marque para DEVIRTUALIZAR na FASE 4 (HyperDbg + angr).
     NÃO gaste horas tentando "dump limpo" — isso não existe pra VM; trabalhe a
     VM na Fase 4.
3. Se .NET: não precisa unpack — é IL. Pule direto pra decompilar (FASE 3, dnSpy).

══ ROTA ELF ══
1. upx -d se packer UPX.
2. Se stripado (sem símbolos):  anote "stripped" — a análise avançada (Fase 4) lida.

══ ROTA APK ══
1. apktool d alvo.apk -o ER-OUTPUT\work\apk-unpacked
   (gera AndroidManifest.xml legível + smali + resources)
2. Se tiver libs nativas (armeabi/*.so), extraia e trate como ELF na Fase 3.
3. Se tiver assets/ index.android.bundle → é React Native → extraia o JS bundle
   (o bundle é o cérebro; trate como FASE 3 JavaScript).

══ ROTA ELECTRON ══
1. npx asar extract app.asar ER-OUTPUT\work\asar-unpacked
2. O cérebro é o JS (main.js, renderer, preload). Vai direto pra FASE 3 como JS.
3. ⚠️ NÃO APAGUE a pasta `app.asar.unpacked\` que fica AO LADO do asar — ela é parte
   do app, não sujeira. Ela guarda os nativos que o Electron se recusa a ler de
   dentro do pacote. Sem ela o app morre no boot.

   MEDIDO (12/10/2026, Content Hub 0.2.25): `app.asar` original = 18,6 MB e
   `app.asar.unpacked\` ao lado com 2 arquivos `.node`. Os nativos ficam DENTRO do
   asar E a pasta existe ao lado. Os dois têm que estar certos.

   ── O ERRO QUE QUEIMA O PACOTE (referência medida, só se você for remontar o pacote) ──
   `unpack` e `unpackDir` NÃO são a mesma coisa:
     · `unpack: '**/*.node'`   → marca o padrão; o asar continua íntegro e grande.
     · `unpackDir: '{**/*.node,**/x}'` → joga ARQUIVO E PASTA inteira pro `.unpacked`.
       Resultado medido: asar cai de 18,6 MB para 6,3 MB e o app abre com a tela
       vermelha "Falha ao iniciar". 6,3 MB é o SINTOMA. Se o seu pacote encolheu
       assim, o culpado é o `unpackDir` largo — não o alvo.

   ── COMO EMPACOTAR CERTO (medido, funcionou) ──
   Compare SEMPRE com o original antes de publicar:
     · nº de entradas do seu pacote == nº do original (medido: 970 = 970)
     · bytes do seu pacote ≈ bytes do original (dentro de 5%)
     · a pasta `.unpacked` ao lado contém os mesmos nativos do original
   Divergiu em qualquer um dos três → NÃO PUBLICAR. É defeito seu.

══ ROTA JAR ══
1. unzip alvo.jar → classes/*.class
2. Use CFR / Procyon / FernFlower para decompilar direto na FASE 3.

══ ROTA PYTHON (bytecode .pyc) ══
1. decompyle3 / uncompyle6 para cada .pyc → .py na FASE 3.

─────────────────────────────────────────────────────────────
CASO SMC (self-modifying code) — binário que se reescreve em runtime
─────────────────────────────────────────────────────────────
Se a Fase 1 flagrou seções .text com write+exec (SMC), o binário "frio" no disco
está ofuscado e só se decripta em memória:
1. Deixe rodar em Qiling/Unicorn (ou x64dbg) até o ponto de decriptação.
2. Faça DUMP do código JÁ decriptado (não do arquivo em disco).
3. Trabalhe com esse dump limpo nas fases seguintes.
NÃO descompilar o binário "frio" ofuscado — é perda de tempo.
─────────────────────────────────────────────────────────────
- Rode "strings" no binário unpacked: as strings REAIS (nomes de função, mensagens)
  devem aparecer agora. Se ainda aparecer só lixo/entropy alta, o unpack falhou.
- Calcule entropy das seções:  seção com entropy > 7.5 ainda está packada/criptada.
- sha256 do unpacked → registre em ER-OUTPUT\00-hashes.txt.

─────────────────────────────────────────────────────────────
O QUE NÃO FAZER
─────────────────────────────────────────────────────────────
- NÃO seguir pra decompilar com seção ainda packada (entropy alta + strings vazias).
- NÃO usar "estimar" o OEP: ache de verdade com o dump no x64dbg.
- NÃO sobrescrever a cópia original da Fase 1; sempre gere um arquivo novo.

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\02-desempacotar.md com:
  - a rota usada (PE/ELF/APK/Electron/JAR/Python)
  - ferramenta + comando exato executado
  - sha256 antes/depois do unpack
  - entropy das seções (antes vs depois)
  - strings novas que apareceram (prova de que funcou)

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] sha256 do unpacked registrado
- [ ] entropy das seções caiu para faixa normal (< 7.0)
- [ ] strings reais visíveis (10+ amostras coladas)
- [ ] relatório salvo em ER-OUTPUT\02-desempacotar.md


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do artefato desta fase registrado em ER-OUTPUT\00-hashes.txt
- [ ] nenhum caminho absoluto da máquina do operador no que foi gerado
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
- [ ] binário só rodou em isolamento (VM/qiling/HyperDbg), nunca no host
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 2 OK. Binário desempacotado em [caminho]. Entropy [antes→depois]."
```
