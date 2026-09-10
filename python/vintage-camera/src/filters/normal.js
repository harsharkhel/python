/**
 * Normal filter — no modifications applied.
 * Acts as a passthrough for the raw camera feed.
 */
const normalFilter = {
  id: 'normal',
  name: 'Normal',
  description: 'No filter applied',

  /**
   * @param {CanvasRenderingContext2D} ctx
   * @param {HTMLCanvasElement} canvas
   * @param {number} intensity - 0 to 1 (unused for normal)
   */
  apply(ctx, canvas, intensity) {
    // No-op: the raw frame is already drawn to canvas
  },
};

export default normalFilter;
