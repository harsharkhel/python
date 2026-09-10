/**
 * Filter Engine — central registry for all camera filters.
 * Each filter is a configuration object with an apply method.
 * New filters can be added by importing and registering them here.
 */
import normalFilter from './normal';
import blackWhiteFilter from './blackWhite';
import vintageFilter from './vintage';
import oldMoneyFilter from './oldMoney';

/**
 * Ordered list of available filters.
 * The order here determines the cycling order for gesture control.
 */
export const filters = [
  normalFilter,
  blackWhiteFilter,
  vintageFilter,
  oldMoneyFilter,
];

/**
 * Get a filter by its ID.
 * @param {string} id
 * @returns {object|undefined}
 */
export function getFilterById(id) {
  return filters.find((f) => f.id === id);
}

/**
 * Get the next filter index in the cycle.
 * @param {number} currentIndex
 * @returns {number}
 */
export function getNextFilterIndex(currentIndex) {
  return (currentIndex + 1) % filters.length;
}

/**
 * Get the previous filter index in the cycle.
 * @param {number} currentIndex
 * @returns {number}
 */
export function getPrevFilterIndex(currentIndex) {
  return (currentIndex - 1 + filters.length) % filters.length;
}

/**
 * Apply a filter to a canvas context.
 * @param {CanvasRenderingContext2D} ctx
 * @param {HTMLCanvasElement} canvas
 * @param {number} filterIndex
 * @param {number} intensity - 0 to 1
 */
export function applyFilter(ctx, canvas, filterIndex, intensity) {
  const filter = filters[filterIndex];
  if (filter && filter.apply) {
    filter.apply(ctx, canvas, intensity);
  }
}

export default filters;
