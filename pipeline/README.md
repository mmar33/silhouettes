# Pipeline des silhouettes (site SCAR)

Ce dossier sert à mettre à jour automatiquement la page `scar.html` (arbre circulaire des Carnivora + carnivores domestiques), intégrée sur https://www.scar-team.com/3d-data par l'adresse https://mmar33.github.io/silhouettes/scar.html.

## Sources
- Fichier maître des silhouettes (ordinateur de Margot, Dropbox) :
  `C:\Users\mmar3\M.mar33 Dropbox\Margot Michaud\Dossier pro\Illustrations\Phylopic\Phylopic.svg`
  Chaque silhouette a son nom d'espèce écrit en dessous (flowRoot).
- Races domestiques : fichier `Phylopic - domestic.svg` dans le même dossier, tableau de lignes (nom français, nom anglais, n° FCI) avec l'icône à gauche (voir `work/domrows.py`, `work/build_dom.py`).
- Arbre : Upham et al. 2019 (`tree/carnivora_upham.nwk`), espèces nouvelles et fossiles greffés à la main dans `tree/build_tree.py`, âges dans `tree/ages.py` (Paleobiology Database).

## État
- `work/wild_index.json` : silhouettes sauvages et fossiles déjà publiées (nom, fichier, éteint ou non, famille).
- `work/dom_index.json` : silhouettes domestiques déjà publiées.
- `tree/old_art.json` : silhouettes historiques (273, couleurs d'origine).
- `state.json` : dates de modification (mtimeMs) de Phylopic.svg et de « Phylopic - domestic.svg » au dernier passage, et points en suspens.

## Ajouter de nouvelles silhouettes
1. Récupérer Phylopic.svg, lancer `work/extract_master.py` puis `work/match2.py` (associe chaque silhouette à son nom).
2. Garder seulement les noms absents de `wild_index.json`, `dom_index.json` et `tree/cur_map.json` (valeurs).
3. Vérifier chaque nom dans la taxonomie en vigueur (MDD pour les actuels, PBDB pour les fossiles) ; harmoniser sans demander et le signaler (Neovison → Neogale, Aonyx → Lutra...). Les sous-espèces sont acceptées.
4. Écrire les SVG (noir, détails blancs conservés, `<title>{nom} — silhouette © Margot Michaud (CC0)</title>`, préfixe `† ` pour les éteints) à la racine du dépôt, ou dans `domestic/dogs|cats|other` ; ajouter les entrées dans les index (`work/build_wild.py`, `work/build_dom.py`).
5. Placer chaque nouvelle espèce dans l'arbre : `sister(ref, nom)` pour une espèce actuelle proche d'une existante, `graft(mrca(...), G(Famille, nom))` pour un fossile, âge dans `tree/ages.py`. Famille dans `work/fam.py` si nouveau genre ; nouvelle famille fossile : ajouter une couleur dans `tree/bbox.py` (COL, n'importe laquelle, la couleur affichée vient du dégradé).
6. `bash pipeline/build.sh` puis vérifier (`node tree/shot.js` si présent, ou capture Playwright) : 0 erreur JS, toutes les silhouettes, aucun chevauchement (`hits 0`).
7. Commit + push sur `main` (push direct possible : application GitHub Claude installée sur le dépôt le 07/11/2026). GitHub Pages se met à jour en 1 à 2 minutes ; Wix suit tout seul.

## Rendu
- Couleurs : une couleur par famille, dégradé OKLCH dans l'ordre des familles autour du cercle (fonction `fcol` dans `tree/render.py`).
- Silhouettes : même boîte pour toutes (84 × 54), 5 rangées, réduction automatique en cas de chevauchement.
- Page en anglais (`site/translate_en.py`), domestiques en vignettes paginées (84 par page).
