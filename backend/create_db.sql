-- schema.sql
-- Table des jeux
CREATE TABLE IF NOT EXISTS games (
    game_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    AppID TEXT NOT NULL UNIQUE  -- AppID unique pour chaque jeu
);
-- Table des sauvegardes
CREATE TABLE IF NOT EXISTS saves (
    save_id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id INTEGER NOT NULL,  -- Référence vers game_id dans la table games
    save_path TEXT NOT NULL,   -- Chemin original de la sauvegarde
    backup_path TEXT NOT NULL, -- Chemin du répertoire de backup
    save_date DATETIME DEFAULT CURRENT_TIMESTAMP,  -- Date et heure de la sauvegarde
    FOREIGN KEY (game_id) REFERENCES games(game_id) ON DELETE CASCADE
);
