/**
 * Frontend JavaScript for Phishing Website Detection System
 * Handles UI animations, sample quick-fills, loading states, and Chart.js visualizations.
 */

document.addEventListener('DOMContentLoaded', () => {

  // 1. Quick Sample URL Autofill
  const sampleBadges = document.querySelectorAll('.sample-badge');
  const urlInput = document.getElementById('urlInput');

  sampleBadges.forEach(badge => {
    badge.addEventListener('click', () => {
      const sampleUrl = badge.getAttribute('data-sample');
      if (urlInput && sampleUrl) {
        urlInput.value = sampleUrl;
        urlInput.focus();
        // Trigger subtle pulse
        urlInput.classList.add('border-primary');
        setTimeout(() => urlInput.classList.remove('border-primary'), 400);
      }
    });
  });

  // 2. URL Analysis Form Submit & Loading Overlay
  const analyzeForm = document.getElementById('analyzeForm');
  const loadingOverlay = document.getElementById('loadingOverlay');
  const loadingStatusText = document.getElementById('loadingStatusText');

  if (analyzeForm) {
    analyzeForm.addEventListener('submit', (e) => {
      const urlVal = urlInput ? urlInput.value.trim() : '';
      if (!urlVal) {
        e.preventDefault();
        alert('Please enter a website URL to analyze.');
        return;
      }

      // Show animated loading overlay
      if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
        
        const steps = [
          'Parsing URL lexical syntax...',
          'Extracting 17 heuristic features...',
          'Checking IP and redirection indicators...',
          'Consulting trained ML Classifier...',
          'Computing calibrated confidence score...'
        ];
        let stepIdx = 0;
        const interval = setInterval(() => {
          stepIdx++;
          if (stepIdx < steps.length && loadingStatusText) {
            loadingStatusText.textContent = steps[stepIdx];
          } else {
            clearInterval(interval);
          }
        }, 350);
      }
    });
  }

  // 3. Clipboard Copy Helper
  const copyButtons = document.querySelectorAll('.btn-copy-url');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetText = btn.getAttribute('data-copy');
      if (targetText && navigator.clipboard) {
        navigator.clipboard.writeText(targetText).then(() => {
          const originalHTML = btn.innerHTML;
          btn.innerHTML = '<i class="bi bi-check2"></i> Copied!';
          setTimeout(() => {
            btn.innerHTML = originalHTML;
          }, 2000);
        });
      }
    });
  });

  // 4. Auto-dismiss Flash Alerts
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alertEl => {
    setTimeout(() => {
      if (window.bootstrap && bootstrap.Alert) {
        const bsAlert = bootstrap.Alert.getInstance(alertEl) || new bootstrap.Alert(alertEl);
        bsAlert.close();
      }
    }, 5000);
  });

  // 5. Dismiss Loading Overlay on page restore (e.g. browser back button)
  window.addEventListener('pageshow', () => {
    if (loadingOverlay) {
      loadingOverlay.style.display = 'none';
    }
  });

  // 6. Render Performance Charts if on Model Performance Page
  if (typeof window.METRICS_DATA !== 'undefined' && window.METRICS_DATA) {
    renderModelPerformanceCharts(window.METRICS_DATA);
  }
});

/**
 * Render Chart.js Visualizations for Model Evaluation
 */
function renderModelPerformanceCharts(metrics) {
  if (typeof Chart === 'undefined') {
    console.warn('Chart.js library is not available.');
    return;
  }
  // Chart defaults for Cyber Dark Theme
  Chart.defaults.color = '#94a3b8';
  Chart.defaults.font.family = "'Inter', sans-serif";

  // Chart 1: Model Comparison Chart
  const compCtx = document.getElementById('modelComparisonChart');
  if (compCtx && metrics.model_comparison) {
    const models = Object.keys(metrics.model_comparison);
    const accuracies = models.map(m => (metrics.model_comparison[m].accuracy * 100).toFixed(2));
    const precisions = models.map(m => (metrics.model_comparison[m].precision * 100).toFixed(2));
    const recalls = models.map(m => (metrics.model_comparison[m].recall * 100).toFixed(2));
    const f1s = models.map(m => (metrics.model_comparison[m].f1_score * 100).toFixed(2));

    new Chart(compCtx, {
      type: 'bar',
      data: {
        labels: models,
        datasets: [
          {
            label: 'Accuracy (%)',
            data: accuracies,
            backgroundColor: 'rgba(56, 189, 248, 0.85)',
            borderColor: '#38bdf8',
            borderWidth: 1
          },
          {
            label: 'Precision (%)',
            data: precisions,
            backgroundColor: 'rgba(16, 185, 129, 0.85)',
            borderColor: '#10b981',
            borderWidth: 1
          },
          {
            label: 'Recall (%)',
            data: recalls,
            backgroundColor: 'rgba(245, 158, 11, 0.85)',
            borderColor: '#f59e0b',
            borderWidth: 1
          },
          {
            label: 'F1-Score (%)',
            data: f1s,
            backgroundColor: 'rgba(139, 92, 246, 0.85)',
            borderColor: '#8b5cf6',
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: { color: '#f1f5f9' }
          },
          tooltip: {
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.raw}%`
            }
          }
        },
        scales: {
          y: {
            min: 75,
            max: 100,
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: {
              callback: (value) => value + '%'
            }
          },
          x: {
            grid: { display: false }
          }
        }
      }
    });
  }

  // Chart 2: Feature Importances Chart
  const featCtx = document.getElementById('featureImportanceChart');
  if (featCtx && metrics.feature_importances) {
    const topFeatures = metrics.feature_importances.slice(0, 10);
    const featLabels = topFeatures.map(f => f.feature.replace(/_/g, ' ').toUpperCase());
    const featValues = topFeatures.map(f => (f.importance * 100).toFixed(2));

    new Chart(featCtx, {
      type: 'bar',
      data: {
        labels: featLabels,
        datasets: [{
          label: 'Importance Weight (%)',
          data: featValues,
          backgroundColor: 'rgba(0, 242, 254, 0.8)',
          borderColor: '#00f2fe',
          borderWidth: 1,
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => `Weight: ${ctx.raw}%`
            }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: {
              callback: (val) => val + '%'
            }
          },
          y: {
            grid: { display: false }
          }
        }
      }
    });
  }
}

