import re
SKIP_EXISTING={'spetheos venaticus','octolobus manul','Profelis aurata','Lynx','artictis binturong','nandinia','arctogalidia trivirgata','profelis aurata','Caracal','puma concolor','Proteles','Genetta felina','Genette maculata','Captopuma temminckii','Captopuma badia','Leopardus jacobitus','Herpestes edwardsii','Lupulella mesomela','Urocyon cinereoargentus','Lycalopex gymnocerus','Lycalopes griseus','Lycalopex vertulus','Nyctereutes procyonides','Alopex lagopus','Canis adustus','Canis mesomelas','cuon alpinus','prionodon linsang','Ursus malayanus','Hydruga leptonyx','Monachus schauinslandi','Mirounga angustirostrid','Procyon cancrivorous','Lycaon pictis','Parahyaenna brunnea','prionodon pardicolor','arctonyx collaris','Herpestes javanicus','Amblonyx cinereus','Galictis viattata','Melogale mochata','Ictonyx libyca','Bassaricyon sp.','Prosansanosmilus drawing'}
DOMESTIC={'Felis catus':'Felis catus','Mustela furo':'Mustela putorius furo','Ligre':'Liger (Panthera leo × P. tigris)'}
RENAME={'Crocuta spelea':'Crocuta crocuta spelaea','Hyaena perrieri':'Pliocrocuta perrieri','Cryptoprocta ferox spelea':'Cryptoprocta spelea',
'homotherium latidens':'Homotherium latidens','cephalogale gracile':'Cephalogale gracile','Megantereon sp':'Megantereon sp.','Brachypsalis sp':'Brachypsalis sp.','Cernictis sp':'Cernictis sp.',
'Smilodon':'Smilodon sp.','Hyaena brevirostris':'Pachycrocuta brevirostris','Tomarctus temerarius':'Paratomarctus temerarius','Canis adoxus':'Eucyon adoxus',
'Viverravidae':'Viverravidae Unident','Hyainailouroidea':'Hyainailouroidea Unident','Limnocyoninae':'Limnocyoninae Unident'}
EXTINCT_RECENT={'Dusicyon australis','Dusicyon avus','Neomonachus tropicalis','Zalophus japonicus','Neogale macrodon','Lutra nippon','Cryptoprocta spelea','Crocuta crocuta spelaea'}
EXTANT_NEW={'Canis lycaon','Nyctereutes viverrinus','Paradoxurus musanga','Paradoxurus philippinensis','Urva auropunctata','Bdeogale omnivora','Canis lupaster','Proteles septentrionalis','Pusa saimensis','Pusa sibirica','Ailurus styani','Bassaricyon gabbii','Bassaricyon medius','Canis lupus dingo','Canis lupus italicus','Leopardus pardinoides','Leopardus tilcayo','Leopardus emiliae','Leopardus guttulus','Leopardus pajeros','Leopardus braccatus','Leopardus fasciatus','Prionailurus javanensis','Leopardus garleppi','Felis lybica','Melogale cucphuongensis','Mustela mopbie','Conepatus amazonicus','Spilogale interrupta','Spilogale leucoparia','Spilogale yucatanensis','Melogale subaurantiaca','Mustela haidarum','Arctonyx albogularis','Arctonyx hoevenii','Meles amurensis','Meles canescens','Lontra annectens','Martes caurina','Lutra congica','Vulpes rueppellii','Mustela aistoodonnivalis','Mustela richardsonii'}
def canon(raw):
    n=re.sub(r'\s+',' ',raw.replace('_',' ')).strip()
    if n in SKIP_EXISTING: return None
    if n in DOMESTIC: return ('domestic',DOMESTIC[n])
    n=RENAME.get(n,n)
    if n in EXTANT_NEW: return ('extant',n)
    if n in EXTINCT_RECENT: return ('extinct',n)
    return ('fossil',n)
