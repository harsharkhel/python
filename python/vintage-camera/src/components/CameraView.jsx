/**
 * CameraView — Core camera rendering component.
 * Draws video frames to canvas, applies filters in real-time,
 * runs hand detection, and manages the render loop.
 *
 * Performance: Uses refs exclusively for animation state.
 * React only re-renders when UI-visible state changes.
 */
import { useRef, useEffect, useCallback, forwardRef, useImperativeHandle } from 'react';
import { applyFilter, filters } from '../filters/filterEngine';

const CameraView = forwardRef(function CameraView(
  {
    videoRef,
    isActive,
    isFrontCamera,
    mirrorSelfie,
    filterIndex,
    intensity,
    handTrackingDetect,
    gestureProcess,
    showHandTracking,
    onGestureResult,
  },
  ref
) {
  const canvasRef = useRef(null);
  const overlayCanvasRef = useRef(null);
  const animFrameRef = useRef(null);
  const filterIndexRef = useRef(filterIndex);
  const intensityRef = useRef(intensity);

  // Keep refs in sync with props
  useEffect(() => {
    filterIndexRef.current = filterIndex;
  }, [filterIndex]);

  useEffect(() => {
    intensityRef.current = intensity;
  }, [intensity]);

  // Expose canvas ref for photo capture
  useImperativeHandle(ref, () => ({
    getCanvas: () => canvasRef.current,
    getOverlayCanvas: () => overlayCanvasRef.current,
  }));

  /**
   * Draw hand landmarks on the overlay canvas.
   */
  const drawHandLandmarks = useCallback(
    (overlayCtx, landmarks, width, height, mirror) => {
      if (!showHandTracking || !landmarks) return;

      overlayCtx.clearRect(0, 0, width, height);

      for (const hand of landmarks) {
        const thumbTip = hand[4];
        const indexTip = hand[8];

        // Calculate positions
        let thumbX = thumbTip.x * width;
        let thumbY = thumbTip.y * height;
        let indexX = indexTip.x * width;
        let indexY = indexTip.y * height;

        if (mirror) {
          thumbX = width - thumbX;
          indexX = width - indexX;
        }

        // Draw fingertip indicators
        const radius = 8;

        // Thumb tip circle
        overlayCtx.beginPath();
        overlayCtx.arc(thumbX, thumbY, radius, 0, Math.PI * 2);
        overlayCtx.strokeStyle = 'rgba(212, 190, 158, 0.8)';
        overlayCtx.lineWidth = 2;
        overlayCtx.stroke();

        // Index tip circle
        overlayCtx.beginPath();
        overlayCtx.arc(indexX, indexY, radius, 0, Math.PI * 2);
        overlayCtx.strokeStyle = 'rgba(212, 190, 158, 0.8)';
        overlayCtx.lineWidth = 2;
        overlayCtx.stroke();

        // Draw connecting line when close (pinching)
        const dx = thumbX - indexX;
        const dy = thumbY - indexY;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 80) {
          overlayCtx.beginPath();
          overlayCtx.moveTo(thumbX, thumbY);
          overlayCtx.lineTo(indexX, indexY);
          overlayCtx.strokeStyle = `rgba(212, 190, 158, ${0.6 * (1 - dist / 80)})`;
          overlayCtx.lineWidth = 2;
          overlayCtx.stroke();

          // Draw midpoint glow
          const midX = (thumbX + indexX) / 2;
          const midY = (thumbY + indexY) / 2;
          const glowRadius = 4 + (1 - dist / 80) * 8;
          const gradient = overlayCtx.createRadialGradient(
            midX, midY, 0, midX, midY, glowRadius
          );
          gradient.addColorStop(0, `rgba(212, 190, 158, ${0.5 * (1 - dist / 80)})`);
          gradient.addColorStop(1, 'rgba(212, 190, 158, 0)');
          overlayCtx.fillStyle = gradient;
          overlayCtx.beginPath();
          overlayCtx.arc(midX, midY, glowRadius, 0, Math.PI * 2);
          overlayCtx.fill();
        }
      }
    },
    [showHandTracking]
  );

  /**
   * Main render loop.
   */
  const renderLoop = useCallback(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    const overlayCanvas = overlayCanvasRef.current;

    if (!video || !canvas || video.readyState < 2) {
      animFrameRef.current = requestAnimationFrame(renderLoop);
      return;
    }

    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    const overlayCtx = overlayCanvas?.getContext('2d');

    // Match canvas size to video
    if (canvas.width !== video.videoWidth || canvas.height !== video.videoHeight) {
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      if (overlayCanvas) {
        overlayCanvas.width = video.videoWidth;
        overlayCanvas.height = video.videoHeight;
      }
    }

    const w = canvas.width;
    const h = canvas.height;
    const mirror = isFrontCamera;

    // Draw video frame with optional mirroring
    ctx.save();
    if (mirror) {
      ctx.translate(w, 0);
      ctx.scale(-1, 1);
    }
    ctx.drawImage(video, 0, 0, w, h);
    ctx.restore();

    // Apply filter
    const currentFilterIndex = filterIndexRef.current;
    const currentIntensity = intensityRef.current;

    if (currentFilterIndex > 0) {
      applyFilter(ctx, canvas, currentFilterIndex, currentIntensity);
    }

    // Run hand detection and gesture processing
    let gestureResult = null;
    if (handTrackingDetect) {
      const handResults = handTrackingDetect();
      if (gestureProcess && handResults) {
        gestureResult = gestureProcess(handResults);

        // Update intensity from gesture ONLY when actively controlling
        // (user must deliberately pinch first to engage intensity mode)
        if (gestureResult && gestureResult.intensityControlActive) {
          intensityRef.current = gestureResult.intensity;
        }

        // Draw hand landmarks
        if (overlayCtx && gestureResult?.landmarks) {
          drawHandLandmarks(
            overlayCtx,
            gestureResult.landmarks,
            w,
            h,
            mirror
          );
        } else if (overlayCtx) {
          overlayCtx.clearRect(0, 0, w, h);
        }

        // Notify parent of gesture results (throttled in parent)
        if (onGestureResult) {
          onGestureResult(gestureResult);
        }
      }
    }

    animFrameRef.current = requestAnimationFrame(renderLoop);
  }, [
    videoRef,
    isFrontCamera,
    handTrackingDetect,
    gestureProcess,
    onGestureResult,
    drawHandLandmarks,
  ]);

  // Start/stop render loop
  useEffect(() => {
    if (isActive) {
      animFrameRef.current = requestAnimationFrame(renderLoop);
    }

    return () => {
      if (animFrameRef.current) {
        cancelAnimationFrame(animFrameRef.current);
      }
    };
  }, [isActive, renderLoop]);

  return (
    <div className="camera-view-container">
      {/* Hidden video element — source for canvas drawing */}
      <video
        ref={videoRef}
        autoPlay
        playsInline
        muted
        className="camera-video-hidden"
      />

      {/* Main filtered canvas */}
      <canvas
        ref={canvasRef}
        className="camera-canvas"
      />

      {/* Overlay canvas for hand tracking visualization */}
      <canvas
        ref={overlayCanvasRef}
        className="camera-overlay"
      />
    </div>
  );
});

export default CameraView;
