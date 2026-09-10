/**
 * Gesture math utilities for hand tracking calculations.
 * All distance calculations use normalized coordinates (0-1).
 */

/**
 * Calculate 2D Euclidean distance between two landmarks.
 * @param {{ x: number, y: number }} p1
 * @param {{ x: number, y: number }} p2
 * @returns {number}
 */
export function euclideanDistance(p1, p2) {
  const dx = p1.x - p2.x;
  const dy = p1.y - p2.y;
  return Math.sqrt(dx * dx + dy * dy);
}

/**
 * Calculate palm size as the distance from wrist (landmark 0)
 * to middle finger MCP (landmark 9).
 * This serves as a normalization reference so gestures work
 * regardless of hand distance from camera.
 * @param {Array} landmarks - MediaPipe hand landmarks
 * @returns {number}
 */
export function calculatePalmSize(landmarks) {
  const wrist = landmarks[0];
  const middleMCP = landmarks[9];
  return euclideanDistance(wrist, middleMCP);
}

/**
 * Get the normalized pinch distance between thumb tip (4)
 * and index finger tip (8), divided by palm size.
 * @param {Array} landmarks - MediaPipe hand landmarks
 * @returns {number} Normalized distance (typically 0.1 - 0.8)
 */
export function normalizedPinchDistance(landmarks) {
  const thumbTip = landmarks[4];
  const indexTip = landmarks[8];
  const palmSize = calculatePalmSize(landmarks);

  if (palmSize < 0.001) return 1; // Avoid division by zero

  return euclideanDistance(thumbTip, indexTip) / palmSize;
}

/**
 * Map a normalized distance to an intensity value (0-1).
 * @param {number} normalizedDist - Normalized pinch distance
 * @param {number} minDist - Distance that maps to 0 (pinched)
 * @param {number} maxDist - Distance that maps to 1 (open)
 * @returns {number} Clamped intensity 0-1
 */
export function mapToIntensity(normalizedDist, minDist = 0.15, maxDist = 0.65) {
  const clamped = Math.max(minDist, Math.min(maxDist, normalizedDist));
  return (clamped - minDist) / (maxDist - minDist);
}

/**
 * Linear interpolation for smooth value transitions.
 * @param {number} current - Current value
 * @param {number} target - Target value
 * @param {number} factor - Smoothing factor (0-1, lower = smoother)
 * @returns {number}
 */
export function lerp(current, target, factor = 0.2) {
  return current + (target - current) * factor;
}

/**
 * Detect if a hand is pinching based on normalized distance
 * with hysteresis support.
 * @param {Array} landmarks - MediaPipe hand landmarks
 * @param {number} threshold - Distance below which = pinching
 * @returns {boolean}
 */
export function isPinching(landmarks, threshold = 0.30) {
  return normalizedPinchDistance(landmarks) < threshold;
}

/**
 * Detect if a hand is open (not pinching) with hysteresis.
 * Uses a higher threshold than pinch to prevent jitter.
 * @param {Array} landmarks
 * @param {number} threshold - Distance above which = open
 * @returns {boolean}
 */
export function isOpen(landmarks, threshold = 0.45) {
  return normalizedPinchDistance(landmarks) > threshold;
}
