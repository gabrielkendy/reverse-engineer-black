#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETAPA LIMPEZA TOTAL — ER BLACK (orquestrador)
=============================================================================
Roda as duas limpezas em sequencia, na ordem certa, e produz UM relatorio.

Ordem:
  1) limpar-identidade.py   (nome, autor, url, copyright, appid, manifest)
  2) limpar-logo.py         (icone, logo, imagens de marca, nome visivel)

Uso:
    python limpar-total.py <PASTA_DO_CLONE> [--nome "Meu App"] [--seed X] [--dry]
"""
import os, sys, subprocess, argparse, json, hashlib
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))

def roda(script, args):
    cmd = [sys.executable, os.path.join(AQUI, script)] + args
    print(f"\n>>> {' '.join(os.path.basename(c) if i else c for i, c in enumerate(cmd))}\n")
    p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    sys.stdout.write(p.stdout or "")
    if p.stderr:
        sys.stderr.write(p.stderr)
    return p.returncode, p.stdout or ""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--nome", default=None, help="vao inventado; se vazio, o script inventa")
    ap.add_argument("--seed", default=None)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    pasta = os.path.abspath(a.pasta)
    if not os.path.isdir(pasta):
        print(f"ERRO: nao existe: {pasta}"); sys.exit(1)

    # o nome tem que ser o MESMO nas duas etapas; se nao veio, inventa aqui
    nome = a.nome
    if not nome:
        semente = a.seed or hashlib.sha256(pasta.encode()).hexdigest()
        import random
        A = ["nor","vex","lu","ky","zar","mi","tel","ru","cal","dor","fen","sil","tan","gim","bra"]
        B = ["dex","tia","ron","lex","va","mira","son","dra","bel","phi","cos","lith","via","nor"]
        r = random.Random(semente)
        nome = r.choice(A).capitalize() + r.choice(B)
    seed = a.seed or hashlib.sha256((pasta + nome).encode()).hexdigest()

    print("#" * 72)
    print(f"#  LIMPEZA TOTAL DE IDENTIDADE — {nome}")
    print(f"#  clone: {pasta}")
    print(f"#  modo : {'SIMULACAO (nada gravado)' if a.dry else 'GRAVANDO'}")
    print("#" * 72)

    base = [pasta, "--nome", nome, "--seed", seed] + (["--dry"] if a.dry else [])

    # 1) identidade de texto
    rc1, out1 = roda("limpar-identidade.py", base)
    # 2) logo / icone / nome visivel
    rc2, out2 = roda("limpar-logo.py", base)

    # 3) relatorio unico
    def extrai(txt, rotulo):
        for ln in txt.split("\n"):
            if rotulo in ln:
                return ln.strip()
        return "?"

    resumo = {
        "nome_inventado": nome,
        "seed": seed,
        "pasta": pasta,
        "data": datetime.now().isoformat(timespec="seconds"),
        "trocas_texto": extrai(out1, "trocas de texto"),
        "arquivos_renomeados": extrai(out1, "arquivos renomeados"),
        "pendencias_texto": extrai(out1, "pendencias"),
        "imagens_marca": extrai(out2, "imagens que sao MARCA"),
        "nomes_visiveis": extrai(out2, "arquivo com nome do produto"),
        "icones_trocados": extrai(out2, "icones trocados"),
        "rc_identidade": rc1,
        "rc_logo": rc2,
    }

    print("\n" + "#" * 72)
    print("#  RESUMO DA LIMPEZA")
    print("#" * 72)
    for k, v in resumo.items():
        print(f"  {k:<22} {v}")

    ok = (rc1 == 0 and rc2 == 0)
    print("\n" + ("  LIMPEZA OK — clone sem identidade do original."
                  if ok else "  LIMPEZA INCOMPLETA — ver as falhas acima."))
    print("  PROIBIDO entregar clone com identidade do original. Confira 03-pendencias.md e 04-icones.md.")

    out = os.path.join(pasta, "ER-LIMPEZA")
    if not a.dry:
        os.makedirs(out, exist_ok=True)
        json.dump(resumo, open(os.path.join(out, "00-resumo.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        print(f"\n  [salvo] {os.path.join(out, '00-resumo.json')}")

if __name__ == "__main__":
    main()
