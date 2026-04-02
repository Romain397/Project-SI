## TP3 - Architectures de communication

Ce dossier contient une implementation complete du CRUD "jeu de societe"
avec les champs obligatoires `title`, `author` et `content`.

### 1. Architecture monolithique

```bash
py -3.13 tp3/bib.py
```

Les donnees sont persistees dans `tp3/bib_data.json`.

### 2. Architecture client/serveur TCP JSON

Terminal 1 :

```bash
py -3.13 tp3/bib_server.py
```

Terminal 2 :

```bash
py -3.13 tp3/bib_client.py
```

### 3. Architecture client/serveur HTTP JSON

Terminal 1 :

```bash
py -3.13 tp3/bib_http_server.py
```

Terminal 2 :

```bash
py -3.13 tp3/bib_http_client.py
```

### 4. Architecture 3-tier HTTP -> TCP -> SQLite

Terminal 1 :

```bash
py -3.13 tp3/bib_server_tier_2.py
```

Terminal 2 :

```bash
$env:BIB_HTTP_BACKEND='tcp'
$env:BIB_TCP_BACKEND_PORT='9998'
py -3.13 tp3/bib_http_server.py
```

Terminal 3 :

```bash
py -3.13 tp3/bib_http_client.py
```

Les donnees du tier 2 sont persistees dans `tp3/bib.sqlite3`.

### Actions disponibles

- `c` : creer un jeu
- `u` : mettre a jour un jeu
- `g` : consulter un jeu
- `l` : lister tous les jeux
- `d` : supprimer un jeu
- `h` : aide
- `q` : quitter
