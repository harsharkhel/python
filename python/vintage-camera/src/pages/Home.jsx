/**
 * Home — Landing page for VINTAGE.
 * Elegant, minimal design with brand identity,
 * tagline, and camera launch button.
 */
import { Camera, Shield, Sparkles, Hand } from 'lucide-react';
import { motion } from 'framer-motion';

export default function Home({ onOpenCamera }) {
  return (
    <div className="home-page">
      {/* Ambient background grain */}
      <div className="home-grain" />

      <motion.div
        className="home-content"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1.2, ease: 'easeOut' }}
      >
        {/* Brand */}
        <motion.div
          className="home-brand"
          initial={{ y: 30, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2, duration: 0.8 }}
        >
          <h1 className="home-title">VINTAGE</h1>
          <p className="home-tagline">Capture the moment differently.</p>
        </motion.div>

        {/* Description */}
        <motion.p
          className="home-description"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.5, duration: 0.8 }}
        >
          An analog-inspired camera controlled by your hands.
        </motion.p>

        {/* CTA Button */}
        <motion.button
          className="home-cta"
          onClick={onOpenCamera}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.8 }}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
        >
          <Camera size={20} />
          <span>Open Camera</span>
        </motion.button>

        {/* Feature tags */}
        <motion.div
          className="home-features"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 1.1, duration: 0.8 }}
        >
          <div className="home-feature">
            <Hand size={14} />
            <span>Gesture controlled</span>
          </div>
          <span className="home-feature-dot">·</span>
          <div className="home-feature">
            <Sparkles size={14} />
            <span>Film inspired</span>
          </div>
          <span className="home-feature-dot">·</span>
          <div className="home-feature">
            <Shield size={14} />
            <span>Private by design</span>
          </div>
        </motion.div>

        {/* Privacy note */}
        <motion.p
          className="home-privacy"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5, duration: 1 }}
        >
          Your camera stays on your device. Nothing is uploaded.
        </motion.p>
      </motion.div>

      {/* Decorative border */}
      <div className="home-border-frame" />
    </div>
  );
}
