/**
 * useCamera — Custom hook for camera stream management.
 * Handles permission requests, stream lifecycle, camera switching,
 * and error states. Uses refs for performance-critical video access.
 */
import { useState, useRef, useCallback, useEffect } from 'react';
import {
  getPreferredConstraints,
  stopStream,
  isMobileDevice,
  isGetUserMediaSupported,
} from '../utils/cameraUtils';

export default function useCamera() {
  const videoRef = useRef(null);
  const streamRef = useRef(null);

  const [isActive, setIsActive] = useState(false);
  const [error, setError] = useState(null);
  const [facingMode, setFacingMode] = useState(
    isMobileDevice() ? 'environment' : 'user'
  );
  const [isLoading, setIsLoading] = useState(false);

  /**
   * Start camera with given facing mode.
   */
  const startCamera = useCallback(async (mode) => {
    setIsLoading(true);
    setError(null);

    if (!isGetUserMediaSupported()) {
      setError('Your browser does not support camera access.');
      setIsLoading(false);
      return false;
    }

    // Stop any existing stream
    stopStream(streamRef.current);

    try {
      const constraints = getPreferredConstraints(mode || facingMode);
      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      streamRef.current = stream;

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        await videoRef.current.play();
      }

      setIsActive(true);
      setIsLoading(false);
      return true;
    } catch (err) {
      console.error('Camera error:', err);

      // Try fallback to front camera if rear failed on mobile
      if (mode === 'environment') {
        try {
          const fallbackConstraints = getPreferredConstraints('user');
          const stream = await navigator.mediaDevices.getUserMedia(
            fallbackConstraints
          );
          streamRef.current = stream;

          if (videoRef.current) {
            videoRef.current.srcObject = stream;
            await videoRef.current.play();
          }

          setFacingMode('user');
          setIsActive(true);
          setIsLoading(false);
          return true;
        } catch (fallbackErr) {
          // Both failed
        }
      }

      if (err.name === 'NotAllowedError') {
        setError('Camera access was denied. Please allow camera permissions and try again.');
      } else if (err.name === 'NotFoundError') {
        setError('No camera found. Please connect a camera and try again.');
      } else if (err.name === 'NotReadableError') {
        setError('Camera is already in use by another application.');
      } else {
        setError(`Camera error: ${err.message}`);
      }

      setIsActive(false);
      setIsLoading(false);
      return false;
    }
  }, [facingMode]);

  /**
   * Stop the camera stream.
   */
  const stopCamera = useCallback(() => {
    stopStream(streamRef.current);
    streamRef.current = null;

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setIsActive(false);
  }, []);

  /**
   * Switch between front and rear cameras.
   */
  const switchCamera = useCallback(async () => {
    const newMode = facingMode === 'user' ? 'environment' : 'user';
    setFacingMode(newMode);
    if (isActive) {
      await startCamera(newMode);
    }
  }, [facingMode, isActive, startCamera]);

  /**
   * Retry camera access (useful after permission denial).
   */
  const retryCamera = useCallback(() => {
    return startCamera(facingMode);
  }, [startCamera, facingMode]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopStream(streamRef.current);
    };
  }, []);

  return {
    videoRef,
    isActive,
    error,
    facingMode,
    isLoading,
    startCamera,
    stopCamera,
    switchCamera,
    retryCamera,
    isFrontCamera: facingMode === 'user',
  };
}
