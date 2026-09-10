/**
 * CameraControls — Camera switch and settings buttons.
 * Minimal overlay controls positioned in the camera header area.
 */
import { SwitchCamera, Settings, X } from 'lucide-react';

export default function CameraControls({
  onSwitchCamera,
  onToggleSettings,
  onClose,
  isFrontCamera,
  showSettings,
}) {
  return (
    <div className="camera-controls">
      <button
        onClick={onClose}
        className="camera-control-btn"
        aria-label="Close camera"
      >
        <X size={20} />
      </button>

      <div className="camera-controls-right">
        <button
          onClick={onSwitchCamera}
          className="camera-control-btn"
          aria-label={`Switch to ${isFrontCamera ? 'rear' : 'front'} camera`}
        >
          <SwitchCamera size={20} />
        </button>

        <button
          onClick={onToggleSettings}
          className="camera-control-btn"
          aria-label={showSettings ? 'Close settings' : 'Open settings'}
        >
          <Settings size={20} />
        </button>
      </div>
    </div>
  );
}
