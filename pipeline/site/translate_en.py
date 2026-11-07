import sys,re
REP=[
('lang="fr"','lang="en"'),
('<title>Silhouettes de Carnivora</title>','<title>Carnivora silhouettes</title>'),
(' espèces et sous-espèces actuelles · ',' extant species and subspecies · '),
(' taxons éteints ou fossiles (†)',' extinct or fossil taxa (†)'),
('Phylogénie datée des espèces actuelles : Upham et al. 2019 (PLoS Biol), arbre MCC node-dated','Dated phylogeny of extant species: Upham et al. 2019 (PLoS Biol), node-dated MCC tree'),
('Fossiles et espèces récemment reconnues ajoutés à la main, positions et âges approximatifs (Paleobiology Database) · * hors Carnivora','Fossils and recently recognised species added by hand, approximate positions and ages (Paleobiology Database) · * outside Carnivora'),
('Silhouettes : Margot Michaud (CC0)','Silhouettes: Margot Michaud (CC0)'),
('Carnivoraformes (stem)','Carnivoraformes (stem)'),
('title="Zoomer"','title="Zoom in"'),('title="Dézoomer"','title="Zoom out"'),('title="Vue entière"','title="Full view"'),('title="Fermer"','title="Close"'),
('<b>Clic droit sur l\'aperçu</b> &rarr; « Enregistrer l\'image sous… »\n       — cette méthode fonctionne partout, même quand le site bloque les téléchargements.','<b>Right-click the preview</b> &rarr; "Save image as…". This always works, even when the site blocks downloads.'),
('Ouvrir dans un onglet','Open in a new tab'),('Enregistrer le SVG','Save SVG'),('Copier le code SVG','Copy SVG code'),('Copié ✓','Copied ✓'),
('Cliquer pour télécharger (SVG)','Click to download (SVG)'),
('Téléchargement lancé. Rien ne se passe&nbsp;? <b>Cliquez ici</b>.','Download started. Nothing happened? <b>Click here</b>.'),
('Votre navigateur a bloqué l’ouverture de l’onglet de téléchargement. Autorisez les fenêtres surgissantes pour ce site, ou utilisez une des solutions ci-dessous.','Your browser blocked the download tab. Allow pop-ups for this site, or use one of the options below.'),
("Si le fichier ne s'est pas enregistré, le site bloque les téléchargements automatiques dans cette page. Utilisez l'une des solutions ci-dessous.","If the file was not saved, this page blocks automatic downloads. Use one of the options below."),
('<h1>CARNIVORES DOMESTIQUES</h1>','<h1>DOMESTIC CARNIVORANS</h1>'),
('Races de chiens et de chats, et autres carnivores domestiques · Margot Michaud · CC0, libres de droits. Cliquez sur une silhouette pour télécharger le fichier SVG.','Dog and cat breeds, and other domestic carnivorans · Margot Michaud · CC0, free to use. Click a silhouette to download the SVG file.'),
('>Chiens<','>Dogs<'),('>Chats<','>Cats<'),('>Autres domestiques<','>Other<'),
('placeholder="Rechercher un nom…"','placeholder="Search a name…"'),
('Aucune silhouette ne correspond.','No matching silhouette.'),
('Races de chiens selon la nomenclature FCI (numéro de standard affiché au survol).','Dog breeds follow the FCI nomenclature (standard number shown on hover).'),
('Toutes les familles','All families'),
# English breed names displayed, no French subtitle
("f:'domestic/'+r[0],t:r[1],e:r[2],fci:r[3],","f:'domestic/'+r[0],t:r[2],e:'',fci:r[3],"),
("a.t.localeCompare(b.t,'fr')","a.t.localeCompare(b.t,'en')"),
]
for fn in sys.argv[1:]:
    t=open(fn).read()
    for a,b in REP: t=t.replace(a,b)
    open(fn,'w').write(t)
