/**
 * Black & White filter — classic monochrome photography.
 * Applies grayscale conversion with slightly increased contrast
 * and subtle brightness adjustment for a film-like B&W look.
 */
const blackWhiteFilter = {
  id: 'bw',
  name: 'B&W',
  description: 'Classic monochrome photography',

  /**
   * @param {CanvasRenderingContext2D} ctx
   * @param {HTMLCanvasElement} canvas
   * @param {number} intensity - 0 to 1
   */
  apply(ctx, canvas, intensity) {
    if (intensity <= 0) return;

    const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const data = imageData.data;
    const len = data.length;

    // Contrast multiplier (subtle increase)
    const contrast = 1.0 + 0.15 * intensity;
    // Brightness offset
    const brightness = 5 * intensity;

    for (let i = 0; i < len; i += 4) {
      const r = data[i];
      const g = data[i + 1];
      const b = data[i + 2];

      // Luminosity-weighted grayscale (perceptual)
      let gray = 0.299 * r + 0.587 * g + 0.114 * b;

      // Apply contrast around midpoint
      gray = ((gray - 128) * contrast + 128) + brightness;

      // Clamp
      gray = gray < 0 ? 0 : gray > 255 ? 255 : gray;

      // Blend original with B&W based on intensity
      data[i] = r + (gray - r) * intensity;
      data[i + 1] = g + (gray - g) * intensity;
      data[i + 2] = b + (gray - b) * intensity;
    }

    ctx.putImageData(imageData, 0, 0);
  },
};

export default blackWhiteFilter;
