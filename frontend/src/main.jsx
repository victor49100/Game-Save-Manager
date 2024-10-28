import React from 'react';
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './services/fontAwesome.js';
import Home from './components/Home.jsx';
import './index.css';

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
