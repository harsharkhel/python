/**
 * CaptureButton — Camera shutter with capture preview.
 * Captures the filtered canvas frame, shows preview with
 * Retake/Save options, and handles download.
 */
import { useState, useCallback } from 'react';
import { Camera, Download, RotateCcw, X } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { captureFilteredFrame, downloadImage } from '../utils/imageUtils';

export default function CaptureButton({ cameraViewRef, filterName }) {
  const [capturedImage, setCapturedImage] = useState(null);
  const [isFlashing, setIsFlashing] = useState(false);

  const handleCapture = useCallback(async () => {
    const cameraView = cameraViewRef.current;
    if (!cameraView) return;

    const canvas = cameraView.getCanvas();
    if (!canvas) return;

    // Flash animation
    setIsFlashing(true);
    setTimeout(() => setIsFlashing(false), 200);

    // Capture the filtered frame
    const dataURL = await captureFilteredFrame(canvas);
    setCapturedImage(dataURL);
  }, [cameraViewRef]);

  const handleSave = useCallback(() => {
    if (capturedImage) {
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const safeName = (filterName || 'photo').toLowerCase().replace(/\s+/g, '-');
      downloadImage(capturedImage, `vintage-${safeName}-${timestamp}.jpg`);
    }
  }, [capturedImage, filterName]);

  const handleRetake = useCallback(() => {
    setCapturedImage(null);
  }, []);

  const handleClose = useCallback(() => {
    setCapturedImage(null);
  }, []);

  return (
    <>
      {/* Shutter flash overlay */}
      <AnimatePresence>
        {isFlashing && (
          <motion.div
            className="shutter-flash"
            initial={{ opacity: 0.8 }}
            animate={{ opacity: 0 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
          />
        )}
      </AnimatePresence>

      {/* Capture button */}
      {!capturedImage && (
        <button
          onClick={handleCapture}
          className="capture-btn"
          aria-label="Capture photo"
        >
          <div className="capture-btn-inner">
            <Camera size={24} />
          </div>
        </button>
      )}

      {/* Preview modal */}
      <AnimatePresence>
        {capturedImage && (
          <motion.div
            className="capture-preview"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
          >
            <div className="capture-preview-content">
              <button
                onClick={handleClose}
                className="capture-close-btn"
                aria-label="Close preview"
              >
                <X size={20} />
              </button>

              <img
                src={capturedImage}
                alt="Captured photo"
                className="capture-preview-image"
              />

              <div className="capture-preview-actions">
                <button
                  onClick={handleRetake}
                  className="capture-action-btn capture-retake-btn"
                >
                  <RotateCcw size={18} />
                  <span>Retake</span>
                </button>

                <button
                  onClick={handleSave}
                  className="capture-action-btn capture-save-btn"
                >
                  <Download size={18} />
                  <span>Save Photo</span>
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
