// Home.jsx

import React, {useState, useEffect} from 'react';
import {
    getGames,
    addGame,
    deleteGame,
    getSavesForGame,
    deleteSave,
    copySaveToLocal,
    restoreSaveFromLocal
} from '../services/games.js';
import '../styles/Home.css';
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';

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
        } else {
            setSaves([]);
        }
    };

    const loadSaves = async (gameId) => {
        const fetchedSaves = await getSavesForGame(gameId);
        setSaves(fetchedSaves);
    };

    const handleAddSave = async () => {
        if (savePath && selectedGame) {
            const saveName = prompt("Entrez le nom de la save (facultatif) :");
            await copySaveToLocal(selectedGame.AppID, savePath , saveName); // Copier la sauvegarde en local
            setSavePath('');
            loadSaves(selectedGame.game_id);
        }
    };

    const handleRestoreSave = async (save) => {
        if (window.confirm('Êtes-vous sûr de vouloir restaurer cette sauvegarde ?')) {
            await restoreSaveFromLocal(selectedGame.AppID, save.backup_path); // Restaurer la sauvegarde
            alert('Sauvegarde restaurée avec succès.');
        }
    };

    const handleDeleteSave = async (saveId) => {
        if (window.confirm('Êtes-vous sûr de vouloir supprimer cette sauvegarde ?')) {
            await deleteSave(saveId);
            loadSaves(selectedGame.game_id);
        }
    };

    const handleAddGame = async () => {
        // Ajout d'un nouveau jeu
        const title = prompt('Entrez le titre du jeu :');
        const AppID = prompt("Entrez l'AppID du jeu :");
        if (title && AppID) {
            await addGame(title, AppID);
            loadGames();
        }
    };

    const handleDeleteGame = async (gameId) => {
        if (window.confirm('Êtes-vous sûr de vouloir supprimer ce jeu ? Toutes les sauvegardes associées seront également supprimées.')) {
            await deleteGame(gameId);
            setSelectedGame(null);
            setSaves([]);
            loadGames();
        }
    };

    return (
        <div className="container">
            {/* Logo du site */}
            <header className="site-header">
                <h1><FontAwesomeIcon icon={['fas', 'gamepad']}/> Game Save Manager</h1>
            </header>

            {/* Ajouter un jeu */}
            <div className="add-game-section">
                <button onClick={handleAddGame}><FontAwesomeIcon icon={['fas', 'plus']}/> Ajouter un jeu</button>
            </div>

            {/* Liste déroulante pour sélectionner un jeu */}
            <div className="game-select-section">
                <label htmlFor="gameSelect">Sélectionnez un jeu :</label>
                <select id="gameSelect" onChange={handleSelectGame} value={selectedGame ? selectedGame.game_id : ''}>
                    <option value="">-- Sélectionnez un jeu --</option>
                    {games.map((game) => (
                        <option key={game.game_id} value={game.game_id}>
                            {game.title}
                        </option>
                    ))}
                </select>
                {selectedGame && (
                    <button className="delete-game-button" onClick={() => handleDeleteGame(selectedGame.game_id)}>
                        <FontAwesomeIcon icon={['fas', 'trash']}/> Supprimer le jeu
                    </button>
                )}
            </div>

            {/* Affichage des informations du jeu sélectionné */}
            {selectedGame && (
                <div className="game-info">
                    <h2>{selectedGame.title}</h2>
                    <p>AppID : {selectedGame.AppID}</p>
                </div>
            )}

            {/* Ajout d'une sauvegarde */}
            {selectedGame && (
                <div className="add-save-section">
                    <input
                        type="text"
                        placeholder="Chemin de la sauvegarde"
                        value={savePath}
                        onChange={(e) => setSavePath(e.target.value)}
                    />
                    <button onClick={handleAddSave}>
                        <FontAwesomeIcon icon={['fas', 'save']}/> Ajouter une sauvegarde
                    </button>
                </div>
            )}

            {/* Tableau des sauvegardes */}
            {saves.length > 0 && (
                <div className="saves-list">
                    <h3>Sauvegardes</h3>
                    <table>
                        <thead>
                        {/*chapeaux du tableau*/}
                        <tr>
                            <th>Numero de la save</th>
                            <th>Nom de la save</th>
                            <th>Chemin de la save</th>
                            <th>Date de la save</th>
                            <th>Actions</th>
                        </tr>
                        </thead>
                        <tbody>
                        {saves.slice().reverse().map((save, index) => (
                            <tr key={save.save_id}>
                                <td>{index + 1}</td>
                                <td>{save.save_name}</td>
                                <td>{save.save_path}</td>
                                <td>{new Date(save.save_date).toLocaleString('fr-FR', {hour12: false})}</td>
                                <td>
                                    <button className="restore-save-button" onClick={() => handleRestoreSave(save)}>
                                        <FontAwesomeIcon icon={['fas', 'redo']}/> Restaurer
                                    </button>
                                    <button className="delete-save-button"
                                            onClick={() => handleDeleteSave(save.save_id)}>
                                        <FontAwesomeIcon icon={['fas', 'trash']}/> Supprimer
                                    </button>
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
