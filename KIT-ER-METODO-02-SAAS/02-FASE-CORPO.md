# 📦 FASE 1 — CLONAR O CORPO (extrair, rebrand e rodar o cliente)

> Reusa o MÉTODO 01 integralmente para o cliente. Aqui resume e foca no rebrand.

---

```
FASE 1 — CLONAR O CORPO (o cliente extraído, rebrandado e rodando)

O cliente de um SaaS é o CORPO: telas, rotas, chamadas de API, deep links. Você o
extrai, troca a marca (rebrand) e roda. Para a mecânica de descompilar, siga
o MÉTODO 01 (fases 1–6). Aqui o foco é o que é ESPECÍFICO de SaaS:

─────────────────────────────────────────────────────────────
AÇÕES
─────────────────────────────────────────────────────────────
1. Identifique o cliente (reusa Método 01, Fase 1): Electron/asar? React Native?
   .NET? APK? Web (PWA)? Anote o tipo e a linguagem.

2. Extraia o código do cliente:
   - Electron →  npx asar extract app.asar ER-OUTPUT\front-clonado\
   - APK       →  apktool d + jadx
   - .NET      →  dnSpy/ILSpy
   - Web/PWA   →  baixe os assets (js/css) servidos

3. REBRAND (trocar a marca pelo teu nome, NÃO o funcionamento):
   - Nome, logo, strings de UI (títulos, labels, mensagens).
   - Domínio/endpoint que o cliente chama  →  troque pelo TEU backend (mais tarde, Fase 5).
   - Deep link/protocolo customizado (ex.: granola:// → anota://).
   - IDs de app OAuth (Google client_id), se houver.

4. NÃO REBRANDE AINDA o shape de dados nem as rotas internas — o contrato (Fase 2)
   depende delas ainda intactas.

5. Rode o cliente a partir do código e faça smoke test: o app abre e mostra as telas.

─────────────────────────────────────────────────────────────
O QUE NÃO FAZER
─────────────────────────────────────────────────────────────
- NÃO edite os shapes de request/response ainda (quebraria a Fase 2).
- NÃO chumbar teu endpoint se ainda não sabe o contrato — deixe uma const central
  (ex.: API_BASE_URL) para trocar na Fase 5.
- NÃO apague código "morto": é nele que moram endpoints de perfumaria a mapear.

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\01-corpo.md com:
  - tipo de cliente + linguagem + como extraiu
  - o que foi rebrandado (nome/logo/strings/domínio/deep link)
  - onde ficou a const API_BASE_URL (para a Fase 5)
  - smoke test do front rodando a partir do código
ER-OUTPUT\front-clonado\  com o cliente extraído

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] cliente extraído e fonte acessível
- [ ] rebrand aplicado (nome/logo/deep link)
- [ ] API_BASE_URL centralizada (1 lugar só)
- [ ] smoke test: front abre e renderiza


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do cliente original salvo antes de qualquer escrita
- [ ] nenhum caminho absoluto nem credencial no código reescrito
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] contrato só declara endpoint capturado (resposta real), nunca por chute
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 1 OK. Cliente [tipo] extraído e rebrandado em front-clonado\."
```
