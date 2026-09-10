/**
 * GestureIndicator — Center-screen animation on filter switch.
 * Shows the new filter name with an elegant fade-in/out animation
 * when the two-hand gesture successfully triggers a filter change.
 */
import { motion, AnimatePresence } from 'framer-motion';

export default function GestureIndicator({ filterName, show }) {
  return (
    <AnimatePresence>
      {show && (
        <motion.div
          className="gesture-indicator"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 1.05 }}
          transition={{ duration: 0.4, ease: 'easeOut' }}
        >
          <span className="gesture-indicator-label">Filter</span>
          <span className="gesture-indicator-name">{filterName}</span>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
