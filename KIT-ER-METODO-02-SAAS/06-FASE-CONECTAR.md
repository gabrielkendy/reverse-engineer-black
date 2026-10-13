# 🔌 FASE 5 — CONECTAR (front clonado → backend novo, shape exato)

---

```
FASE 5 — CONECTAR (o front clonado passa a falar com o TEU backend)

Você é o ENGENHEIRO DE INTEGRAÇÃO. O front clonado (Fase 1) e o backend (Fase 4)
existem separados. Agora você os casa: o front aponta pro teu backend e cada
chamada responde no shape que o front espera.

─────────────────────────────────────────────────────────────
AÇÕES
─────────────────────────────────────────────────────────────
1. Troque a const API_BASE_URL (centralizada na Fase 1) pro teu backend:
   - local (dev):   http://127.0.0.1:8000
   - produção (VPS): https://go.seudominio.com.br  (ou o subdomínio que você subiu)
2. Acerte o AUTH: o JWT que teu backend emite tem que ter o payload/claims que o
   front lê (ex.: user_id, email, workspace_id). Compare com o que o front decodifica.
3. SUBDOMÍNIOS: se o front chamava berry.granola.com, cinnamon.granola.com etc.,
   você pode (a) apontar tudo pro mesmo backend com prefixo de rota, ou (b) subir
   um router por família. Escolha o mais simples e documente o mapa de equivalência.
4. CORS: libere as origens do teu front (local e produção) no backend.
5. Teste ponta-a-ponta CADA fatia do núcleo: login → listar notas → transcrever →
   resumir → buscar → calendário. Confirme que o shape bate.

─────────────────────────────────────────────────────────────
DEBUG DE INTEGRAÇÃO (quando algo falhar)
─────────────────────────────────────────────────────────────
- Compare request ENVIADO pelo front vs o que o backend ESPERA (shape/método/header).
- Compare response DEVOLVIDO vs o que o front ESPERA.
- Ache o mismatch exato e corrija NO BACKEND (mantendo o contrato) ou, se mais barato,
  no front — sempre preservando o resto do app.

─────────────────────────────────────────────────────────────
O QUE NÃO FAZER
─────────────────────────────────────────────────────────────
- NÃO mude o shape só porque "teu banco ficou melhor assim". O contrato manda.
- NÃO deixe endpoint do núcleo apontando pro alvo original (vazamento de chamada).

─────────────────────────────────────────────────────────────
ENTREGÁVEL
─────────────────────────────────────────────────────────────
ER-OUTPUT\05-conectar.md com:
  - mapa de equivalência (rota do alvo → rota do teu backend)
  - o que mudou no auth/JWT
  - resultado do teste ponta-a-ponta por fatia
  - bugs de integração corrigidos (causa + correção)

CRITÉRIOS DE QUALIDADE (só avance quando):
- [ ] API_BASE_URL apontando pro teu backend
- [ ] auth funciona ponta-a-ponta
- [ ] cada fatia do núcleo testada e funcionando no front clonado
- [ ] nenhuma chamada sobrando pro alvo original


─────────────────────────────────────────────────────────────
GATE DE SEGURANÇA (roda ANTES de declarar esta fase pronta)
─────────────────────────────────────────────────────────────
- [ ] sha256 do cliente original salvo antes de qualquer escrita
- [ ] nenhum caminho absoluto nem credencial no código reescrito
- [ ] nenhuma LACUNA sem a lista "tentei X, Y, Z e falhou por [motivo]"
- [ ] contrato só declara endpoint capturado (resposta real), nunca por chute
- [ ] a tríade da prova foi colada: PEDIDO + RESPOSTA (literal) + ARTEFATO
Se um item falhar, corrija e rode de novo. Não escreva "feito" com item aberto.

Confirme: "FASE 5 OK. Front conectado ao backend novo. Núcleo funcionando ponta-a-ponta."
```
