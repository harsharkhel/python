/**
 * FilterSelector — Bottom carousel for manual filter selection.
 * Shows all available filters with the active one highlighted.
 * Supports click/tap selection and animated transitions.
 */
import { useRef } from 'react';
import { filters } from '../filters/filterEngine';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function FilterSelector({ activeIndex, onSelect, disabled }) {
  const containerRef = useRef(null);

  const handlePrev = () => {
    const newIndex = (activeIndex - 1 + filters.length) % filters.length;
    onSelect(newIndex);
  };

  const handleNext = () => {
    const newIndex = (activeIndex + 1) % filters.length;
    onSelect(newIndex);
  };

  return (
    <div className="filter-selector" role="tablist" aria-label="Camera filters">
      {/* Active filter name with animation */}
      <div className="filter-active-name">
        <button
          onClick={handlePrev}
          className="filter-arrow-btn"
          aria-label="Previous filter"
          disabled={disabled}
        >
          <ChevronLeft size={18} />
        </button>

        <AnimatePresence mode="wait">
          <motion.span
            key={activeIndex}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.2 }}
            className="filter-name-text"
          >
            {filters[activeIndex]?.name}
          </motion.span>
        </AnimatePresence>

        <button
          onClick={handleNext}
          className="filter-arrow-btn"
          aria-label="Next filter"
          disabled={disabled}
        >
          <ChevronRight size={18} />
        </button>
      </div>

      {/* Filter dots */}
      <div className="filter-dots" ref={containerRef}>
        {filters.map((filter, index) => (
          <button
            key={filter.id}
            role="tab"
            aria-selected={index === activeIndex}
            aria-label={`${filter.name} filter`}
            className={`filter-dot ${index === activeIndex ? 'filter-dot-active' : ''}`}
            onClick={() => onSelect(index)}
            disabled={disabled}
          >
            <span className="sr-only">{filter.name}</span>
          </button>
        ))}
      </div>
    </div>
  );
}
