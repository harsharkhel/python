/**
 * Vintage filter — realistic analog 35mm film effect.
 * Applies warm color temperature, reduced saturation, faded blacks,
 * increased contrast, subtle sepia, film grain, and vignette.
 */

// Pre-generate a noise texture for film grain (reused across frames)
let grainCanvas = null;
let grainCtx = null;
let lastGrainSize = { w: 0, h: 0 };
let grainFrameCount = 0;

function generateGrainTexture(width, height) {
  // Only regenerate every few frames for a "stuck grain" film effect
  grainFrameCount++;
  if (
    grainCanvas &&
    lastGrainSize.w === width &&
    lastGrainSize.h === height &&
    grainFrameCount % 3 !== 0
  ) {
    return grainCanvas;
  }

  if (!grainCanvas) {
    grainCanvas = document.createElement('canvas');
    grainCtx = grainCanvas.getContext('2d');
  }

  // Use a smaller canvas for grain (performance), we'll scale up
  const scale = 0.5;
  const gw = Math.floor(width * scale);
  const gh = Math.floor(height * scale);
  grainCanvas.width = gw;
  grainCanvas.height = gh;
  lastGrainSize = { w: width, h: height };

  const imageData = grainCtx.createImageData(gw, gh);
  const data = imageData.data;

  for (let i = 0; i < data.length; i += 4) {
    const v = Math.random() * 60 - 30; // -30 to +30
    data[i] = 128 + v;
    data[i + 1] = 128 + v;
    data[i + 2] = 128 + v;
    data[i + 3] = 255;
  }

  grainCtx.putImageData(imageData, 0, 0);
  return grainCanvas;
}

const vintageFilter = {
  id: 'vintage',
  name: 'Vintage',
  description: 'Analog 35mm film photography',

  /**
   * @param {CanvasRenderingContext2D} ctx
   * @param {HTMLCanvasElement} canvas
   * @param {number} intensity - 0 to 1
   */
  apply(ctx, canvas, intensity) {
    if (intensity <= 0) return;

    const w = canvas.width;
    const h = canvas.height;
    const imageData = ctx.getImageData(0, 0, w, h);
    const data = imageData.data;
    const len = data.length;

    // Parameters scaled by intensity
    const warmth = 15 * intensity;         // warm color temp
    const saturationMul = 1.0 - 0.3 * intensity; // reduce saturation
    const contrast = 1.0 + 0.2 * intensity;
    const fadedBlacks = 20 * intensity;    // lift blacks
    const sepiaAmount = 0.25 * intensity;

    for (let i = 0; i < len; i += 4) {
      let r = data[i];
      let g = data[i + 1];
      let b = data[i + 2];

      // 1. Warm color temperature
      r = r + warmth;
      g = g + warmth * 0.4;
      b = b - warmth * 0.5;

      // 2. Reduce saturation
      const gray = 0.299 * r + 0.587 * g + 0.114 * b;
      r = gray + (r - gray) * saturationMul;
      g = gray + (g - gray) * saturationMul;
      b = gray + (b - gray) * saturationMul;

      // 3. Sepia tint
      const sr = gray * 1.1;
      const sg = gray * 0.9;
      const sb = gray * 0.7;
      r = r + (sr - r) * sepiaAmount;
      g = g + (sg - g) * sepiaAmount;
      b = b + (sb - b) * sepiaAmount;

      // 4. Contrast
      r = (r - 128) * contrast + 128;
      g = (g - 128) * contrast + 128;
      b = (b - 128) * contrast + 128;

      // 5. Faded blacks (lift shadows)
      r = r + fadedBlacks * (1 - r / 255);
      g = g + fadedBlacks * (1 - g / 255);
      b = b + fadedBlacks * (1 - b / 255);

      // Clamp
      data[i] = Math.max(0, Math.min(255, r));
      data[i + 1] = Math.max(0, Math.min(255, g));
      data[i + 2] = Math.max(0, Math.min(255, b));
    }

    ctx.putImageData(imageData, 0, 0);

    // 6. Vignette overlay
    if (intensity > 0.1) {
      const cx = w / 2;
      const cy = h / 2;
      const radius = Math.max(w, h) * 0.7;
      const gradient = ctx.createRadialGradient(cx, cy, radius * 0.3, cx, cy, radius);
      gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
      gradient.addColorStop(0.7, `rgba(0, 0, 0, ${0.15 * intensity})`);
      gradient.addColorStop(1, `rgba(0, 0, 0, ${0.45 * intensity})`);

      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, w, h);
    }

    // 7. Film grain overlay
    if (intensity > 0.2) {
      const grainTexture = generateGrainTexture(w, h);
      ctx.save();
      ctx.globalAlpha = 0.06 * intensity;
      ctx.globalCompositeOperation = 'overlay';
      ctx.drawImage(grainTexture, 0, 0, w, h);
      ctx.restore();
    }
  },
};

export default vintageFilter;
