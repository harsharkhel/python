/**
 * useGestureControl — Gesture state machine for filter control.
 *
 * ONE HAND: Thumb-index distance → filter intensity (0-100%)
 *   BUT only when user deliberately enters "intensity mode" by pinching first.
 *   Simply having a hand visible does NOT override the filter intensity.
 *
 * TWO HANDS: Pinch-open gesture → switch to next filter
 *
 * State machine for two-hand gesture:
 *   IDLE → BOTH_PINCHED → BOTH_OPEN → TRIGGER → IDLE (with cooldown)
 *
 * State machine for one-hand intensity:
 *   INTENSITY_IDLE → (pinch detected) → INTENSITY_ENGAGED → (tracking distance)
 *   → (hand disappears or stays fully open for 1.5s) → INTENSITY_IDLE
 *
 * Uses hysteresis thresholds to prevent jitter:
 *   PINCH_THRESHOLD = 0.30 (below this = pinching)
 *   OPEN_THRESHOLD  = 0.45 (above this = open)
 */
import { useRef, useCallback } from 'react';
import {
  normalizedPinchDistance,
  mapToIntensity,
  lerp,
  isPinching,
  isOpen,
} from '../utils/gestureMath';
import { getNextFilterIndex } from '../filters/filterEngine';

// Gesture state constants
const GESTURE_IDLE = 'IDLE';
const GESTURE_BOTH_PINCHED = 'BOTH_PINCHED';
const GESTURE_COOLDOWN = 'COOLDOWN';

// One-hand intensity states
const INTENSITY_IDLE = 'INTENSITY_IDLE';
const INTENSITY_ENGAGED = 'INTENSITY_ENGAGED';

// Cooldown duration after successful filter change
const COOLDOWN_MS = 800;

// How long fingers must stay fully open before disengaging intensity mode
const INTENSITY_DISENGAGE_MS = 1500;

export default function useGestureControl(enabled = true) {
  // All state is stored in refs to avoid React re-renders during animation loop
  const gestureStateRef = useRef(GESTURE_IDLE);
  const smoothedIntensityRef = useRef(1.0);
  const filterIndexRef = useRef(0);
  const cooldownTimerRef = useRef(0);
  const lastGestureTimeRef = useRef(0);
  const isGestureActiveRef = useRef(false);
  const gestureTriggeredRef = useRef(false);
  const handsCountRef = useRef(0);

  // One-hand intensity state machine
  const intensityStateRef = useRef(INTENSITY_IDLE);
  const intensityDisengageTimerRef = useRef(0);
  const isIntensityControlActiveRef = useRef(false);

  // Callbacks for UI updates (called sparingly)
  const onFilterChangeRef = useRef(null);
  const onIntensityChangeRef = useRef(null);
  const onGestureTriggeredRef = useRef(null);

  /**
   * Set callback for filter changes.
   */
  const setOnFilterChange = useCallback((cb) => {
    onFilterChangeRef.current = cb;
  }, []);

  /**
   * Set callback for intensity changes.
   */
  const setOnIntensityChange = useCallback((cb) => {
    onIntensityChangeRef.current = cb;
  }, []);

  /**
   * Set callback for gesture triggered animation.
   */
  const setOnGestureTriggered = useCallback((cb) => {
    onGestureTriggeredRef.current = cb;
  }, []);

  /**
   * Set filter index externally (e.g., from manual UI selection).
   */
  const setFilterIndex = useCallback((index) => {
    filterIndexRef.current = index;
  }, []);

  /**
   * Set intensity externally (e.g., from manual slider).
   */
  const setIntensity = useCallback((value) => {
    smoothedIntensityRef.current = value;
  }, []);

  /**
   * Process hand tracking results every frame.
   * Called from the main animation loop.
   *
   * @param {object} results - MediaPipe HandLandmarker results
   * @returns {{ intensity: number, filterIndex: number, gestureState: string, handsCount: number, gestureTriggered: boolean, intensityControlActive: boolean }}
   */
  const processGesture = useCallback(
    (results) => {
      const now = performance.now();
      gestureTriggeredRef.current = false;

      if (!enabled || !results || !results.landmarks || results.landmarks.length === 0) {
        isGestureActiveRef.current = false;
        handsCountRef.current = 0;

        // When hand disappears, disengage intensity control but keep current value
        if (intensityStateRef.current === INTENSITY_ENGAGED) {
          intensityStateRef.current = INTENSITY_IDLE;
          isIntensityControlActiveRef.current = false;
        }

        return {
          intensity: smoothedIntensityRef.current,
          filterIndex: filterIndexRef.current,
          gestureState: gestureStateRef.current,
          handsCount: 0,
          gestureTriggered: false,
          intensityControlActive: false,
          landmarks: null,
        };
      }

      const numHands = results.landmarks.length;
      handsCountRef.current = numHands;
      isGestureActiveRef.current = true;

      // Check cooldown
      if (gestureStateRef.current === GESTURE_COOLDOWN) {
        if (now - cooldownTimerRef.current > COOLDOWN_MS) {
          gestureStateRef.current = GESTURE_IDLE;
        } else {
          return {
            intensity: smoothedIntensityRef.current,
            filterIndex: filterIndexRef.current,
            gestureState: GESTURE_COOLDOWN,
            handsCount: numHands,
            gestureTriggered: false,
            intensityControlActive: isIntensityControlActiveRef.current,
            landmarks: results.landmarks,
          };
        }
      }

      // === ONE HAND: Intensity control (requires deliberate pinch to engage) ===
      if (numHands === 1) {
        const landmarks = results.landmarks[0];
        const dist = normalizedPinchDistance(landmarks);
        const pinched = isPinching(landmarks);
        const open = isOpen(landmarks);

        switch (intensityStateRef.current) {
          case INTENSITY_IDLE:
            // User must deliberately pinch to enter intensity control mode
            if (pinched) {
              intensityStateRef.current = INTENSITY_ENGAGED;
              isIntensityControlActiveRef.current = true;
              intensityDisengageTimerRef.current = 0;
            }
            // Do NOT update intensity — leave it at whatever it was set to
            break;

          case INTENSITY_ENGAGED:
            // Actively tracking finger distance → intensity
            {
              const rawIntensity = mapToIntensity(dist);

              // Smooth the intensity value
              smoothedIntensityRef.current = lerp(
                smoothedIntensityRef.current,
                rawIntensity,
                0.2
              );

              // Notify when change is significant
              const rounded = Math.round(smoothedIntensityRef.current * 100);
              if (onIntensityChangeRef.current) {
                onIntensityChangeRef.current(rounded);
              }

              // Check if user has been fully open for a while → disengage
              if (open) {
                if (intensityDisengageTimerRef.current === 0) {
                  intensityDisengageTimerRef.current = now;
                } else if (now - intensityDisengageTimerRef.current > INTENSITY_DISENGAGE_MS) {
                  intensityStateRef.current = INTENSITY_IDLE;
                  isIntensityControlActiveRef.current = false;
                }
              } else {
                // Reset disengage timer if fingers come back together
                intensityDisengageTimerRef.current = 0;
              }
            }
            break;

          default:
            break;
        }

        // Reset two-hand state when going to one hand
        if (gestureStateRef.current === GESTURE_BOTH_PINCHED) {
          gestureStateRef.current = GESTURE_IDLE;
        }
      }

      // === TWO HANDS: Filter switching gesture ===
      if (numHands === 2) {
        // Disengage intensity control when both hands appear
        intensityStateRef.current = INTENSITY_IDLE;
        isIntensityControlActiveRef.current = false;

        const leftLandmarks = results.landmarks[0];
        const rightLandmarks = results.landmarks[1];

        const leftPinched = isPinching(leftLandmarks);
        const rightPinched = isPinching(rightLandmarks);
        const leftOpen = isOpen(leftLandmarks);
        const rightOpen = isOpen(rightLandmarks);

        const bothPinched = leftPinched && rightPinched;
        const bothOpen = leftOpen && rightOpen;

        switch (gestureStateRef.current) {
          case GESTURE_IDLE:
            if (bothPinched) {
              gestureStateRef.current = GESTURE_BOTH_PINCHED;
            }
            break;

          case GESTURE_BOTH_PINCHED:
            if (bothOpen) {
              // Trigger filter change!
              const newIndex = getNextFilterIndex(filterIndexRef.current);
              filterIndexRef.current = newIndex;
              gestureTriggeredRef.current = true;

              // Enter cooldown
              gestureStateRef.current = GESTURE_COOLDOWN;
              cooldownTimerRef.current = now;
              lastGestureTimeRef.current = now;

              // Notify UI
              if (onFilterChangeRef.current) {
                onFilterChangeRef.current(newIndex);
              }
              if (onGestureTriggeredRef.current) {
                onGestureTriggeredRef.current(newIndex);
              }
            }
            break;

          default:
            break;
        }
      }

      return {
        intensity: smoothedIntensityRef.current,
        filterIndex: filterIndexRef.current,
        gestureState: gestureStateRef.current,
        handsCount: numHands,
        gestureTriggered: gestureTriggeredRef.current,
        intensityControlActive: isIntensityControlActiveRef.current,
        landmarks: results.landmarks,
      };
    },
    [enabled]
  );

  return {
    processGesture,
    setOnFilterChange,
    setOnIntensityChange,
    setOnGestureTriggered,
    setFilterIndex,
    setIntensity,
    filterIndexRef,
    smoothedIntensityRef,
    gestureStateRef,
    isGestureActiveRef,
    isIntensityControlActiveRef,
    handsCountRef,
  };
}
