#!/bin/bash
# Reconstruit l'arbre et la page SCAR (scar.html) a partir de pipeline/ et des SVG du depot.
# usage : bash pipeline/build.sh   (depuis la racine du depot)
set -e
ROOT=$(cd "$(dirname "$0")/.." && pwd); P=$ROOT/pipeline
cd $P/tree
python3 build_tree.py
python3 bbox.py
node bb.js
python3 render.py
python3 $P/site/build_site.py $P/tree/carnivora_arbre.html $P/work/dom_index.json $ROOT/scar.html
cp $P/tree/carnivora_arbre.html $ROOT/arbre.html
rm -f $P/tree/allart.html
echo "scar.html et arbre.html reconstruits"
