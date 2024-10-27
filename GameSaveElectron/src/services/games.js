import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Récupérer tous les jeux
export const getGames = async () => {
  const response = await axios.get(`${API_BASE_URL}/games/`);
  return response.data;
};

// Ajouter un jeu
export const addGame = async (title, AppID) => {
  const response = await axios.post(`${API_BASE_URL}/addGame/${title}/${AppID}`);
  return response.data;
};

// Ajouter une sauvegarde
export const addSave = async (game_id, save_path) => {
  const response = await axios.post(`${API_BASE_URL}/addSave/${game_id}`, { save_path });
  return response.data;
};

// Récupérer les sauvegardes pour un jeu
export const getSavesForGame = async (game_id) => {
  const response = await axios.get(`${API_BASE_URL}/saves/${game_id}`);
  return response.data;
};

// Copier une sauvegarde en local
export const copySaveToLocal = async (AppID, savePath) => {
  const response = await axios.post(`${API_BASE_URL}/copySaveToLocal`, { AppID, savePath });
  return response.data;
};

// Restaurer une sauvegarde à partir du local
export const restoreSaveFromLocal = async (AppID, savePath) => {
  const response = await axios.post(`${API_BASE_URL}/restoreSaveFromLocal`, { AppID, savePath });
  return response.data;
};

// Supprimer une sauvegarde
export const deleteSave = async (save_id) => {
  const response = await axios.delete(`${API_BASE_URL}/saves/${save_id}`);
  return response.data;
};

export const loadSave = async (save_id) => {
  const response = await axios.post(`${API_BASE_URL}/loadSave/${save_id}`);
  return response.data;
};
