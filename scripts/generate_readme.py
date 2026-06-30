#!/usr/bin/env python3
"""
generate_readme.py — Repo HTML
Scanne writeups/*.html, lit le bloc <!--META...META-->,
et met à jour uniquement la section entre les balises
<!-- WRITEUPS:START --> et <!-- WRITEUPS:END --> dans README.md.

Si les balises sont absentes, le README est créé depuis zéro.
Lancer manuellement : python3 scripts/generate_readme.py
"""
import re
from pathlib import Path
from datetime import datetime

# ── À modifier avant le premier push ─────────────────────────────────────────
GITHUB_USERNAME    = "Yangtoinette"       # ← ton pseudo GitHub
GITHUB_REPO        = "TryHackMe-Writeups"      # ← nom du repo
PAGES_URL          = f"https://{GITHUB_USERNAME}.github.io/{GITHUB_REPO}"
README_TITLE       = "OSINT Write-ups"
README_DESCRIPTION = "Résolutions de challenges OSINT — rendu visuel dark terminal."
# ─────────────────────────────────────────────────────────────────────────────

WRITEUPS_DIR  = Path("writeups")
README_PATH   = Path("README.md")
MARKER_START  = "<!-- WRITEUPS:START -->"
MARKER_END    = "<!-- WRITEUPS:END -->"


def extract_meta(filepath):
    """Lit le bloc <!--META\\n...\\nMETA--> en tête de fichier HTML."""
    text = filepath.read_text(encoding="utf-8")
    match = re.search(r"<!--META\n(.*?)\nMETA-->", text, re.DOTALL)
    if not match:
        print(f"  [!] Pas de bloc META dans {filepath.name} — ignoré")
        return None
    meta = {}
    for line in match.group(1).strip().splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            meta[key.strip().lower()] = val.strip()
    meta["_file"] = filepath.name
    return meta


def build_table(entries):
    if not entries:
        return "_Aucun write-up pour le moment._\n"
    rows = [
        "| Challenge | Plateforme | Catégorie | Difficulté | Date | Points |",
        "|:----------|:-----------|:----------|:-----------|:-----|-------:|",
    ]
    for e in sorted(entries, key=lambda x: x.get("date", ""), reverse=True):
        title = e.get("title", e["_file"].replace(".html", ""))
        url   = f"{PAGES_URL}/writeups/{e['_file']}"
        rows.append(
            f"| [{title}]({url}) "
            f"| {e.get('platform', '-')} "
            f"| {e.get('category', '-')} "
            f"| {e.get('difficulty', '-')} "
            f"| {e.get('date', '-')} "
            f"| {e.get('points', '-')} |"
        )
    return "\n".join(rows) + "\n"


def update_readme(table):
    """
    Si les balises WRITEUPS:START / END existent dans README.md,
    ne met à jour que cette section — le reste est préservé.
    Sinon, crée un README depuis zéro.
    """
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    block = (
        f"{MARKER_START}\n"
        f"<!-- Dernière mise à jour : {now} UTC -->\n\n"
        f"{table}\n"
        f"{MARKER_END}"
    )

    if README_PATH.exists():
        content = README_PATH.read_text(encoding="utf-8")
        if MARKER_START in content and MARKER_END in content:
            # Remplacer uniquement ce qui est entre les balises
            updated = re.sub(
                re.escape(MARKER_START) + r".*?" + re.escape(MARKER_END),
                block,
                content,
                flags=re.DOTALL,
            )
            README_PATH.write_text(updated, encoding="utf-8")
            print("README.md mis à jour (section write-ups uniquement)")
            return

    # Pas de balises ou pas de fichier → création depuis zéro
    README_PATH.write_text(
        f"# {README_TITLE}\n\n"
        f"{README_DESCRIPTION}\n\n"
        f"---\n\n"
        f"{block}\n\n"
        f"---\n\n"
        f"*Généré par [scripts/generate_readme.py](scripts/generate_readme.py)*\n",
        encoding="utf-8",
    )
    print("README.md créé depuis zéro")


def main():
    entries = []
    if WRITEUPS_DIR.exists():
        for f in sorted(WRITEUPS_DIR.glob("*.html")):
            if f.stem.upper() == "TEMPLATE":
                continue
            meta = extract_meta(f)
            if meta:
                entries.append(meta)
    print(f"{len(entries)} write-up(s) trouvé(s)")
    update_readme(build_table(entries))


if __name__ == "__main__":
    main()
