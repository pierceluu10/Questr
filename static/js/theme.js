const THEME_KEY = 'questr-appearance';
const LIGHT_THEME = 'light';
const DARK_THEME = 'dark';
const button = document.querySelector('.theme-toggle');
let appearance = LIGHT_THEME;
try {
  appearance = localStorage.getItem(THEME_KEY) === DARK_THEME ? DARK_THEME : LIGHT_THEME;
} catch (error) {
  if (!(error instanceof DOMException)) throw error;
}
function applyAppearance() {
  document.documentElement.dataset.theme = appearance;
  button.setAttribute('aria-pressed', String(appearance === DARK_THEME));
  button.setAttribute('aria-label', `Use ${appearance === DARK_THEME ? 'light' : 'dark'} appearance`);
  document.dispatchEvent(new Event('appearancechange'));
}
if (button) {
  button.hidden = false;
  applyAppearance();
  button.addEventListener('click', () => {
    appearance = appearance === DARK_THEME ? LIGHT_THEME : DARK_THEME;
    applyAppearance();
    try {
      localStorage.setItem(THEME_KEY, appearance);
    } catch (error) {
      if (!(error instanceof DOMException)) throw error;
    }
  });
}
