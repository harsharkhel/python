/**
 * SettingsPanel — Slide-in settings drawer.
 * Controls camera, mirror, hand tracking, gesture, and intensity settings.
 * Persists user preferences to localStorage.
 */
import { X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function SettingsPanel({
  show,
  onClose,
  settings,
  onSettingChange,
  intensity,
  onIntensityChange,
  filterName,
}) {
  const handleToggle = (key) => {
    onSettingChange(key, !settings[key]);
  };

  return (
    <AnimatePresence>
      {show && (
        <>
          {/* Backdrop */}
          <motion.div
            className="settings-backdrop"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />

          {/* Panel */}
          <motion.div
            className="settings-panel"
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          >
            <div className="settings-header">
              <h2 className="settings-title">Settings</h2>
              <button
                onClick={onClose}
                className="settings-close-btn"
                aria-label="Close settings"
              >
                <X size={20} />
              </button>
            </div>

            <div className="settings-body">
              {/* Mirror Selfie */}
              <div className="settings-item">
                <div className="settings-item-info">
                  <span className="settings-item-label">Mirror Selfie</span>
                  <span className="settings-item-desc">
                    Mirror the captured photo for selfie mode
                  </span>
                </div>
                <button
                  className={`settings-toggle ${settings.mirrorSelfie ? 'settings-toggle-on' : ''}`}
                  onClick={() => handleToggle('mirrorSelfie')}
                  role="switch"
                  aria-checked={settings.mirrorSelfie}
                  aria-label="Toggle mirror selfie"
                >
                  <span className="settings-toggle-thumb" />
                </button>
              </div>

              {/* Hand Tracking */}
              <div className="settings-item">
                <div className="settings-item-info">
                  <span className="settings-item-label">Hand Tracking</span>
                  <span className="settings-item-desc">
                    Enable real-time hand detection
                  </span>
                </div>
                <button
                  className={`settings-toggle ${settings.handTracking ? 'settings-toggle-on' : ''}`}
                  onClick={() => handleToggle('handTracking')}
                  role="switch"
                  aria-checked={settings.handTracking}
                  aria-label="Toggle hand tracking"
                >
                  <span className="settings-toggle-thumb" />
                </button>
              </div>

              {/* Gesture Control */}
              <div className="settings-item">
                <div className="settings-item-info">
                  <span className="settings-item-label">Gesture Control</span>
                  <span className="settings-item-desc">
                    Control filters using hand gestures
                  </span>
                </div>
                <button
                  className={`settings-toggle ${settings.gestureControl ? 'settings-toggle-on' : ''}`}
                  onClick={() => handleToggle('gestureControl')}
                  role="switch"
                  aria-checked={settings.gestureControl}
                  aria-label="Toggle gesture control"
                >
                  <span className="settings-toggle-thumb" />
                </button>
              </div>

              {/* Show Hand Tracking Visualization */}
              <div className="settings-item">
                <div className="settings-item-info">
                  <span className="settings-item-label">Show Tracking</span>
                  <span className="settings-item-desc">
                    Display fingertip indicators on screen
                  </span>
                </div>
                <button
                  className={`settings-toggle ${settings.showTracking ? 'settings-toggle-on' : ''}`}
                  onClick={() => handleToggle('showTracking')}
                  role="switch"
                  aria-checked={settings.showTracking}
                  aria-label="Toggle tracking visualization"
                >
                  <span className="settings-toggle-thumb" />
                </button>
              </div>

              {/* Intensity Slider */}
              <div className="settings-item settings-item-column">
                <div className="settings-item-info">
                  <span className="settings-item-label">Filter Intensity</span>
                  <span className="settings-item-value">
                    {Math.round(intensity * 100)}%
                  </span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={Math.round(intensity * 100)}
                  onChange={(e) => onIntensityChange(parseInt(e.target.value) / 100)}
                  className="settings-slider"
                  aria-label="Filter intensity"
                />
              </div>

              {/* Reset Tutorial */}
              <div className="settings-item">
                <div className="settings-item-info">
                  <span className="settings-item-label">Tutorial</span>
                  <span className="settings-item-desc">
                    Show gesture tutorial again
                  </span>
                </div>
                <button
                  className="settings-reset-btn"
                  onClick={() => onSettingChange('resetTutorial', true)}
                >
                  Reset
                </button>
              </div>
            </div>

            {/* Privacy note */}
            <div className="settings-footer">
              <p className="settings-privacy">
                🔒 Your camera stays on your device.
                No images are uploaded or stored.
              </p>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
