import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import Home from './pages/Home'; // Assurez-vous que le chemin est correct
import './main.css'; // Si vous avez un fichier CSS global

// Point d'entrée pour monter l'application React dans l'élément root
const rootElement = document.getElementById('root');
if (rootElement) {
  createRoot(rootElement).render(
    <StrictMode>
      <Home />
    </StrictMode>
  );
} else {
  console.error('Root element not found');
}
