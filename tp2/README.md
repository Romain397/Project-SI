Créer une base de données `gameboards` sur l'instance postgres exécuté au sein d'un conteneur Docker.
La base doit être automatiquement créée au démarrage du conteneur.

Tout doit tenir :
    Impératif : `docker run ...

    Déclaratif : `compose.yaml`

Tester le démarrage et la présence des objets demandés

```bash
docker run --rm  --name gameboard_db -e POSTGRES_PASSWORD=password -e POSTGRES_DB=gameboards -v "./data:/docker-entrypoint-initdb.d" -p 5432:5432 postgres:latest
```

Utiliser le fichier `compose.yaml` pour créer le service.

```bash
docker compose up -d
```

Conversion en docker compose


```bash
docker exec -it gameboard_db psql -h localhost -U postgres
```

```bash
docker compose exec gameboard_db psql -h localhost -U postgres gameboards
```

