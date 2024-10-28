
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
   git clone https://github.com/victor49100/GameSaves
   cd GameSaves
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

4. Créez la base de données SQLite `SaveBdd.sqlite` dans le répertoire `backend` en exécutant le script SQL `create_db.sql`. Assurez-vous que SQLite est installé sur votre machine.

   ```bash
   sqlite3 SaveBdd.sqlite < create_db.sql
   ```

5. Démarrez le backend avec un port spécifique (optionnel). Par défaut, le port `8000` est utilisé. Pour choisir un autre port, définissez la variable d'environnement `BACKEND_PORT` et lancez le serveur :

   ```bash
   BACKEND_PORT=5555 python main.py
   ```
### Frontend (React)

1. Accédez au répertoire `frontend` et installez les dépendances :

   ```bash
   cd ../frontend
   npm install
   ```

2. Démarrez le frontend en spécifiant un port (optionnel). Par défaut, le port `5173` est utilisé. Pour changer le port, définissez la variable d'environnement `FRONTEND_PORT` et lancez le projet :

   ```bash
   FRONTEND_PORT=3000 npm run dev
   ```

### API Backend

Le backend expose une API REST que vous pouvez consulter et tester via la documentation interactive Swagger disponible à l'URL suivante :

```
http://localhost:<BACKEND_PORT>/docs
```
