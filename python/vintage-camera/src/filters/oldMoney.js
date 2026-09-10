/**
 * Old Money filter — sophisticated luxury/editorial photography effect.
 * Creates a European summer / vintage luxury / old-money editorial look.
 * 
 * Characteristics:
 * - Warm highlights with creamy tones
 * - Muted, desaturated colors (especially greens/blues)
 * - Soft contrast with lifted blacks
 * - Subtle brown/beige tint
 * - Cinematic vignette
 * - Subtle film grain
 */

// Reusable grain canvas for Old Money
let omGrainCanvas = null;
let omGrainCtx = null;
let omGrainFrame = 0;
let omGrainSize = { w: 0, h: 0 };

function generateOldMoneyGrain(width, height) {
  omGrainFrame++;
  if (
    omGrainCanvas &&
    omGrainSize.w === width &&
    omGrainSize.h === height &&
    omGrainFrame % 4 !== 0
  ) {
    return omGrainCanvas;
  }

  if (!omGrainCanvas) {
    omGrainCanvas = document.createElement('canvas');
    omGrainCtx = omGrainCanvas.getContext('2d');
  }

  const scale = 0.4;
  const gw = Math.floor(width * scale);
  const gh = Math.floor(height * scale);
  omGrainCanvas.width = gw;
  omGrainCanvas.height = gh;
  omGrainSize = { w: width, h: height };

  const imageData = omGrainCtx.createImageData(gw, gh);
  const data = imageData.data;

  for (let i = 0; i < data.length; i += 4) {
    const v = Math.random() * 40 - 20;
    data[i] = 128 + v;
    data[i + 1] = 128 + v;
    data[i + 2] = 128 + v;
    data[i + 3] = 255;
  }

  omGrainCtx.putImageData(imageData, 0, 0);
  return omGrainCanvas;
}

const oldMoneyFilter = {
  id: 'oldmoney',
  name: 'Old Money',
  description: 'European luxury editorial photography',

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
    const desaturation = 0.35 * intensity;     // overall desaturation
    const softContrast = 1.0 + 0.08 * intensity; // very soft contrast
    const liftedBlacks = 25 * intensity;       // lifted shadows
    const warmHighlight = 10 * intensity;      // warm highlights
    const brownTint = 0.15 * intensity;        // brown/beige tint amount

    for (let i = 0; i < len; i += 4) {
      let r = data[i];
      let g = data[i + 1];
      let b = data[i + 2];

      // 1. Selective desaturation — more aggressive on greens and blues
      const lum = 0.299 * r + 0.587 * g + 0.114 * b;

      // Determine how "green" or "blue" the pixel is
      const greenDominance = Math.max(0, g - Math.max(r, b)) / 255;
      const blueDominance = Math.max(0, b - Math.max(r, g)) / 255;
      const coolFactor = greenDominance + blueDominance;

      // Extra desaturation for cool colors
      const extraDesat = coolFactor * 0.4 * intensity;
      const totalDesat = desaturation + extraDesat;

      r = lum + (r - lum) * (1 - totalDesat);
      g = lum + (g - lum) * (1 - totalDesat);
      b = lum + (b - lum) * (1 - totalDesat);

      // 2. Brown/beige tint (warm cream)
      const tintR = lum * 1.06;
      const tintG = lum * 0.97;
      const tintB = lum * 0.82;
      r = r + (tintR - r) * brownTint;
      g = g + (tintG - g) * brownTint;
      b = b + (tintB - b) * brownTint;

      // 3. Warm highlights — add warmth to bright areas
      const brightness = lum / 255;
      if (brightness > 0.5) {
        const highlightFactor = (brightness - 0.5) * 2 * warmHighlight;
        r = r + highlightFactor * 0.8;
        g = g + highlightFactor * 0.3;
        b = b - highlightFactor * 0.2;
      }

      // 4. Creamy skin tones — gentle push for mid-range warm tones
      if (r > g && g > b && lum > 80 && lum < 200) {
        const skinFactor = 0.05 * intensity;
        r = r + 4 * skinFactor * (1 - Math.abs(lum - 140) / 140);
        g = g + 2 * skinFactor * (1 - Math.abs(lum - 140) / 140);
      }

      // 5. Soft contrast
      r = (r - 128) * softContrast + 128;
      g = (g - 128) * softContrast + 128;
      b = (b - 128) * softContrast + 128;

      // 6. Lifted blacks (raise shadows)
      r = r + liftedBlacks * (1 - r / 255);
      g = g + liftedBlacks * (1 - g / 255);
      b = b + liftedBlacks * (1 - b / 255);

      // Clamp
      data[i] = Math.max(0, Math.min(255, r));
      data[i + 1] = Math.max(0, Math.min(255, g));
      data[i + 2] = Math.max(0, Math.min(255, b));
    }

    ctx.putImageData(imageData, 0, 0);

    // 7. Cinematic vignette (softer than vintage)
    if (intensity > 0.1) {
      const cx = w / 2;
      const cy = h / 2;
      const radius = Math.max(w, h) * 0.75;
      const gradient = ctx.createRadialGradient(cx, cy, radius * 0.4, cx, cy, radius);
      gradient.addColorStop(0, 'rgba(0, 0, 0, 0)');
      gradient.addColorStop(0.6, `rgba(20, 15, 10, ${0.08 * intensity})`);
      gradient.addColorStop(1, `rgba(20, 15, 10, ${0.35 * intensity})`);

      ctx.fillStyle = gradient;
      ctx.fillRect(0, 0, w, h);
    }

    // 8. Subtle film grain
    if (intensity > 0.2) {
      const grainTexture = generateOldMoneyGrain(w, h);
      ctx.save();
      ctx.globalAlpha = 0.04 * intensity;
      ctx.globalCompositeOperation = 'overlay';
      ctx.drawImage(grainTexture, 0, 0, w, h);
      ctx.restore();
    }
  },
};

export default oldMoneyFilter;
