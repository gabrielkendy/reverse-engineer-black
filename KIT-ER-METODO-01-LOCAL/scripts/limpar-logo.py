#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LIMPEZA DE LOGO E ICONE — ER BLACK
=============================================================================
Cobre o que o limpar-identidade.py NAO cobre: os binarios visuais.
  - acha TODOS os icones e logos do clone (.ico .icns .png .svg .jpg)
  - descobre quais sao MARCA (nome do produto no arquivo, ou dentro de pasta
    de assets/brand) e quais sao conteudo
  - GERA um icone novo, inventado, com o nome inventado do app
  - troca no lugar, deixa backup
  - reescreve o apontamento do icone no electron-builder / manifests

Nao depende de nada externo: desenha o PNG na mao (zlib + struct) e converte
para .ico. Roda em qualquer Windows com Python 3.

Uso:
    python limpar-logo.py <PASTA_DO_CLONE> --nome "Maryra" [--dry]
"""
import os, re, sys, zlib, struct, shutil, argparse, json, hashlib
from datetime import datetime

# ---------------------------------------------------------------- PNG na mao
def _chunk(tipo, dados):
    c = tipo + dados
    return struct.pack(">I", len(dados)) + c + struct.pack(">I", zlib.crc32(c) & 0xFFFFFFFF)

def png_solido(w, h, cor, raio_rel=0.18):
    """PNG RGBA com fundo arredondado na cor dada + marca geometrica clara."""
    r, g, b = cor
    raio = int(min(w, h) * raio_rel)
    linhas = []
    for y in range(h):
        lin = bytearray()
        for x in range(w):
            dentro = True
            # cantos arredondados
            for cx, cy in ((raio, raio), (w-1-raio, raio), (raio, h-1-raio), (w-1-raio, h-1-raio)):
                if ((x < raio and y < raio) or (x > w-1-raio and y < raio) or
                    (x < raio and y > h-1-raio) or (x > w-1-raio and y > h-1-raio)):
                    if (x-cx)**2 + (y-cy)**2 > raio*raio:
                        dentro = False; break
            if not dentro:
                lin += bytes((0, 0, 0, 0))
                continue
            # marca: dois losangos entrelacados (geometria pura, nada de logo)
            nx, ny = (x - w/2) / (w/2), (y - h/2) / (h/2)
            d1 = abs(nx) + abs(ny)
            d2 = abs(nx - 0.35) + abs(ny + 0.35)
            if d1 < 0.30 or d2 < 0.30:
                lin += bytes((245, 245, 250, 255))
            else:
                lin += bytes((r, g, b, 255))
        linhas.append(bytes(lin))
    raw = b"".join(b"\x00" + l for l in linhas)
    return (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + _chunk(b"IDAT", zlib.compress(raw, 9))
            + _chunk(b"IEND", b""))

def ico_de_pngs(pngs):
    """Monta um .ico com varios tamanhos (guardando PNG dentro do ICO)."""
    n = len(pngs)
    out = struct.pack("<HHH", 0, 1, n)
    offset = 6 + 16 * n
    entradas, dados = b"", b""
    for tam, png in pngs:
        w = 0 if tam >= 256 else tam
        entradas += struct.pack("<BBBBHHII", w, w, 0, 0, 1, 32, len(png), offset)
        dados += png
        offset += len(png)
    return out + entradas + dados

# ---------------------------------------------------------------- deteccao
EXT_IMG = {".ico", ".icns", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg"}

# pastas que NUNCA devem ser varridas (nao sao do produto)
PULA = {"node_modules", ".git", "ER-LIMPEZA", "venv-er", "venv", "__pycache__",
        "Lib", "site-packages", "locales"}

def eh_marca(rel, nomes_produto):
    """Marca = nome do produto no caminho, ou esta em pasta de marca/icone."""
    baixo = rel.lower()
    if any(n in baixo for n in nomes_produto):
        return True
    pasta = baixo.replace("\\", "/")
    if re.search(r"/(icon|icons|logo|logos|brand|branding|marca|assets)/", pasta):
        return True
    if re.search(r"(icon|logo|favicon|tray|splash|badge)[^/]*\.(ico|icns|png|svg|jpg)$", pasta):
        return True
    return False

def acha_imagens(pasta, nomes_produto):
    marca, conteudo = [], []
    for dp, dns, fns in os.walk(pasta):
        dns[:] = [d for d in dns if d not in PULA]
        for fn in fns:
            if os.path.splitext(fn)[1].lower() not in EXT_IMG:
                continue
            fp = os.path.join(dp, fn)
            rel = os.path.relpath(fp, pasta)
            (marca if eh_marca(rel, nomes_produto) else conteudo).append((fp, rel))
    return marca, conteudo

def acha_nomes_visiveis(pasta, nomes_produto):
    """O que o usuario VE como nome: executaveis, atalhos, pastas de topo."""
    achados = []
    for dp, dns, fns in os.walk(pasta):
        dns[:] = [d for d in dns if d not in PULA]
        partes = os.path.relpath(dp, pasta).split(os.sep)
        for fn in fns:
            baixo = fn.lower()
            if not any(n in baixo for n in nomes_produto):
                continue
            ext = os.path.splitext(fn)[1].lower()
            if ext in {".exe", ".lnk", ".bat", ".cmd", ".app", ".desktop", ".dll"} or not ext:
                achados.append((os.path.join(dp, fn), os.path.relpath(os.path.join(dp, fn), pasta)))
    return achados

# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--nome", required=True, help="nome inventado do app (do limpar-identidade)")
    ap.add_argument("--seed", default=None)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    pasta = os.path.abspath(a.pasta)
    nome = a.nome
    semente = a.seed or hashlib.sha256((pasta + nome).encode()).hexdigest()
    r = int(hashlib.sha256(semente.encode()).hexdigest()[:4], 16)
    cor = ((r * 37) % 120 + 20, (r * 91) % 120 + 30, (r * 53) % 120 + 80)  # cor estavel
    nomes_produto = [s.lower() for s in
                     ("content-hub", "content hub", "contenthub", "content-studio",
                      "content studio", "contentstudio", "arte-viva-hub", "arte viva hub",
                      "arte-viva", nome.lower())]

    print("=" * 72)
    print("  LIMPEZA DE LOGO E ICONE — ER BLACK")
    print("=" * 72)
    print(f"  clone : {pasta}")
    print(f"  nome  : {nome}")
    print(f"  cor   : rgb{cor}")
    print(f"  modo  : {'SIMULACAO' if a.dry else 'GRAVANDO'}")
    print("=" * 72)

    marca, conteudo = acha_imagens(pasta, nomes_produto)
    visiveis = acha_nomes_visiveis(pasta, nomes_produto)
    print(f"\n  imagens que sao MARCA  : {len(marca)}")
    print(f"  imagens que sao CONTEUDO: {len(conteudo)}")
    print(f"  arquivos com nome do produto (usuario VE): {len(visiveis)}")
    print("\n  --- marca (trocando) ---")
    for fp, rel in marca[:40]:
        print(f"    {rel}  ({os.path.getsize(fp)} B)")
    if len(marca) > 40:
        print(f"    ... +{len(marca)-40}")
    print("\n  --- nomes visiveis (renomeando) ---")
    for fp, rel in visiveis[:20]:
        print(f"    {rel}")

    # gera os icones novos
    pngs = [(s, png_solido(s, s, cor))
            for s in (16, 24, 32, 48, 64, 128, 256)]
    ico = ico_de_pngs(pngs)
    png256 = png_solido(256, 256, cor)
    png512 = png_solido(512, 512, cor)

    print(f"\n  icone novo gerado: .ico com {len(pngs)} tamanhos ({len(ico)} bytes)")

    out = os.path.join(pasta, "ER-LIMPEZA")
    antes = os.path.join(out, "_antes-icones")
    feitos = []
    if not a.dry:
        os.makedirs(out, exist_ok=True)
        for fp, rel in marca:
            try:
                os.makedirs(antes, exist_ok=True)
                shutil.copy2(fp, os.path.join(antes, rel.replace(os.sep, "__")))
                ext = os.path.splitext(fp)[1].lower()
                if ext == ".ico":
                    open(fp, "wb").write(ico)
                elif ext == ".svg":
                    open(fp, "w", encoding="utf-8").write(
                        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">'
                        f'<rect width="256" height="256" rx="46" fill="rgb{cor}"/>'
                        f'<path d="M128 52 L204 128 L128 204 L52 128 Z" fill="#f5f5fa"/>'
                        f'<path d="M128 92 L164 128 L128 164 L92 128 Z" fill="rgb{cor}"/>'
                        f'</svg>')
                elif ext in (".png", ".webp"):
                    open(fp, "wb").write(png512 if os.path.getsize(fp) > 200_000 else png256)
                elif ext in (".jpg", ".jpeg"):
                    # JPEG nao aceita alfa; gera versao sobre fundo da cor
                    open(fp, "wb").write(_jpeg_fallback(256, cor))
                feitos.append(rel)
            except Exception as e:
                print(f"    FALHA {rel}: {e}")

    # reescreve apontamentos
    aponta = []
    for dp, dns, fns in os.walk(pasta):
        dns[:] = [d for d in dns if d not in {"node_modules", ".git", "ER-LIMPEZA"}]
        for fn in fns:
            if fn != "package.json":
                continue
            fp = os.path.join(dp, fn)
            try:
                t = open(fp, encoding="utf-8").read()
            except Exception:
                continue
            orig = t
            # aponta todo campo de icone para .ico novo
            t = re.sub(r'("icon"\s*:\s*")[^"]{0,200}(")', r'\1build/icon.ico\2', t)
            if t != orig and not a.dry:
                shutil.copy2(fp, os.path.join(antes, os.path.relpath(fp, pasta).replace(os.sep, "__")))
                open(fp, "w", encoding="utf-8").write(t)
                aponta.append(os.path.relpath(fp, pasta))

    print(f"\n  icones trocados : {len(feitos)}")
    print(f"  manifests ajustados: {len(aponta)}  {aponta}")

    # cria a pasta build com o icone novo (o apontamento espera ela)
    if not a.dry:
        bd = os.path.join(pasta, "build")
        os.makedirs(bd, exist_ok=True)
        open(os.path.join(bd, "icon.ico"), "wb").write(ico)
        print(f"  [ok] build/icon.ico escrito")

    if not a.dry:
        L = [f"# Limpeza de icone e logo — {nome}\n",
             f"> Gerado por `limpar-logo.py` em {datetime.now():%Y-%m-%d %H:%M}\n",
             f"\n## Icone novo\n",
             f"- formato: ICO multi-tamanho ({', '.join(str(s) for s,_ in pngs)})",
             f"- cor: rgb{cor}",
             f"- marca: dois losangos (geometria pura, nenhum logo de terceiro)",
             f"\n## Arquivos de marca trocados: {len(feitos)}\n"]
        for f_ in feitos:
            L.append(f"- `{f_}`")
        L.append(f"\n## Manifests ajustados: {len(aponta)}\n")
        for f_ in aponta:
            L.append(f"- `{f_}`")
        L.append("\n## CONFERIR NA TELA (nao da pra automatizar)\n")
        L.append("- [ ] Icone na barra de tarefas")
        L.append("- [ ] Icone na janela (canto superior esquerdo)")
        L.append("- [ ] Icone no menu Iniciar / atalho")
        L.append("- [ ] Icone no instalador gerado")
        L.append("- [ ] Titulo da janela")
        L.append("- [ ] Splash screen, se houver")
        L.append("- [ ] Icone da bandeja (tray), se houver")
        open(os.path.join(out, "04-icones.md"), "w", encoding="utf-8").write("\n".join(L))
        print(f"  [salvo] {os.path.join(out,'04-icones.md')}")

def _jpeg_fallback(tam, cor):
    """JPEG minimo valido (fundo solido). Evita depender de PIL."""
    r, g, b = cor
    try:
        from PIL import Image
        import io
        im = Image.new("RGB", (tam, tam), cor)
        buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
        return buf.getvalue()
    except Exception:
        pass
    # JPEG 1x1 cinza valido como ultimo recurso
    return bytes.fromhex(
        "ffd8ffe000104a46494600010100000100010000ffdb00430008060607060508070707"
        "09090807090b0c0e0d0b0c0b0d11131210131416151215161c1f1f1c1a1f1f1f1f1f"
        "1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f"
        "1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1f1"
        "ffc00011080001000103012200021101031101ffc4001f000001050101010101010000"
        "0000000000000102030405060708090a0bffc400b5100002010303020403050504040000"
        "017d01020300041105122131410613516107227114328191a1082342b1c11552d1f02433"
        "627282090a161718191a25262728292a3435363738393a434445464748494a53545556"
        "5758595a636465666768696a737475767778797a838485868788898a92939495969798"
        "999aa2a3a4a5a6a7a8a9aab2b3b4b5b6b7b8b9bac2c3c4c5c6c7c8c9cad2d3d4d5d6"
        "d7d8d9dae1e2e3e4e5e6e7e8e9eaf1f2f3f4f5f6f7f8f9faffda0008010100003f00"
        "fefcfcfeffd9")

if __name__ == "__main__":
    main()
