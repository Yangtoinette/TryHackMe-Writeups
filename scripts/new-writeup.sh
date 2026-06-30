#!/usr/bin/env bash
# Usage : ./scripts/new-writeup.sh "Nom du challenge"
# Crée writeups/nom-du-challenge.html depuis le template.

NAME="${1}"
if [[ -z "$NAME" ]]; then
  echo "Usage : $0 'Nom du challenge'"
  exit 1
fi

SLUG=$(echo "$NAME" \
  | tr '[:upper:]' '[:lower:]' \
  | sed 's/[àáâä]/a/g; s/[éèêë]/e/g; s/[îï]/i/g; s/[ôö]/o/g; s/[ùûü]/u/g; s/ç/c/g' \
  | sed 's/[^a-z0-9]/-/g' \
  | sed 's/-\+/-/g; s/^-//; s/-$//')

SRC="writeups/TEMPLATE.html"
DST="writeups/${SLUG}.html"

[[ ! -f "$SRC" ]] && echo "Template introuvable : $SRC" && exit 1
[[ -f  "$DST" ]] && echo "Fichier déjà existant : $DST" && exit 1

cp "$SRC" "$DST"
echo "✓ Créé : $DST"
echo ""
echo "Étapes :"
echo "  1. Remplir le bloc META en haut du fichier"
echo "  2. Écrire le contenu du write-up"
echo "  3. git add $DST && git commit -m \"add: ${SLUG}\" && git push"
