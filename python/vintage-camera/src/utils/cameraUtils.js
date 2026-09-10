/**
 * Camera utility functions for device enumeration and constraints.
 */

/**
 * Check if the current device is mobile.
 * @returns {boolean}
 */
export function isMobileDevice() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
}

/**
 * Get available video input devices.
 * @returns {Promise<MediaDeviceInfo[]>}
 */
export async function getAvailableCameras() {
  try {
    const devices = await navigator.mediaDevices.enumerateDevices();
    return devices.filter((device) => device.kind === 'videoinput');
  } catch (err) {
    console.warn('Could not enumerate devices:', err);
    return [];
  }
}

/**
 * Build camera constraints for getUserMedia.
 * Prefers rear camera on mobile, front camera on desktop.
 * @param {'user'|'environment'} facingMode
 * @returns {MediaStreamConstraints}
 */
export function getPreferredConstraints(facingMode = 'user') {
  return {
    video: {
      facingMode: { ideal: facingMode },
      width: { ideal: 1280 },
      height: { ideal: 720 },
      frameRate: { ideal: 30 },
    },
    audio: false,
  };
}

/**
 * Stop all tracks on a media stream.
 * @param {MediaStream|null} stream
 */
export function stopStream(stream) {
  if (stream) {
    stream.getTracks().forEach((track) => track.stop());
  }
}

/**
 * Check if the browser supports getUserMedia.
 * @returns {boolean}
 */
export function isGetUserMediaSupported() {
  return !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia);
}
