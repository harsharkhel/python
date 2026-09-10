/**
 * useHandTracking — Custom hook for MediaPipe HandLandmarker.
 * Loads the WASM runtime + model, runs detection in rAF loop,
 * and exposes results via a ref (not state) for zero re-render overhead.
 */
import { useRef, useCallback, useEffect, useState } from 'react';

// We'll dynamically import MediaPipe to avoid blocking initial load
let FilesetResolver = null;
let HandLandmarker = null;

async function loadMediaPipe() {
  if (FilesetResolver && HandLandmarker) return;

  const vision = await import('@mediapipe/tasks-vision');
  FilesetResolver = vision.FilesetResolver;
  HandLandmarker = vision.HandLandmarker;
}

export default function useHandTracking(videoRef, isActive, enabled = true) {
  const handLandmarkerRef = useRef(null);
  const resultsRef = useRef(null);
  const animFrameRef = useRef(null);
  const lastTimestampRef = useRef(-1);

  const [isLoading, setIsLoading] = useState(false);
  const [isReady, setIsReady] = useState(false);
  const [error, setError] = useState(null);

  /**
   * Initialize the HandLandmarker.
   */
  const initialize = useCallback(async () => {
    if (!enabled || handLandmarkerRef.current) return;

    setIsLoading(true);
    setError(null);

    try {
      await loadMediaPipe();

      const vision = await FilesetResolver.forVisionTasks(
        'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm'
      );

      const handLandmarker = await HandLandmarker.createFromOptions(vision, {
        baseOptions: {
          modelAssetPath:
            'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
          delegate: 'GPU',
        },
        runningMode: 'VIDEO',
        numHands: 2,
        minHandDetectionConfidence: 0.5,
        minHandPresenceConfidence: 0.5,
        minTrackingConfidence: 0.5,
      });

      handLandmarkerRef.current = handLandmarker;
      setIsReady(true);
      setIsLoading(false);
    } catch (err) {
      console.error('MediaPipe initialization error:', err);

      // Try CPU fallback
      try {
        await loadMediaPipe();

        const vision = await FilesetResolver.forVisionTasks(
          'https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest/wasm'
        );

        const handLandmarker = await HandLandmarker.createFromOptions(vision, {
          baseOptions: {
            modelAssetPath:
              'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task',
            delegate: 'CPU',
          },
          runningMode: 'VIDEO',
          numHands: 2,
          minHandDetectionConfidence: 0.5,
          minHandPresenceConfidence: 0.5,
          minTrackingConfidence: 0.5,
        });

        handLandmarkerRef.current = handLandmarker;
        setIsReady(true);
        setIsLoading(false);
      } catch (cpuErr) {
        console.error('MediaPipe CPU fallback also failed:', cpuErr);
        setError('Hand tracking could not be initialized. Manual controls are still available.');
        setIsLoading(false);
      }
    }
  }, [enabled]);

  /**
   * Run detection loop — called from the main render loop externally.
   * This function is designed to be called from requestAnimationFrame
   * by the CameraView component, NOT to run its own rAF loop.
   * This avoids running two separate animation loops.
   */
  const detect = useCallback(() => {
    if (
      !handLandmarkerRef.current ||
      !videoRef.current ||
      videoRef.current.readyState < 2
    ) {
      return null;
    }

    const video = videoRef.current;
    const timestamp = performance.now();

    // MediaPipe requires strictly increasing timestamps
    if (timestamp <= lastTimestampRef.current) {
      return resultsRef.current;
    }

    lastTimestampRef.current = timestamp;

    try {
      const results = handLandmarkerRef.current.detectForVideo(video, timestamp);
      resultsRef.current = results;
      return results;
    } catch (err) {
      // Silently handle detection errors (common during camera transitions)
      return resultsRef.current;
    }
  }, [videoRef]);

  /**
   * Get the latest results without triggering detection.
   */
  const getResults = useCallback(() => {
    return resultsRef.current;
  }, []);

  // Initialize when enabled and camera is active
  useEffect(() => {
    if (isActive && enabled && !handLandmarkerRef.current && !isLoading) {
      initialize();
    }
  }, [isActive, enabled, initialize, isLoading]);

  // Cleanup on unmount or disable
  useEffect(() => {
    return () => {
      if (handLandmarkerRef.current) {
        handLandmarkerRef.current.close();
        handLandmarkerRef.current = null;
      }
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
      setIsReady(false);
    };
  }, []);

  return {
    detect,
    getResults,
    resultsRef,
    isLoading,
    isReady,
    error,
    initialize,
  };
}
