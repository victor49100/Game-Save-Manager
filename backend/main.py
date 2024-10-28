# main.py

import os
import shutil
from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Initialisation de FastAPI
app = FastAPI()

# Configuration CORS pour autoriser toutes les origines
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autoriser toutes les origines
    allow_credentials=True,
    allow_methods=["*"],  # Autoriser toutes les méthodes HTTP
    allow_headers=["*"],  # Autoriser tous les headers
)

# Création du moteur SQLAlchemy pour SQLite
DATABASE_URL = "sqlite:///./SaveBdd.sqlite"
engine = create_engine(DATABASE_URL, echo=True)

# Déclaration de la base pour SQLAlchemy ORM
Base = declarative_base()

# Session SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modèles de la base de données
class Game(Base):
    __tablename__ = "games"
    game_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    AppID = Column(String, unique=True, nullable=False)  # Identifiant unique du jeu

class Save(Base):
    __tablename__ = "saves"
    save_id = Column(Integer, primary_key=True, autoincrement=True)
    game_id = Column(Integer, ForeignKey('games.game_id'), nullable=False)
    save_path = Column(Text, nullable=False)
    backup_path = Column(Text, nullable=False)  # Chemin du répertoire de sauvegarde
    save_date = Column(DateTime, default=datetime.utcnow)

class SaveCreateRequest(BaseModel):
    save_path: str

# Crée les tables dans la base de données si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Fonction pour récupérer la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Répertoire de sauvegarde local
LOCAL_SAVE_DIR = "saves"

# Modèles pour copier et restaurer des fichiers
class SaveOperation(BaseModel):
    AppID: str
    savePath: str

class RestoreSaveOperation(BaseModel):
    AppID: str
    backup_path: str

# Fonction pour générer un sous-dossier horodaté dans le dossier de l'AppID
def generate_timestamped_backup_dir(AppID):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(LOCAL_SAVE_DIR, AppID, f"backup_{timestamp}")

# Route pour copier la sauvegarde dans un répertoire local et enregistrer le chemin dans la base de données
@app.post("/copySaveToLocal")
async def copy_save_to_local(save_operation: SaveOperation, db: Session = Depends(get_db)):
    # Rechercher le jeu via l'AppID
    game = db.query(Game).filter(Game.AppID == save_operation.AppID).first()

    if not game:
        raise HTTPException(status_code=404, detail="Jeu non trouvé avec cet AppID.")

    # Créer le dossier AppID s'il n'existe pas
    app_save_dir = os.path.join(LOCAL_SAVE_DIR, save_operation.AppID)
    os.makedirs(app_save_dir, exist_ok=True)

    # Générer un nom de sous-dossier avec la date et l'heure actuelle
    backup_dir = generate_timestamped_backup_dir(save_operation.AppID)
    os.makedirs(backup_dir, exist_ok=True)

    # Copier les fichiers dans le dossier de backup
    if os.path.isdir(save_operation.savePath):
        for root, dirs, files in os.walk(save_operation.savePath):
            relative_path = os.path.relpath(root, save_operation.savePath)
            backup_root = os.path.join(backup_dir, relative_path)
            os.makedirs(backup_root, exist_ok=True)
            for file in files:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(backup_root, file)
                shutil.copy2(source_file, destination_file)
    else:
        shutil.copy2(save_operation.savePath, backup_dir)

    # Enregistrer le chemin du backup dans la base de données
    new_save = Save(game_id=game.game_id, save_path=save_operation.savePath, backup_path=backup_dir)
    db.add(new_save)
    db.commit()

    return {"message": "Sauvegarde copiée dans le dossier local", "local_path": backup_dir}

# Route pour restaurer une sauvegarde depuis le répertoire local
@app.post("/restoreSaveFromLocal")
async def restore_save_from_local(restore_operation: RestoreSaveOperation, db: Session = Depends(get_db)):
    # Rechercher le jeu via l'AppID
    game = db.query(Game).filter(Game.AppID == restore_operation.AppID).first()

    if not game:
        raise HTTPException(status_code=404, detail="Jeu non trouvé avec cet AppID.")

    # Récupérer la sauvegarde associée
    save = db.query(Save).filter(Save.game_id == game.game_id, Save.backup_path == restore_operation.backup_path).first()

    if not save:
        raise HTTPException(status_code=404, detail="Sauvegarde non trouvée.")

    backup_path = save.backup_path
    original_save_path = save.save_path

    # Vérifier que le backup existe
    if not os.path.exists(backup_path):
        raise HTTPException(status_code=404, detail="Chemin de backup introuvable")

    # Restaurer la sauvegarde
    if os.path.isdir(backup_path):
        for root, dirs, files in os.walk(backup_path):
            relative_path = os.path.relpath(root, backup_path)
            restore_root = os.path.join(original_save_path, relative_path)
            os.makedirs(restore_root, exist_ok=True)
            for file in files:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(restore_root, file)
                shutil.copy2(source_file, destination_file)
    else:
        shutil.copy2(backup_path, original_save_path)

    return {"message": f"Sauvegarde restaurée avec succès."}

# API Endpoints pour ajouter et gérer les jeux
@app.post("/addGame/{title}/{AppID}")
async def add_game(title: str, AppID: str, db: Session = Depends(get_db)):
    existing_game = db.query(Game).filter(Game.AppID == AppID).first()
    if existing_game:
        raise HTTPException(status_code=400, detail="Le jeu existe déjà.")

    new_game = Game(title=title, AppID=AppID)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return {"game_id": new_game.game_id, "title": new_game.title, "AppID": new_game.AppID}

@app.get("/games/")
async def get_all_games(db: Session = Depends(get_db)):
    games = db.query(Game).all()
    return games

# API pour récupérer les sauvegardes d'un jeu via game_id
@app.get("/saves/{game_id}")
async def get_saves_for_game(game_id: int, db: Session = Depends(get_db)):
    # Rechercher le jeu via game_id
    game = db.query(Game).filter(Game.game_id == game_id).first()

    if not game:
        raise HTTPException(status_code=404, detail="Jeu non trouvé avec cet game_id.")

    saves = db.query(Save).filter(Save.game_id == game.game_id).all()
    return saves

# Route pour supprimer une sauvegarde et son répertoire de backup
@app.delete("/saves/{save_id}")
async def delete_save(save_id: int, db: Session = Depends(get_db)):
    # Récupérer la sauvegarde à partir de l'ID
    save = db.query(Save).filter(Save.save_id == save_id).first()

    if not save:
        raise HTTPException(status_code=404, detail="Sauvegarde non trouvée.")

    # Vérifier si le chemin du dossier de backup est présent
    backup_path = save.backup_path
    if not backup_path:
        raise HTTPException(status_code=404, detail="Aucun chemin de sauvegarde enregistré.")

    # Supprimer le dossier de backup
    if os.path.exists(backup_path):
        try:
            shutil.rmtree(backup_path)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression du dossier : {str(e)}")

    # Supprimer l'entrée de la sauvegarde dans la base de données
    db.delete(save)
    db.commit()

    return {"message": f"Backup {backup_path} supprimé avec succès."}

# Route pour supprimer un jeu
@app.delete("/games/{game_id}")
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    # Récupérer le jeu par game_id
    game = db.query(Game).filter(Game.game_id == game_id).first()

    if not game:
        raise HTTPException(status_code=404, detail="Jeu non trouvé.")

    # Supprimer les sauvegardes associées et leurs dossiers de backup
    saves = db.query(Save).filter(Save.game_id == game.game_id).all()
    for save in saves:
        backup_path = save.backup_path
        if os.path.exists(backup_path):
            try:
                shutil.rmtree(backup_path)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression du dossier : {str(e)}")
        db.delete(save)

    # Supprimer le jeu
    db.delete(game)
    db.commit()

    return {"message": f"Jeu '{game.title}' supprimé avec succès."}

# Route de base

@app.get("/")
async def root():
    return {"message": "Bienvenue dans l'API de sauvegarde de jeux"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("BACKEND_PORT", 8000))  # Utilisation de la variable d'environnement pour le port
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)