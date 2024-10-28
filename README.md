
# Game Save Manager

**Game Save Manager** est une application permettant de gérer les sauvegardes de jeux vidéo.

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

4. Créez la base de données SQLite `SaveBdd.sqlite` dans le répertoire `backend` :

   ```bash
   sqlite3 SaveBdd.sqlite < create_db.sql
   ```

5. Démarrez le backend avec un port spécifique :

   ```bash
   BACKEND_PORT=5555 python main.py
   ```
### Frontend (React)

1. Accédez au répertoire `frontend` et installez les dépendances :

   ```bash
   cd ../frontend
   npm install
   ```

2. Démarrez le frontend en spécifiant un port :
   ```bash
   FRONTEND_PORT=3000 npm run dev
   ```
