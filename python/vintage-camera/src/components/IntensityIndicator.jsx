/**
 * IntensityIndicator — Shows filter intensity during one-hand gesture.
 * Displays a horizontal progress bar with percentage.
 * Auto-hides after 2 seconds of inactivity.
 */
import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function IntensityIndicator({ intensity, isActive, filterName }) {
  const [visible, setVisible] = useState(false);
  const hideTimerRef = useRef(null);

  useEffect(() => {
    if (isActive) {
      setVisible(true);

      // Reset hide timer
      if (hideTimerRef.current) {
        clearTimeout(hideTimerRef.current);
      }

      hideTimerRef.current = setTimeout(() => {
        setVisible(false);
      }, 2000);
    }

    return () => {
      if (hideTimerRef.current) {
        clearTimeout(hideTimerRef.current);
      }
    };
  }, [isActive, intensity]);

  const percentage = Math.round(intensity * 100);

  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          className="intensity-indicator"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 10 }}
          transition={{ duration: 0.25 }}
        >
          <span className="intensity-label">Filter Intensity</span>
          <div className="intensity-bar-container">
            <div className="intensity-bar-track">
              <motion.div
                className="intensity-bar-fill"
                animate={{ width: `${percentage}%` }}
                transition={{ duration: 0.1 }}
              />
              <div
                className="intensity-bar-thumb"
                style={{ left: `${percentage}%` }}
              />
            </div>
          </div>
          <span className="intensity-value">{percentage}%</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
