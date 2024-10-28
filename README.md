
# Game Save Manager

**Game Save Manager** est une application permettant de gérer les sauvegardes de jeux vidéo. Elle est composée de deux parties :
- Un backend en **FastAPI**.
- Un frontend en **React**.

## Prérequis

- **Python 3.10** ou plus pour le backend.
- **Node.js 16** ou plus pour le frontend.
- **SQLite** pour la base de données.

## Installation et configuration

### Backend (FastAPI)

1. Clonez le repository et accédez au répertoire `backend` :

   ```bash
   git clone https://github.com/votre-repository.git
   cd backend
   ```

2. Créez et activez un environnement virtuel Python :

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Installez les dépendances Python à l'aide du fichier `requirements.txt` :

   ```bash
   pip install -r requirements.txt
   ```

4. Démarrez le backend avec un port spécifique (optionnel). Par défaut, le port `8000` est utilisé. Pour choisir un autre port, définissez la variable d'environnement `BACKEND_PORT` et lancez le serveur :

   ```bash
   BACKEND_PORT=5555 python main.py
   ```

   Si vous ne spécifiez pas de port, le serveur utilisera le port par défaut `8000` :

   ```bash
   python main.py
   ```

   Le backend sera disponible à `http://localhost:<BACKEND_PORT>`.

### Frontend (React)

1. Accédez au répertoire `frontend` et installez les dépendances :

   ```bash
   cd ../frontend
   npm install
   ```

2. Créez un fichier `.env` à la racine du répertoire `frontend` pour configurer l'URL du backend. Par défaut, le backend utilise le port `8000`, mais vous pouvez changer ce port si nécessaire :

   **.env**

   ```env
   VITE_BACKEND_URL=http://localhost:8000
   ```

3. Démarrez le frontend en spécifiant un port (optionnel). Par défaut, le port `5173` est utilisé. Pour changer le port, définissez la variable d'environnement `FRONTEND_PORT` et lancez le projet :

   ```bash
   FRONTEND_PORT=3000 npm run dev
   ```

   Sinon, démarrez avec le port par défaut :

   ```bash
   npm run dev
   ```

   Le frontend sera disponible à `http://localhost:<FRONTEND_PORT>`.

### Utilisation

Une fois les deux serveurs démarrés (backend et frontend), vous pouvez accéder à l'interface utilisateur pour gérer vos sauvegardes de jeux.

### API Backend

Le backend expose une API REST que vous pouvez consulter et tester via la documentation interactive Swagger disponible à l'URL suivante :

```
http://localhost:<BACKEND_PORT>/docs
```

### Frontend

Le frontend vous permet de gérer les jeux, d'ajouter des sauvegardes, de restaurer des sauvegardes depuis des backups, et de supprimer des jeux ou des sauvegardes.

## Variables d'environnement

- **BACKEND_PORT** : Le port sur lequel le backend FastAPI sera exposé (par défaut: 8000).
- **FRONTEND_PORT** : Le port sur lequel le frontend React sera exposé (par défaut: 5173).
- **VITE_BACKEND_URL** : L'URL du backend utilisée par le frontend. Par défaut `http://localhost:8000`.

## Dépendances

### Backend

Les dépendances du backend sont gérées via le fichier `requirements.txt` et incluent :

- **FastAPI**
- **Pydantic**
- **Uvicorn**
- **SQLAlchemy**

Pour installer ces dépendances, utilisez la commande :

```bash
pip install -r requirements.txt
```

### Frontend

Les dépendances du frontend sont gérées via le fichier `package.json` et incluent :

- **React**
- **Axios**
- **FontAwesome**

Pour installer ces dépendances, utilisez la commande :

```bash
npm install
```

## Démarrage rapide

1. **Backend** :
   - Créez et activez un environnement virtuel Python.
   - Installez les dépendances via `pip install -r requirements.txt`.
   - Lancez le serveur avec un port personnalisé ou laissez-le utiliser le port par défaut (8000).

2. **Frontend** :
   - Installez les dépendances via `npm install`.
   - Lancez le frontend avec un port personnalisé ou laissez-le utiliser le port par défaut (5173).

```bash
# Démarrage du backend avec un port spécifique
BACKEND_PORT=5555 python main.py

# Démarrage du frontend avec un port spécifique
FRONTEND_PORT=3000 npm run dev
```

## Structure du projet

```
.
├── backend
│   ├── main.py                # Code principal de l'API FastAPI
│   ├── requirements.txt        # Dépendances Python
│   └── SaveBdd.sqlite          # Fichier de base de données SQLite (créé au lancement)
├── frontend
│   ├── src/
│   ├── package.json            # Fichier des dépendances frontend
│   ├── vite.config.js          # Configuration de Vite pour le frontend
│   ├── .env                    # Fichier pour les variables d'environnement du frontend
│   └── public/
└── README.md                   # Documentation du projet
```

## Contributeurs

Si vous souhaitez contribuer au projet, n'hésitez pas à soumettre une pull request ou à ouvrir une issue sur le repository GitHub.
