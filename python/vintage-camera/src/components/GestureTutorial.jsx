/**
 * GestureTutorial — First-use overlay with gesture instructions.
 * Shows on initial camera open, dismisses on first gesture or manual close.
 * Completion state persisted in localStorage.
 */
import { Hand, Grip } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function GestureTutorial({ show, onDismiss }) {
  if (!show) return null;

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className="gesture-tutorial"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.4 }}
        >
          <motion.div
            className="gesture-tutorial-card"
            initial={{ y: 30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -20, opacity: 0 }}
            transition={{ delay: 0.1, duration: 0.4 }}
          >
            <h3 className="gesture-tutorial-title">Gesture Controls</h3>

            <div className="gesture-tutorial-items">
              <div className="gesture-tutorial-item">
                <div className="gesture-tutorial-icon">
                  <Hand size={28} />
                </div>
                <div className="gesture-tutorial-text">
                  <strong>One Hand</strong>
                  <p>Pinch thumb & index to control filter intensity</p>
                </div>
              </div>

              <div className="gesture-tutorial-item">
                <div className="gesture-tutorial-icon">
                  <Grip size={28} />
                </div>
                <div className="gesture-tutorial-text">
                  <strong>Both Hands</strong>
                  <p>Pinch both hands, then open to switch filters</p>
                </div>
              </div>
            </div>

            <button
              onClick={onDismiss}
              className="gesture-tutorial-btn"
            >
              Got it
            </button>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
