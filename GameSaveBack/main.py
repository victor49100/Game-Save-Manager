from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from datetime import datetime

# Initialisation de FastAPI
app = FastAPI()

# Création du moteur SQLAlchemy pour SQLite
DATABASE_URL = "sqlite:///./SaveBdd.sqlite"
engine = create_engine(DATABASE_URL, echo=True)

# Déclaration de la base pour SQLAlchemy ORM
Base = declarative_base()

# Session SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modèles de la base de données
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)

class Game(Base):
    __tablename__ = "games"
    game_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    steam_id = Column(String, unique=True, nullable=False)

class UserGame(Base):
    __tablename__ = "user_games"
    user_game_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    game_id = Column(Integer, ForeignKey('games.game_id'), nullable=False)

class Save(Base):
    __tablename__ = "saves"
    save_id = Column(Integer, primary_key=True, autoincrement=True)
    user_game_id = Column(Integer, ForeignKey('user_games.user_game_id'), nullable=False)
    save_path = Column(Text, nullable=False)
    save_date = Column(DateTime, default=datetime.utcnow)

# Crée les tables dans la base de données si elles n'existent pas
Base.metadata.create_all(bind=engine)

# Fonction pour récupérer la session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Servir les fichiers statiques (images, CSS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Utilisation de Jinja2 pour servir des templates HTML
templates = Jinja2Templates(directory="templates")

# Page d'accueil
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# API Endpoints

# 1. Ajout d'un utilisateur
@app.post("/addUser/{username}")
async def add_user(username: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="L'utilisateur existe déjà.")

    new_user = User(username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"user_id": new_user.user_id, "username": new_user.username}

# 2. Mise à jour d'un utilisateur
@app.put("/updateUser/{user_id}")
async def update_user(user_id: int, username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    user.username = username
    db.commit()
    db.refresh(user)

    return {"user_id": user.user_id, "updated_username": user.username}

# 3. Ajout d'un jeu
@app.post("/addGame/{title}/{steam_id}")
async def add_game(title: str, steam_id: str, db: Session = Depends(get_db)):
    existing_game = db.query(Game).filter(Game.steam_id == steam_id).first()
    if existing_game:
        raise HTTPException(status_code=400, detail="Le jeu existe déjà.")

    new_game = Game(title=title, steam_id=steam_id)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return {"game_id": new_game.game_id, "title": new_game.title, "steam_id": new_game.steam_id}

# 4. Mise à jour d'un jeu
@app.put("/updateGame/{game_id}")
async def update_game(game_id: int, title: str, steam_id: str, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.game_id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Jeu non trouvé.")

    game.title = title
    game.steam_id = steam_id
    db.commit()
    db.refresh(game)

    return {"game_id": game.game_id, "updated_title": game.title, "updated_steam_id": game.steam_id}

# 5. Associer un jeu à un utilisateur
@app.post("/addUserGame/{user_id}/{game_id}")
async def add_user_game(user_id: int, game_id: int, db: Session = Depends(get_db)):
    existing_user_game = db.query(UserGame).filter(UserGame.user_id == user_id, UserGame.game_id == game_id).first()
    if existing_user_game:
        raise HTTPException(status_code=400, detail="L'utilisateur possède déjà ce jeu.")

    new_user_game = UserGame(user_id=user_id, game_id=game_id)
    db.add(new_user_game)
    db.commit()
    db.refresh(new_user_game)

    return {"user_game_id": new_user_game.user_game_id, "user_id": new_user_game.user_id, "game_id": new_user_game.game_id}

# 6. Ajout d'une sauvegarde (save)
@app.post("/addSave/{user_game_id}")
async def add_save(user_game_id: int, save_path: str, db: Session = Depends(get_db)):
    existing_save = db.query(Save).filter(Save.user_game_id == user_game_id, Save.save_path == save_path).first()
    if existing_save:
        raise HTTPException(status_code=400, detail="La sauvegarde existe déjà.")

    new_save = Save(user_game_id=user_game_id, save_path=save_path)
    db.add(new_save)
    db.commit()
    db.refresh(new_save)

    return {
        "save_id": new_save.save_id,
        "user_game_id": new_save.user_game_id,
        "save_path": new_save.save_path,
        "save_date": new_save.save_date
    }

# 7. Récupérer tous les utilisateurs
@app.get("/users/")
async def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

# 8. Récupérer un utilisateur par ID
@app.get("/users/{user_id}")
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    return user

# 9. Récupérer tous les jeux
@app.get("/games/")
async def get_all_games(db: Session = Depends(get_db)):
    games = db.query(Game).all()
    return games

# 10. Récupérer un jeu par ID
@app.get("/games/{game_id}")
async def get_game_by_id(game_id: int, db: Session = Depends(get_db)):
    game = db.query(Game).filter(Game.game_id == game_id).first()
    if not game:
        raise HTTPException(status_code=404, detail="Jeu non trouvé.")
    return game

# 11. Récupérer toutes les associations utilisateur-jeu
@app.get("/userGames/")
async def get_all_user_games(db: Session = Depends(get_db)):
    user_games = db.query(UserGame).all()
    return user_games

# 12. Récupérer une association utilisateur-jeu par ID
@app.get("/userGames/{user_game_id}")
async def get_user_game_by_id(user_game_id: int, db: Session = Depends(get_db)):
    user_game = db.query(UserGame).filter(UserGame.user_game_id == user_game_id).first()
    if not user_game:
        raise HTTPException(status_code=404, detail="Association utilisateur-jeu non trouvée.")
    return user_game

# 13. Récupérer toutes les sauvegardes
@app.get("/saves/")
async def get_all_saves(db: Session = Depends(get_db)):
    saves = db.query(Save).all()
    return saves

# 14. Récupérer une sauvegarde par ID
@app.get("/saves/{save_id}")
async def get_save_by_id(save_id: int, db: Session = Depends(get_db)):
    save = db.query(Save).filter(Save.save_id == save_id).first()
    if not save:
        raise HTTPException(status_code=404, detail="Sauvegarde non trouvée.")
    return save
