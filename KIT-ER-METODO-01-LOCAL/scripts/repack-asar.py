#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REPACK DO ASAR — ER BLACK (v2, ordem unica)
=============================================================================
Monta app.asar a partir de uma pasta limpa.

REGRA QUE CUSTOU CARO (bug ja cometido): o header e o blob TEM que sair da
MESMA lista ordenada. Se o header for montado com sorted() e o blob for
escrito na ordem do os.walk, os offsets apontam para o arquivo errado e o
Electron le pedaco do vizinho — o app abre com tela quebrada, sem erro.

Regras do formato (conferidas contra asar que funciona):
  * cabecalho: struct "<IIII" = (4, jsonLen+8, jsonLen+4, jsonLen)
  * jsonLen   = tamanho EXATO do header json, sem padding
  * blob comeca em 16 + jsonLen, sem alinhamento
  * offset de cada arquivo = posicao relativa ao inicio do blob
  * .node vai com "unpacked": true (fica fora, em app.asar.unpacked/)

Uso:
  python repack-asar.py <pasta_limpa> <destino/app.asar> [--unpacked <dir>]

O teste que decide nao e este script terminar: e o app ABRIR e a tela
aparecer igual. Depois do repack, sempre ler o pacote de volta e conferir.
"""
import os
import sys
import json
import struct
import shutil

CABECALHO = 16
FORA_SEMPRE = {"ER-LIMPEZA", ".git", "__pycache__", "venv-er"}


def lista_arquivos(base):
    """Lista UNICA, ordenada, de tudo que entra no blob. Fonte da verdade."""
    itens = []
    for dp, dns, fns in os.walk(base):
        dns[:] = sorted(x for x in dns if x not in FORA_SEMPRE)
        for f in sorted(fns):
            fp = os.path.join(dp, f)
            rel = os.path.relpath(fp, base).replace(os.sep, "/")
            itens.append(rel)
    return sorted(itens)


def monta_arvore(itens):
    """Monta a arvore do header a partir da MESMA lista do blob."""
    raiz = {"files": {}}
    for rel in itens:
        partes = rel.split("/")
        no = raiz
        for p in partes[:-1]:
            no = no["files"].setdefault(p, {"files": {}})
        nome = partes[-1]
        d = {"size": 0}
        if nome.endswith(".node"):
            d["unpacked"] = True
        no["files"][nome] = d
    return raiz


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    limpa = sys.argv[1].rstrip("/\\")
    destino = sys.argv[2]
    if os.path.abspath(destino).startswith(os.path.abspath(limpa) + os.sep):
        print("ERRO: o destino esta DENTRO da pasta de origem.")
        print("      Grave o app.asar em outra pasta, senao ele se empacota a si mesmo.")
        return 3
    unpacked_dir = None
    if "--unpacked" in sys.argv:
        unpacked_dir = sys.argv[sys.argv.index("--unpacked") + 1]

    itens = lista_arquivos(limpa)
    arvore = monta_arvore(itens)

    # contabiliza offsets na MESMA ordem do blob
    off = 0
    dados = {}
    for rel in itens:
        b = open(os.path.join(limpa, rel), "rb").read()
        dados[rel] = b
        if not rel.endswith(".node"):
            # grava o offset na arvore descendo o caminho
            partes = rel.split("/")
            no = arvore
            for p in partes[:-1]:
                no = no["files"][p]
            no["files"][partes[-1]]["offset"] = str(off)
            no["files"][partes[-1]]["size"] = len(b)
            off += len(b)
        else:
            partes = rel.split("/")
            no = arvore
            for p in partes[:-1]:
                no = no["files"][p]
            no["files"][partes[-1]]["size"] = len(b)

    header = json.dumps(arvore, separators=(",", ":")).encode("utf-8")
    hsz = len(header)

    with open(destino, "wb") as f:
        f.write(struct.pack("<IIII", 4, hsz + 8, hsz + 4, hsz))
        f.write(header)
        for rel in itens:
            if not rel.endswith(".node"):
                f.write(dados[rel])

    print("arquivos no pacote  : %d" % len(itens))
    print("nativos (unpacked)  : %s" % ", ".join(r for r in itens if r.endswith(".node")))
    print("header              : %d bytes" % hsz)
    print("blob                : %d bytes" % off)
    print("TOTAL               : %d bytes -> %s" % (CABECALHO + hsz + off, destino))

    if unpacked_dir:
        for rel in itens:
            if rel.endswith(".node"):
                dst = os.path.join(unpacked_dir, rel)
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(os.path.join(limpa, rel), dst)
        print("unpacked copiado    : %s" % unpacked_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
