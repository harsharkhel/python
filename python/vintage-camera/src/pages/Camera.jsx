/**
 * Camera — Full-screen camera experience page.
 * Composes all camera-related components and manages
 * top-level coordination between camera, hand tracking,
 * gesture control, and UI state.
 */
import { useState, useRef, useCallback, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Loader2 } from 'lucide-react';

import CameraView from '../components/CameraView';
import FilterSelector from '../components/FilterSelector';
import GestureIndicator from '../components/GestureIndicator';
import IntensityIndicator from '../components/IntensityIndicator';
import CameraControls from '../components/CameraControls';
import CaptureButton from '../components/CaptureButton';
import SettingsPanel from '../components/SettingsPanel';
import GestureTutorial from '../components/GestureTutorial';

import useCamera from '../hooks/useCamera';
import useHandTracking from '../hooks/useHandTracking';
import useGestureControl from '../hooks/useGestureControl';
import { filters } from '../filters/filterEngine';

// localStorage key for settings
const SETTINGS_KEY = 'vintage-settings';
const TUTORIAL_KEY = 'vintage-tutorial-done';

function loadSettings() {
  try {
    const saved = localStorage.getItem(SETTINGS_KEY);
    if (saved) return JSON.parse(saved);
  } catch (e) {
    // ignore
  }
  return {
    mirrorSelfie: true,
    handTracking: true,
    gestureControl: true,
    showTracking: false,
  };
}

function saveSettings(settings) {
  try {
    localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
  } catch (e) {
    // ignore
  }
}

export default function CameraPage({ onClose }) {
  const cameraViewRef = useRef(null);

  // Settings state
  const [settings, setSettings] = useState(loadSettings);
  const [showSettings, setShowSettings] = useState(false);

  // Filter state (React state for UI updates)
  const [activeFilterIndex, setActiveFilterIndex] = useState(0);
  const [intensity, setIntensity] = useState(1.0);

  // Gesture feedback state
  const [showGestureIndicator, setShowGestureIndicator] = useState(false);
  const [gestureFilterName, setGestureFilterName] = useState('');
  const [intensityActive, setIntensityActive] = useState(false);

  // Tutorial
  const [showTutorial, setShowTutorial] = useState(() => {
    try {
      return !localStorage.getItem(TUTORIAL_KEY);
    } catch {
      return true;
    }
  });

  // Camera hook
  const camera = useCamera();

  // Hand tracking hook
  const handTracking = useHandTracking(
    camera.videoRef,
    camera.isActive,
    settings.handTracking
  );

  // Gesture control hook
  const gestureControl = useGestureControl(
    settings.gestureControl && settings.handTracking
  );

  // Throttle UI updates from gesture results
  const lastUIUpdateRef = useRef(0);
  const gestureIndicatorTimerRef = useRef(null);

  // Start camera on mount
  useEffect(() => {
    camera.startCamera();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Sync gesture control callbacks
  useEffect(() => {
    gestureControl.setOnFilterChange((newIndex) => {
      setActiveFilterIndex(newIndex);
      setGestureFilterName(filters[newIndex]?.name || '');
      setShowGestureIndicator(true);

      if (gestureIndicatorTimerRef.current) {
        clearTimeout(gestureIndicatorTimerRef.current);
      }
      gestureIndicatorTimerRef.current = setTimeout(() => {
        setShowGestureIndicator(false);
      }, 1200);

      // Dismiss tutorial on first gesture
      if (showTutorial) {
        setShowTutorial(false);
        try {
          localStorage.setItem(TUTORIAL_KEY, 'true');
        } catch (e) {
          // ignore
        }
      }
    });

    gestureControl.setOnIntensityChange((rounded) => {
      const now = performance.now();
      if (now - lastUIUpdateRef.current > 100) {
        setIntensity(rounded / 100);
        setIntensityActive(true);
        lastUIUpdateRef.current = now;
      }
    });
  }, [gestureControl, showTutorial]);

  // Handle gesture results from render loop (throttled)
  const handleGestureResult = useCallback((result) => {
    if (!result) return;

    // Update filter index if gesture changed it
    if (result.gestureTriggered) {
      setActiveFilterIndex(result.filterIndex);
    }

    // Track intensity activity — only show indicator when deliberately controlling
    if (result.intensityControlActive) {
      setIntensityActive(true);
    } else {
      setIntensityActive(false);
    }
  }, []);

  // Manual filter selection
  const handleFilterSelect = useCallback(
    (index) => {
      setActiveFilterIndex(index);
      gestureControl.setFilterIndex(index);
    },
    [gestureControl]
  );

  // Manual intensity change
  const handleIntensityChange = useCallback(
    (value) => {
      setIntensity(value);
      gestureControl.setIntensity(value);
    },
    [gestureControl]
  );

  // Settings
  const handleSettingChange = useCallback(
    (key, value) => {
      if (key === 'resetTutorial') {
        setShowTutorial(true);
        try {
          localStorage.removeItem(TUTORIAL_KEY);
        } catch (e) {
          // ignore
        }
        return;
      }

      setSettings((prev) => {
        const next = { ...prev, [key]: value };
        saveSettings(next);
        return next;
      });
    },
    []
  );

  const handleDismissTutorial = useCallback(() => {
    setShowTutorial(false);
    try {
      localStorage.setItem(TUTORIAL_KEY, 'true');
    } catch (e) {
      // ignore
    }
  }, []);

  // Error state
  if (camera.error && !camera.isActive) {
    return (
      <div className="camera-error-page">
        <div className="camera-error-content">
          <h2 className="camera-error-title">Camera Unavailable</h2>
          <p className="camera-error-message">{camera.error}</p>
          <div className="camera-error-actions">
            <button onClick={camera.retryCamera} className="camera-error-retry">
              Try Again
            </button>
            <button onClick={onClose} className="camera-error-back">
              Go Back
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <motion.div
      className="camera-page"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Loading overlay */}
      {(camera.isLoading || (settings.handTracking && handTracking.isLoading)) && (
        <div className="camera-loading">
          <Loader2 size={32} className="camera-loading-spinner" />
          <span className="camera-loading-text">
            {camera.isLoading
              ? 'Starting camera...'
              : 'Loading hand tracking...'}
          </span>
        </div>
      )}

      {/* Camera View */}
      <CameraView
        ref={cameraViewRef}
        videoRef={camera.videoRef}
        isActive={camera.isActive}
        isFrontCamera={camera.isFrontCamera}
        mirrorSelfie={settings.mirrorSelfie}
        filterIndex={activeFilterIndex}
        intensity={intensity}
        handTrackingDetect={
          settings.handTracking && handTracking.isReady
            ? handTracking.detect
            : null
        }
        gestureProcess={
          settings.gestureControl && settings.handTracking
            ? gestureControl.processGesture
            : null
        }
        showHandTracking={settings.showTracking}
        onGestureResult={handleGestureResult}
      />

      {/* Header controls */}
      <CameraControls
        onSwitchCamera={camera.switchCamera}
        onToggleSettings={() => setShowSettings(!showSettings)}
        onClose={onClose}
        isFrontCamera={camera.isFrontCamera}
        showSettings={showSettings}
      />

      {/* Brand watermark */}
      <div className="camera-brand">VINTAGE</div>

      {/* Hand tracking status */}
      {settings.handTracking && handTracking.isReady && (
        <div className="tracking-status">
          <div className="tracking-dot" />
        </div>
      )}

      {handTracking.error && (
        <div className="tracking-error">
          {handTracking.error}
        </div>
      )}

      {/* Gesture feedback */}
      <GestureIndicator
        filterName={gestureFilterName}
        show={showGestureIndicator}
      />

      {/* Intensity indicator */}
      <IntensityIndicator
        intensity={intensity}
        isActive={intensityActive && activeFilterIndex > 0}
        filterName={filters[activeFilterIndex]?.name}
      />

      {/* Filter selector */}
      <FilterSelector
        activeIndex={activeFilterIndex}
        onSelect={handleFilterSelect}
      />

      {/* Capture button */}
      <CaptureButton
        cameraViewRef={cameraViewRef}
        filterName={filters[activeFilterIndex]?.name}
      />

      {/* Settings panel */}
      <SettingsPanel
        show={showSettings}
        onClose={() => setShowSettings(false)}
        settings={settings}
        onSettingChange={handleSettingChange}
        intensity={intensity}
        onIntensityChange={handleIntensityChange}
        filterName={filters[activeFilterIndex]?.name}
      />

      {/* Tutorial */}
      <GestureTutorial
        show={showTutorial && camera.isActive && !camera.isLoading}
        onDismiss={handleDismissTutorial}
      />
    </motion.div>
  );
}
