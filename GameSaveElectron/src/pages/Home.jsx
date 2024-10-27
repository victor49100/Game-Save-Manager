import React, { useState, useEffect } from 'react';
import { getGames, addGame, addSave, getSavesForGame, deleteSave, loadSave, copySaveToLocal, restoreSaveFromLocal } from '../services/games.js';
import './Home.css';

function Home() {
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [savePath, setSavePath] = useState('');
  const [saves, setSaves] = useState([]);

  useEffect(() => {
    loadGames();
  }, []);

  const loadGames = async () => {
    const fetchedGames = await getGames();
    setGames(fetchedGames);
  };

  const handleSelectGame = async (event) => {
    const gameId = event.target.value;
    const game = games.find((g) => g.game_id === parseInt(gameId));
    setSelectedGame(game);
    if (gameId) {
      loadSaves(gameId);
    }
  };

  const loadSaves = async (gameId) => {
    const fetchedSaves = await getSavesForGame(gameId);
    setSaves(fetchedSaves);
  };

  const handleAddSave = async () => {
    if (savePath && selectedGame) {
      await addSave(selectedGame.game_id, savePath);
      setSavePath('');
      loadSaves(selectedGame.game_id);
      await copySaveToLocal(selectedGame.AppID, savePath); // Copier la sauvegarde en local
    }
  };

  const handleRestoreSave = async (saveId, savePath) => {
    await restoreSaveFromLocal(selectedGame.AppID, savePath); // Remplacer la sauvegarde par celle stockée en local
  };

  const handleDeleteSave = async (saveId) => {
    await deleteSave(saveId);
    loadSaves(selectedGame.game_id);
  };

  const handleAddGame = async () => {
    // Ajout d'un nouveau jeu
    const title = prompt('Enter game title:');
    const AppID = prompt('Enter AppID:');
    if (title && AppID) {
      await addGame(title, AppID);
      loadGames();
    }
  };

  return (
    <div className="container">
      <h1>Game Saves</h1>

      {/* Ajouter un jeu */}
      <div className="add-game-section">
        <button onClick={handleAddGame}>Add Game</button>
      </div>

      {/* Liste déroulante pour sélectionner un jeu */}
      <div className="game-select-section">
        <label htmlFor="gameSelect">Select Game:</label>
        <select id="gameSelect" onChange={handleSelectGame}>
          <option value="">-- Select a Game --</option>
          {games.map((game) => (
            <option key={game.game_id} value={game.game_id}>
              {game.title}
            </option>
          ))}
        </select>
      </div>

      {/* Affichage des informations du jeu sélectionné */}
      {selectedGame && (
        <div className="game-info">
          <h2>{selectedGame.title}</h2>
          <p>AppID: {selectedGame.AppID}</p>
        </div>
      )}

      {/* Ajout d'une sauvegarde */}
      {selectedGame && (
        <div className="add-save-section">
          <input
            type="text"
            placeholder="Save Path"
            value={savePath}
            onChange={(e) => setSavePath(e.target.value)}
          />
          <button onClick={handleAddSave}>Add Save</button>
        </div>
      )}

      {/* Tableau des sauvegardes */}
      {saves.length > 0 && (
        <div className="saves-list">
          <h3>Saves</h3>
          <table>
            <thead>
              <tr>
                <th>Save Path</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {saves.map((save) => (
                <tr key={save.save_id}>
                  <td>{save.save_path}</td>
                  <td>{new Date(save.save_date).toLocaleString()}</td>
                  <td>
                    <button onClick={() => handleRestoreSave(save.save_id, save.save_path)}>Restore</button>
                    <button onClick={() => handleDeleteSave(save.save_id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Home;
