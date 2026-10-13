#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ETAPA LIMPEZA DE IDENTIDADE — ER BLACK
=============================================================================
Roda DEPOIS do desempacotar (Fase 2) e ANTES de reconstruir/reeditar.
Objetivo: o clone nasce SEM identidade do original. Nome, logo, icone,
autor, copyright, URLs, IDs de telemetria — tudo trocado por valores
INVENTADOS, gerados pelo proprio script. Nada do PC do operador entra.

REGRA DURA: PROIBIDO o clone manter QUALQUER identidade do original.
Se o script nao souber o que e, ele NEUTRALIZA (nao deixa passar).

Uso:
    python limpar-identidade.py <PASTA_DO_CLONE> [--nome "Meu App"] [--dry]

Saida:
    <PASTA_DO_CLONE>/ER-LIMPEZA/01-relatorio.md     (o que foi trocado)
    <PASTA_DO_CLONE>/ER-LIMPEZA/02-mapa.json        (de -> para, byte a byte)
    <PASTA_DO_CLONE>/ER-LIMPEZA/03-pendencias.md    (o que precisa de olho humano)
    backup dos arquivos tocados em ER-LIMPEZA/_antes/
"""
import os, re, sys, json, random, string, hashlib, shutil, argparse
from datetime import datetime

# ---------------------------------------------------------------- inventados
SILABAS_A = ["nor", "vex", "lu", "ky", "zar", "mi", "tel", "ru", "cal", "dor",
             "fen", "sil", "tan", "gim", "bra", "quel", "vin", "sol", "mar", "nyx"]
SILABAS_B = ["dex", "tia", "ron", "lex", "va", "mira", "son", "dra", "bel",
             "phi", "cos", "lith", "via", "nor", "quin", "arlo", "mex", "yra"]

def inventa_nome(seed=None):
    r = random.Random(seed)
    a = r.choice(SILABAS_A).capitalize()
    b = r.choice(SILABAS_B)
    return a + b

def inventa_pacote(seed=None):
    r = random.Random(seed)
    return ".".join(r.choice(SILABAS_A) + r.choice(SILABAS_B) for _ in range(2))

def inventa_id(prefixo="", n=12, seed=None):
    r = random.Random(seed)
    alf = string.ascii_lowercase + string.digits
    return prefixo + "".join(r.choice(alf) for _ in range(n))

def inventa_versao(seed=None):
    r = random.Random(seed)
    return f"{r.randint(0,3)}.{r.randint(0,9)}.{r.randint(0,20)}"

# ---------------------------------------------------------------- padroes
# Cada item: (rotulo, regex, gerador do substituto)
# A ordem importa: o mais especifico primeiro.
def monta_regras(ctx):
    P = ctx["nome_curto"]      # ex.: "Nordex"
    p = ctx["nome_curto"].lower()
    PKG = ctx["pacote"]        # ex.: "nortex.quival"
    AUTOR = ctx["autor"]
    URL = ctx["url"]
    VER = ctx["versao"]
    APPID = ctx["appid"]

    R = []
    # --- nome do produto, em varios formatos
    R.append(("nome-produto", r"\b(Content Hub|Content Studio|content-hub|content-studio|content_studio)\b", P))
    R.append(("nome-produto-slug", r"\b(content[-_ ]hub|content[-_ ]studio)\b", p))
    # --- autor / copyright
    R.append(("copyright", r"(?i)copyright\s*(?:\(c\)|©)?\s*\d{4}(?:\s*[-–]\s*\d{4})?\s*[^\r\n\"'<]{0,60}",
              f"Copyright (c) {datetime.now().year} {AUTOR}"))
    R.append(("autor-campo", r"(?im)^(\s*(?:author|owner|maintainer|copyright)\s*[:=]\s*)[^\r\n]{1,80}",
              lambda m: m.group(1) + AUTOR))
    # --- url / site
    R.append(("url-site", r"https?://[a-z0-9.-]*(?:content.?hub|content.?studio|agenciabase|getlayers)[a-z0-9./_-]*",
              URL))
    R.append(("email", r"[\w.+-]+@[\w-]*(?:content.?hub|content.?studio|agenciabase|getlayers)[\w.-]*\.[a-z]{2,}",
              f"contato@{p}.dev"))
    # --- package.json / manifest (REGEX ANCORADA: nao pega chave que nao existe)
    R.append(("pkg-name", r'("name"\s*:\s*")[^"]{1,80}(")', lambda m: m.group(1) + ctx["pkg_npm"] + m.group(2)))
    # author pode ser string OU objeto {name,url}: cobre os dois
    R.append(("pkg-author-nome", r'("author"\s*:\s*\{[^{}]*?"name"\s*:\s*")[^"]{0,120}(")',
              lambda m: m.group(1) + AUTOR + m.group(2)))
    R.append(("pkg-author-url", r'("author"\s*:\s*\{[^{}]*?"url"\s*:\s*")[^"]{0,160}(")',
              lambda m: m.group(1) + URL + m.group(2)))
    R.append(("pkg-author-str", r'("author"\s*:\s*")([^"]{0,120})(")',
              lambda m: m.group(1) + AUTOR + m.group(3)))
    R.append(("pkg-homepage", r'("homepage"\s*:\s*")[^"]{0,160}(")', lambda m: m.group(1) + URL + m.group(2)))
    R.append(("pkg-description", r'("description"\s*:\s*")[^"]{0,200}(")',
              lambda m: m.group(1) + f"App local de conteudo" + m.group(2)))
    # version: troca o miolo inteiro, preserva as aspas
    R.append(("pkg-version", r'("version"\s*:\s*")\d+\.\d+\.\d+(?:-[\w.]+)?(")',
              lambda m: m.group(1) + VER + m.group(2)))
    # --- electron-builder
    R.append(("appid", r'(?i)("appId"\s*:\s*")[^"]{1,90}(")', lambda m: m.group(1) + APPID + m.group(2)))
    R.append(("productName", r'(?i)("productName"\s*:\s*")[^"]{1,90}(")', lambda m: m.group(1) + P + m.group(2)))
    R.append(("executableName", r'(?i)("executableName"\s*:\s*")[^"]{1,90}(")', lambda m: m.group(1) + p + m.group(2)))
    # --- telemetria: SO o host/URL, nunca a palavra solta
    R.append(("telemetria-host",
              r"(?i)(?<![\w.])https?://[a-z0-9.-]*(?:sentry|segment|mixpanel|amplitude|posthog)[a-z0-9./_-]*(?![\w.])",
              "https://localhost:9/disabled"))
    R.append(("telemetria-chave", r'(?i)(["\']?(?:sentry|posthog|segment)[_-]?(?:dsn|key|token|writeKey)["\']?\s*[:=]\s*["\'])[^"\']{8,200}(["\'])',
              lambda m: m.group(1) + "DISABLED" + m.group(2)))
    # --- credito de autor: SO as formas explicitas, SEM "by" solto.
    # (bug ja cometido: "|by)" casava com qualquer "by" do codigo e o
    #  [\\w'.] da cauda engolia aspas e parenteses — injetou "')" no topo
    #  do package.json e o app deixou de abrir.)
    # Ancora: a frase precisa estar num contexto de credito/rodape.
    R.append(("credito-autor",
              r"(?i)(crafted by|feito por|desenvolvido por|created by|powered by|built by)"
              r"([^\S\r\n]+)"
              r"[A-Za-zÀ-ÿ0-9@._·|/() -]{2,80}?"
              r"(?=[\r\n\"'<]|$)",
              lambda m: m.group(1) + " " + AUTOR))
    R.append(("arroba-social", r"@[a-zA-Z0-9._-]*(?:gabrielkendy|kendy|agenciabase|getlayers)[a-zA-Z0-9._-]*",
              f"@{p}.app"))
    # --- nome de produto NO COdigo e em titulo de janela
    R.append(("titulo-janela", r"(title\s*:\s*['\"])[^'\"]{1,90}(['\"])",
              lambda m: m.group(1) + P + m.group(2)))
    # --- nome de PRODUTO com maiusculas variadas: Arte Viva Hub, arte viva, ARTE VIVA
    R.append(("nome-produto-extenso",
              r"\b(?:Arte\s*Viva(?:\s*Hub)?|ARTE\s*VIVA(?:\s*HUB)?|arte[\s-]viva(?:[\s-]hub)?)\b",
              P))
    # --- prefixo tecnico com marca (arquivo temporario, chave de storage, cookie)
    R.append(("prefixo-tecnico",
              r"\.(?:arte[\s-]?viva|content[\s-]?hub|content[\s-]?studio)[\w.-]*",
              lambda m: "." + p + m.group(0)[len(re.match(r'\.(?:arte[\s-]?viva|content[\s-]?hub|content[\s-]?studio)', m.group(0), re.I).group(0)):] if re.match(r'\.(?:arte[\s-]?viva|content[\s-]?hub|content[\s-]?studio)', m.group(0), re.I) else m.group(0)))
    # --- chave de storage / cookie / namespace localstorage
    R.append(("namespace-storage",
              r"(?i)(['\"])(?:arte[\s-]?viva|content[\s-]?hub|content[\s-]?studio)([\w.:-]*)\1",
              lambda m: f"{m.group(1)}{p}{m.group(2)}{m.group(1)}"))
    # --- endpoint de API do produto
    R.append(("endpoint-api",
              r"https?://[a-z0-9.-]*(?:agenciabase|content-?hub|content-?studio|getlayers)[a-z0-9./_-]*",
              URL))
    return R

# ---------------------------------------------------------------- motor
# REGRA: nome de arquivo e ESTRUTURA, nao identidade. Nao renomeie codigo.
# So renomeia o que o usuario VE: a pasta do app na raiz e o executavel final.
NUNCA_RENOMEAR_EXT = {".js", ".mjs", ".cjs", ".ts", ".json", ".html", ".htm", ".css",
                      ".scss", ".md", ".txt", ".yml", ".yaml", ".xml", ".svg", ".py",
                      ".cs", ".go", ".rs", ".java", ".kt", ".php", ".rb", ".sh"}
TEXTOIS = {".js", ".mjs", ".cjs", ".ts", ".json", ".html", ".htm", ".css", ".scss",
           ".md", ".txt", ".yml", ".yaml", ".xml", ".svg", ".less",
           ".cs", ".py", ".rb", ".php", ".java", ".kt", ".swift", ".go", ".rs",
           ".rc", ".nsi", ".iss", ".ini", ".cfg", ".toml", ".env", ".bat", ".ps1", ".sh"}

PULA_DIRS = {"node_modules", ".git", "_antes", "ER-LIMPEZA", "dist", "out", ".cache"}

def varre(pasta, regras, dry=False):
    trocas, pendencias = [], []
    antes = os.path.join(pasta, "ER-LIMPEZA", "_antes")
    for dp, dns, fns in os.walk(pasta):
        dns[:] = [d for d in dns if d not in PULA_DIRS]
        for fn in fns:
            ext = os.path.splitext(fn)[1].lower()
            fp = os.path.join(dp, fn)
            rel = os.path.relpath(fp, pasta)

            if ext in TEXTOIS:
                try:
                    t = open(fp, encoding="utf-8", errors="surrogateescape").read()
                except Exception:
                    pendencias.append((rel, "nao consegui ler como texto")); continue
                orig = t
                for rot, pat, sub in regras:
                    def rep(m):
                        novo = sub(m) if callable(sub) else sub
                        trocas.append((rel, rot, m.group(0)[:90], str(novo)[:90]))
                        return novo
                    try:
                        t = re.sub(pat, rep, t)
                    except re.error:
                        pass
                if t != orig:
                    if not dry:
                        os.makedirs(antes, exist_ok=True)
                        dst = os.path.join(antes, rel.replace(os.sep, "__"))
                        shutil.copy2(fp, dst)
                        open(fp, "w", encoding="utf-8", errors="surrogateescape").write(t)
            elif ext in (".exe", ".dll", ".node", ".ico", ".png", ".jpg", ".jpeg", ".gif", ".icns"):
                # binario: so reporta, quem troca e a etapa de icones
                pendencias.append((rel, f"binario {ext} — identidade visual precisa de troca dedicada"))
    return trocas, pendencias

def limpa_nome_arquivo(pasta, trocas, dry=False):
    """Renomeia SO o que o usuario VE:
         - diretorios de primeiro nivel (a pasta do app)
         - arquivos SEM extensao de codigo (executavel, atalho, marcador)
       NUNCA renomeia codigo: quebraria require/import e o app nao abre."""
    feitos, recusados = [], []
    alvos = ["content-hub", "content hub", "contenthub",
             "content-studio", "content studio", "contentstudio",
             "arte-viva-hub", "arte viva hub"]
    raiz = os.path.abspath(pasta)
    for dp, dns, fns in os.walk(pasta, topdown=False):
        partes = os.path.relpath(dp, raiz).split(os.sep)
        if any(x in partes for x in PULA_DIRS):
            continue
        profundidade = 0 if partes == ["."] else len(partes)
        for nome in list(dns) + list(fns):
            ext = os.path.splitext(nome)[1].lower()
            # regra: codigo nunca; arquivo sem extensao de codigo pode
            if ext in NUNCA_RENOMEAR_EXT:
                if any(a in nome.lower() for a in alvos):
                    recusados.append((os.path.join(os.path.relpath(dp, raiz), nome),
                                      "tem nome do produto mas e CODIGO — renomear quebraria require/import"))
                continue
            # diretorio: so no primeiro nivel
            if nome in dns and profundidade > 1:
                continue
            novo = nome
            for a in alvos:
                novo = re.sub(re.escape(a), "app", novo, flags=re.I)
            novo = novo.strip(" -_")
            if novo and novo != nome:
                de, para = os.path.join(dp, nome), os.path.join(dp, novo)
                if os.path.exists(para):
                    continue
                if not dry:
                    try:
                        os.rename(de, para)
                    except OSError as e:
                        recusados.append((nome, f"falhou ao renomear: {e}")); continue
                feitos.append((os.path.relpath(de, pasta), os.path.relpath(para, pasta)))
    trocas.extend(("(renomeado)", "nome-arquivo", a, b) for a, b in feitos)
    trocas.extend(("(preservado)", "nome-arquivo-recusado", a, b) for a, b in recusados)
    return feitos

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pasta")
    ap.add_argument("--nome", default=None)
    ap.add_argument("--seed", default=None)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()

    pasta = os.path.abspath(a.pasta)
    if not os.path.isdir(pasta):
        print(f"ERRO: nao existe: {pasta}"); sys.exit(1)

    semente = a.seed or hashlib.sha256(pasta.encode()).hexdigest()
    nome = a.nome or inventa_nome(semente)

    ctx = {
        "nome_curto": nome,
        "pkg_npm": nome.lower(),
        "pacote": inventa_pacote(semente),
        "autor": inventa_nome(semente + "autor"),
        "url": "https://" + nome.lower() + ".dev",
        "versao": inventa_versao(semente),
        "appid": "com." + inventa_pacote(semente),
    }

    print("=" * 72)
    print("  LIMPEZA DE IDENTIDADE — ER BLACK")
    print("=" * 72)
    print(f"  clone      : {pasta}")
    print(f"  nome novo  : {ctx['nome_curto']}")
    print(f"  pacote     : {ctx['pacote']}")
    print(f"  autor      : {ctx['autor']}")
    print(f"  url        : {ctx['url']}")
    print(f"  appid      : {ctx['appid']}")
    print(f"  versao     : {ctx['versao']}")
    print(f"  modo       : {'SIMULACAO (nada gravado)' if a.dry else 'GRAVANDO'}")
    print("=" * 72)

    regras = monta_regras(ctx)
    trocas, pendencias = varre(pasta, regras, a.dry)
    renomeados = limpa_nome_arquivo(pasta, trocas, a.dry)

    print(f"\n  trocas de texto : {len(trocas)}")
    print(f"  arquivos renomeados: {len(renomeados)}")
    print(f"  pendencias      : {len(pendencias)}")

    if trocas:
        print("\n  --- amostra das trocas ---")
        for rel, rot, de, para in trocas[:25]:
            print(f"    [{rot}] {rel}")
            print(f"        de : {de[:70]}")
            print(f"        para: {para[:70]}")
    if pendencias:
        print("\n  --- pendencias ---")
        for rel, m in pendencias[:15]:
            print(f"    {rel}  ->  {m}")

    # ------------------------------------------------ relatorio
    out = os.path.join(pasta, "ER-LIMPEZA")
    if not a.dry:
        os.makedirs(out, exist_ok=True)
        L = []
        L.append(f"# Limpeza de identidade — {ctx['nome_curto']}\n")
        L.append(f"> Gerado por `limpar-identidade.py` em {datetime.now():%Y-%m-%d %H:%M}\n")
        L.append(f"> Clone: `{pasta}`\n")
        L.append("\n## Valores inventados neste clone\n")
        L.append("| campo | valor |\n|---|---|")
        for k, v in ctx.items():
            L.append(f"| {k} | `{v}` |")
        L.append(f"\n## Trocas aplicadas: {len(trocas)}\n")
        L.append("| arquivo | campo | de | para |\n|---|---|---|---|")
        for rel, rot, de, para in trocas:
            L.append(f"| `{rel}` | {rot} | `{de}` | `{para}` |")
        L.append(f"\n## Arquivos renomeados: {len(renomeados)}\n")
        for de, para in renomeados:
            L.append(f"- `{de}` → `{para}`")
        L.append(f"\n## Pendencias ({len(pendencias)})\n")
        for rel, m in pendencias:
            L.append(f"- `{rel}`: {m}")
        L.append("\n## Itens que o script NAO consegue julgar sozinho\n")
        L.append("- Icones e imagens de marca (precisa nova identidade visual).")
        L.append("- Nomes de janela desenhados em canvas/runtime.")
        L.append("- Metadados de assinatura digital do executavel.")
        L.append("- Strings embutidas em binarios (.node/.dll/.exe) — requer Etapa de binario.")
        open(os.path.join(out, "01-relatorio.md"), "w", encoding="utf-8").write("\n".join(L))
        json.dump({"ctx": ctx, "trocas": trocas, "renomeados": renomeados,
                   "pendencias": pendencias},
                  open(os.path.join(out, "02-mapa.json"), "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
        P = ["# Pendencias — olho humano\n",
             "\nEstas NAO foram resolvidas automaticamente. Nao entregue sem tratar:\n"]
        for rel, m in pendencias:
            P.append(f"- [ ] `{rel}` — {m}")
        P.append("\n- [ ] Conferir aba de titulo da janela rodando.")
        P.append("- [ ] Conferir icone na barra de tarefas.")
        P.append("- [ ] Conferir nome no Gerenciador de Tarefas.")
        P.append("- [ ] Conferir rodape/sobre do app.")
        open(os.path.join(out, "03-pendencias.md"), "w", encoding="utf-8").write("\n".join(P))
        print(f"\n  [salvo] {os.path.join(out,'01-relatorio.md')}")
        print(f"  [salvo] {os.path.join(out,'02-mapa.json')}")
        print(f"  [salvo] {os.path.join(out,'03-pendencias.md')}")

if __name__ == "__main__":
    main()
