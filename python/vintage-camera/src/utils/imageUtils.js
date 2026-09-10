/**
 * Image utility functions for capturing and saving filtered frames.
 */

/**
 * Capture the current canvas content as a downloadable image.
 * @param {HTMLCanvasElement} canvas
 * @param {string} filename - Download filename
 * @param {string} format - Image format ('image/png' or 'image/jpeg')
 * @param {number} quality - JPEG quality 0-1
 * @returns {Promise<string>} Data URL of the captured image
 */
export function captureFilteredFrame(
  canvas,
  filename = 'vintage-photo',
  format = 'image/jpeg',
  quality = 0.92
) {
  return new Promise((resolve) => {
    const dataURL = canvas.toDataURL(format, quality);
    resolve(dataURL);
  });
}

/**
 * Download a data URL as a file.
 * @param {string} dataURL
 * @param {string} filename
 */
export function downloadImage(dataURL, filename = 'vintage-photo.jpg') {
  const link = document.createElement('a');
  link.download = filename;
  link.href = dataURL;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/**
 * Convert canvas to Blob.
 * @param {HTMLCanvasElement} canvas
 * @param {string} format
 * @param {number} quality
 * @returns {Promise<Blob>}
 */
export function canvasToBlob(canvas, format = 'image/jpeg', quality = 0.92) {
  return new Promise((resolve) => {
    canvas.toBlob(
      (blob) => resolve(blob),
      format,
      quality
    );
  });
}
