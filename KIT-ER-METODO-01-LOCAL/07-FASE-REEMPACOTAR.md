# 📦 FASE 6 — REEMPACOTAR (rebuild + assinatura + formato final)

> Cole depois da Fase 5. O fonte vira de novo um artefato distribuível e funcional.

---

```
FASE 6 — REEMPACOTAR (o código reconstruído volta a ser um app que roda)

Você é o ENGENHEIRO DE BUILD. O projeto-fonte da Fase 5 vira um binário/artefato
final, com assinatura e empacotamento corretos, pronto para distribuir e rodar.

─────────────────────────────────────────────────────────────
BUILD POR ALVO
─────────────────────────────────────────────────────────────
══ NATIVO (C/C++/Rust/Go) ══
1. Compile com o toolchain da Fase 0 (clang/MinGW/MSVC), flags de otimização
   equivalentes às detectadas na Fase 1 (ex.: -O2). Mantenha arquitetura (x86/x64).
2. Se era .dll, gere o export table igual (os mesmos símbolos exportados).
3. Se havia anti-tamper (checksum próprio), recalcule/insira o valor correto da Fase 4.

══ .NET ══
1. dotnet build -c Release. Preserve assembly name, version, public key se havia.

══ APK ══
1. jadx/Android Studio monta o projeto; gradle assembleRelease.
2. Assine:  keytool -genkeypair ...  +  apksigner sign --ks minha-key.jks
3. Se havia keystore original (debug key), assine com equivalente e documente.

══ ELECTRON ══
1. npm install (deps do Fase 5) → npm run build → npx electron-builder
2. Re-empacote o asar:  npx asar pack app ER-OUTPUT\build\app.asar
3. Preserve deep links/config detectados na Fase 1 (ex.: protocolo customizado).
4. ⚠️ EMPACOTAR DO JEITO QUE O ORIGINAL É — não do jeito que parece certo.
   O erro nº 1 aqui (medido 12/10/2026, custou 2 pacotes) é usar `unpackDir` largo:

     ❌ ERRADO → asar 18,6 MB vira 6,3 MB, app abre com "Falha ao iniciar"
        asar.createPackageWithOptions(src, dst, {
          unpackDir: '{**/*.node,**/node_modules/better-sqlite3/**}'
        })

     ✅ CERTO → asar mantém o tamanho; `.unpacked\` ao lado com os nativos
        asar.createPackageWithOptions(src, dst, { unpack: '**/*.node' })
        (e COPIE a pasta `app.asar.unpacked\` do original para o lado do seu asar)
   `unpack` marca; `unpackDir` expulsa o pacote inteiro pra fora. Use `unpack`.

5. CONFERÊNCIA OBRIGATÓRIA ANTES DE PUBLICAR (cole os 3 números):
   - entradas do SEU asar  == entradas do ORIGINAL   (medido: 970 = 970)
   - bytes do SEU asar     ≈ bytes do ORIGINAL       (dentro de 5%)
   - `.unpacked\` ao lado com os MESMOS nativos do original (medido: 2 arquivos .node)
   Falhou qualquer um → NÃO publique. Reempacote. Não culpe o alvo.

══ JAR ══
1. javac das classes → jar cfm (preserve MANIFEST/Main-Class).

─────────────────────────────────────────────────────────────
VERIFICAÇÃO DO BUILD (obrigatória — PADRÃO DEV PRO)
─────────────────────────────────────────────────────────────
- O artefato final ABRE e passa do entry point sem crash.
- Rode um smoke test: o app abre, a tela/processo sobe, não crasha em 30s.
- Compare tamanho/estrutura com o original (não precisa ser idêntico, mas anote).
- sha256 do artefato final → ER-OUTPUT\00-hashes.txt.
- Se havia anti-tamper/checksum: PROVE que o binário aceita a própria assinatura
  (rode e confirme que NÃO dispara "tamper detected").
- Se o original era assinado (Authenticode/keystore): assine o seu, mesmo que com
  cert auto-assinado, e documente — binário sem assinatura é entregue CASCA.

─────────────────────────────────────────────────────────────
O QUE NÃO FAZER
─────────────────────────────────────────────────────────────
- NÃO entregar só o .exe nu se o original era instalador/AppBundle/APK.
- NÃO assinar com key nova sem documentar (o operador precisa saber que repetiu o processo).
- NÃO pular o smoke test — "compilou" ≠ "roda".

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\06-reempacotar.md com:
  - comando de build exato
  - artefato final (caminho) + sha256
  - resultado do smoke test (abriu? crasha? prints/evidência)
  - diferenças de tamanho/estrutura vs original
ER-OUTPUT\build\ com o artefato final

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] build completou sem erro
- [ ] artefato final abre e roda 30s sem crash
- [ ] assinatura/empacotamento feito e documentado
- [ ] sha256 do artefato registrado
- [ ] (Electron) entradas do pacote == original E bytes dentro de 5%
- [ ] (Electron) `.unpacked\` ao lado com os mesmos nativos do original
- [ ] relatório salvo em ER-OUTPUT\06-reempacotar.md


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do artefato desta fase registrado em ER-OUTPUT\00-hashes.txt
- [ ] (Electron) paridade de pacote medida: entradas + bytes + nativos vs original
- [ ] o app abre SEM tela de erro e sem lista vazia (medido, não "deve abrir")
- [ ] se abriu com erro: a causa foi lida no LOG do app, não suposta
- [ ] nenhum caminho absoluto da máquina do operador no que foi gerado
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
- [ ] binário só rodou em isolamento (VM/qiling/HyperDbg), nunca no host
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 6 OK. Artefato final em build\. Smoke test passou (ou falha X a corrigir)."
```
