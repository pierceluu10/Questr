const SENTIMENT_MINIMUM = -1;
const SENTIMENT_MAXIMUM = 1;
const SENTIMENT_THRESHOLD = 0.1;
const CATEGORY_LABELS = ['Social', 'Health', 'Mindfulness'];
const charts = [];
const controller = new AbortController();
class MoodResponseError extends Error {}

function palette() {
  const style = getComputedStyle(document.documentElement);
  return Object.fromEntries(['ink', 'body', 'line', 'green', 'green-soft', 'clay', 'honey'].map(
    name => [name, style.getPropertyValue(`--${name}`).trim()],
  ));
}
function sentimentLabel(score) {
  if (score > SENTIMENT_THRESHOLD) return 'Positive';
  if (score < -SENTIMENT_THRESHOLD) return 'Negative';
  return 'Neutral';
}
function chartOptions(colors) {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: !matchMedia('(prefers-reduced-motion: reduce)').matches,
    color: colors.body,
    plugins: { legend: { display: false } },
  };
}
function showStatus(canvas, status, text) {
  canvas.hidden = true;
  status.hidden = false;
  status.textContent = text;
}
function showCanvas(canvas, status) {
  status.hidden = true;
  canvas.hidden = false;
}
function initializeCategories() {
  const canvas = document.getElementById('categoryChart');
  const status = document.getElementById('category-status');
  const counts = [canvas.dataset.socialCount, canvas.dataset.healthCount, canvas.dataset.mindfulnessCount].map(Number);
  if (!counts.some(count => count > 0)) {
    showStatus(canvas, status, 'Complete a quest to start your history.');
    return;
  }
  const colors = palette();
  showCanvas(canvas, status);
  charts.push(new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels: CATEGORY_LABELS,
      datasets: [{ data: counts, backgroundColor: [colors.clay, colors.green, colors.honey], borderWidth: 0 }],
    },
    options: { ...chartOptions(colors), cutout: '76%' },
  }));
}
async function initializeMood() {
  const canvas = document.getElementById('moodChart');
  const status = document.getElementById('mood-status');
  try {
    const response = await fetch('/api/mood-data', { signal: controller.signal });
    if (!response.ok) throw new MoodResponseError(`Mood endpoint returned ${response.status}`);
    const data = await response.json();
    if (!Array.isArray(data.dates) || !Array.isArray(data.scores) || data.dates.length !== data.scores.length || !data.scores.every(Number.isFinite)) {
      throw new MoodResponseError('Mood endpoint returned invalid chart data');
    }
    if (data.dates.length === 0) {
      showStatus(canvas, status, 'Your first reflection will start this story.');
      return;
    }
    const colors = palette();
    showCanvas(canvas, status);
    const latestScore = data.scores.at(-1);
    document.getElementById('mood-summary').textContent = `${data.dates.length} reflection${data.dates.length === 1 ? '' : 's'} · Latest entry: ${sentimentLabel(latestScore).toLowerCase()} sentiment`;
    charts.push(new Chart(canvas, {
      type: 'line',
      data: {
        labels: data.dates,
        datasets: [{ label: 'Journal sentiment', data: data.scores, borderColor: colors.green, backgroundColor: colors['green-soft'], borderWidth: 2, pointRadius: 3, fill: true, tension: 0.25 }],
      },
      options: {
        ...chartOptions(colors),
        interaction: { intersect: false, mode: 'index' },
        scales: {
          x: { grid: { display: false }, ticks: { color: colors.body, maxTicksLimit: 4, maxRotation: 0 } },
          y: { min: SENTIMENT_MINIMUM, max: SENTIMENT_MAXIMUM, ticks: { color: colors.body, maxTicksLimit: 3, callback: sentimentLabel }, grid: { color: colors.line } },
        },
      },
    }));
  } catch (error) {
    if (error.name === 'AbortError') return;
    if (!(error instanceof MoodResponseError || error instanceof TypeError || error instanceof SyntaxError)) throw error;
    showStatus(canvas, status, 'Your reflections couldn’t load. Refresh to try again.');
    console.error('Journal chart request failed:', error);
  }
}
function updateChartAppearance() {
  const colors = palette();
  for (const chart of charts) {
    chart.options.color = colors.body;
    const dataset = chart.data.datasets[0];
    if (chart.config.type === 'line') {
      dataset.borderColor = colors.green;
      dataset.backgroundColor = colors['green-soft'];
      chart.options.scales.x.ticks.color = colors.body;
      chart.options.scales.y.ticks.color = colors.body;
      chart.options.scales.y.grid.color = colors.line;
    } else {
      dataset.backgroundColor = [colors.clay, colors.green, colors.honey];
    }
    chart.update('none');
  }
}
if (document.getElementById('moodChart')) {
  if (typeof Chart === 'undefined') {
    showStatus(document.getElementById('moodChart'), document.getElementById('mood-status'), 'Chart display is unavailable. Your entries are listed below.');
    showStatus(document.getElementById('categoryChart'), document.getElementById('category-status'), 'Chart display is unavailable. Your category totals are listed below.');
  } else {
    initializeCategories();
    initializeMood();
    document.addEventListener('appearancechange', updateChartAppearance);
    window.addEventListener('pagehide', () => {
      controller.abort();
      document.removeEventListener('appearancechange', updateChartAppearance);
      for (const chart of charts) chart.destroy();
    }, { once: true });
  }
}
