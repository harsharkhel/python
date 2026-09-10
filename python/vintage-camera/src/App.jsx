/**
 * App — Root component for VINTAGE camera application.
 * Simple state-based routing between Home and Camera screens.
 */
import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import Home from './pages/Home';
import CameraPage from './pages/Camera';

export default function App() {
  const [screen, setScreen] = useState('home');

  return (
    <div className="app">
      <AnimatePresence mode="wait">
        {screen === 'home' ? (
          <Home
            key="home"
            onOpenCamera={() => setScreen('camera')}
          />
        ) : (
          <CameraPage
            key="camera"
            onClose={() => setScreen('home')}
          />
        )}
      </AnimatePresence>
    </div>
  );
}
