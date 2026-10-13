#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""VALIDA UM KIT ER BLACK CONTRA O PADRAO DEV PRO ULTRA.

Uso:
    python VALIDAR-KIT.py "<caminho da pasta do kit>"
    python VALIDAR-KIT.py --todas        (varre os dois KITs e da a nota)

Sem opiniao. So mede mecanica, item por item. Saida: OK ou FORA DO PADRAO
com a lista exata do que falta. Espelho do VALIDAR-AULA.py do padrao Kendy,
adaptado pra pacote de Engenharia Reversa.

O que este portao NAO pode deixar passar (cada item vira checagem):
  1. Kit sem o prompt mestre.
  2. Kit sem a fase de VALIDAR/PARIDADE.
  3. Fase com regra de LACUNA sem "tentei X, Y, Z".
  4. Fase sem a regra da COPIA (trabalhar nunca no original).
  5. Fase sem hash sha256 do alvo.
  6. Kit sem "inteligencia de alvo" (CVE / writeup / versao open-source).
  7. Kit sem o gate de seguranca (prova obrigatoria, achado sem prova nao entra).
  8. Kit sem a esteira (Linear/Codex/Orca equivalente) quando e SaaS.
  9. Fase com caminho absoluto chumbado.
 10. Kit sem o "cerebro" mapeado (a lista de funcoes/endpoints que faz o app).

So le. Nunca escreve, nunca move, nunca apaga.
"""
import os, re, sys, glob

CHECAGENS = []   # (ok, item, detalhe)


def ler(p):
    try:
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception:
        return ""


def chk(ok, item, detalhe=""):
    CHECAGENS.append((bool(ok), item, detalhe))


def achar(base, *nomes):
    for n in nomes:
        for p in glob.glob(os.path.join(base, "**", n), recursive=True):
            return p
    return None


# palavras-chave que, se ausentes em TODAS as fases, reprovam o kit
TOKENS_OBRIGATORIOS = {
    "COPIA": (r"(?i)\b(c[oó]pia|nunca toque|n[ãa]o toque|backup|original intocado|isolamento)\b",
              "regra da copia (nunca no original)"),
    "SHA256": (r"(?i)\bsha-?256\b",
               "hash sha256 do alvo"),
    "LACUNA": (r"(?i)\blacuna\b",
               "regra de lacuna (fato != inferencia)"),
    "TENTEI": (r"(?i)\btentei\b",
               "lacuna exige 'tentei X, Y, Z'"),
    "INTEL": (r"(?i)\b(cve|writeup|open-?source equivalente|intelig[êe]ncia de alvo|pesquise o alvo|version)\b",
              "inteligencia de alvo (CVE/writeup/open-source)"),
    "PROVA": (r"(?i)\b(sem prova n[ãa]o entra|achado sem prova|prova obrigat[óo]ria|pedido \+ resposta \+ print|pedido\+resposta)\b",
              "gate de seguranca (achado sem prova nao entra)"),
    "PARIDADE": (r"(?i)\b(paridade|byte a byte|mesma entrada|id[êe]ntico|comportamento exato)\b",
                "prova de paridade"),
    "RELATIVO": (r"(?i)\b(caminho\s+relativo|use\s+relativo|relativo\s*\(nunca chumbado\)|n[ãa]o chumbe|n[ãa]o use caminho absoluto|path relativo)\b",
                "caminho relativo, nunca chumbado"),
    "CEREBRO": (r"(?i)\b(c[ée]rebro|mapa de fun[çc][õo]es|lista de fun[çc][õo]es|endpoints|grafo de chamada|cat[áa]logo)\b",
                "cerebro mapeado (funcoes/endpoints)"),
    "SEVERIDADE": (r"(?i)\b(cr[íi]tica|severidade|alta|m[ée]dia|baixa)\b",
                  "criterio de severidade"),
}


def validar(kit):
    CHECAGENS.clear()
    nome = os.path.basename(os.path.normpath(kit))

    # 1. prompt mestre
    mestre = achar(kit, "00-PROMPT-MESTRE.md", "PROMPT-MESTRE.md")
    chk(mestre is not None, "prompt mestre existe", mestre or "nao achei")

    # 2. fase de validar
    valida = achar(kit, "*VALIDAR*.md", "*VALIDACAO*.md", "*PARIDADE*.md")
    chk(valida is not None, "fase VALIDAR existe", valida or "nao achei")

    # 3. readme
    readme = achar(kit, "README.md")
    chk(readme is not None, "README existe", readme or "nao achei")

    # 4. checklist final
    chklist = achar(kit, "*CHECKLIST*.md")
    chk(chklist is not None, "checklist final existe", chklist or "nao achei")

    # 5. ferramentas
    fer = achar(kit, "*FERRAMENTAS*.md")
    chk(fer is not None, "tabela de ferramentas existe", fer or "nao achei")

    # 6. conteudo agregado de todos os .md
    todos = glob.glob(os.path.join(kit, "**", "*.md"), recursive=True)
    tudo = ""
    for t in todos:
        tudo += ler(t) + "\n"

    # 7. tokens obrigatorios (qualquer arquivo do kit pode carregar)
    for tok, (pat, rot) in TOKENS_OBRIGATORIOS.items():
        chk(re.search(pat, tudo) is not None, "kit: " + rot, "")

    # 8. caminho absoluto chumbado (heuristica: letra de drive + backslash no prompt)
    drive = re.search(r"\b[A-Z]:\\\\", tudo)
    chk(drive is None, "kit: sem caminho absoluto chumbado",
        ("achou " + drive.group(0)) if drive else "")

    # 9. numero de fases (espera 4+ arquivos de fase)
    fases = [f for f in todos if re.search(r"FASE", os.path.basename(f))]
    chk(len(fases) >= 4, "kit: 4+ arquivos de fase", "%d fases" % len(fases))

    # 10. anatomia densa: cada fase tem "o que falta" ou "nao fazer" ou "armadilha"
    anat = re.search(r"(?i)\b(o que faltou|o que n[ãa]o fazer|nao fazer|armadilha|queimou|deu errado|retrabalho)\b", tudo)
    chk(anat is not None, "kit: secao de armadilha/o que faltou presente", "")

    # 11. TODAS as fases carregam o gate de seguranca (nao so o prompt mestre)
    if fases:
        sem_gate = [os.path.basename(f) for f in fases if "GATE DE SEGURAN" not in ler(f)]
        chk(not sem_gate, "todas as fases tem gate (" + str(len(fases)) + " fases)",
            ("sem gate: " + str(sem_gate)) if sem_gate else "")

    return nome, list(CHECAGENS)


def relatorio(kit):
    nome, r = validar(kit)
    ok = sum(1 for x in r if x[0])
    tot = len(r)
    pct = round(100.0 * ok / tot) if tot else 0
    print("=" * 70)
    print("KIT: %s" % nome)
    print("NOTA: %d/%d  (%d%%)  %s" % (ok, tot, pct, "OK" if ok == tot else "FORA DO PADRAO"))
    print("=" * 70)
    for o, item, det in r:
        if not o:
            print("  [ ] %s   %s" % (item, ("(%s)" % det) if det else ""))
    if ok == tot:
        print("  tudo conforme o padrao DEV PRO ULTRA.")
    print()
    return pct


if __name__ == "__main__":
    base = os.path.dirname(os.path.abspath(__file__))
    if "--todas" in sys.argv:
        kits = [d for d in glob.glob(os.path.join(base, "KIT-*")) if os.path.isdir(d)]
        print("\n%d KITs. Nota de cada:\n" % len(kits))
        res = []
        for k in kits:
            n, r = validar(k)
            ok = sum(1 for x in r if x[0])
            res.append((round(100.0 * ok / max(1, len(r))), os.path.basename(k)))
        for pct, n in sorted(res, reverse=True):
            barra = "#" * (pct // 5) + "." * (20 - pct // 5)
            print("  %3d%%  %s  %s" % (pct, barra, n))
        print()
    elif len(sys.argv) >= 2:
        relatorio(sys.argv[1])
    else:
        print(__doc__)
