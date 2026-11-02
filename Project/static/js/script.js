/**
 * CodePulse AI - Enterprise Cybersecurity SaaS Client Logic
 * Handles sidebar toggles, theme switching, sample autofill, Chart.js instances, and preferences.
 */

document.addEventListener('DOMContentLoaded', () => {

  // =========================================================================
  // 1. Theme Management (Dark / Light / High Contrast)
  // =========================================================================
  const savedTheme = localStorage.getItem('cp_theme') || 'dark';
  applyTheme(savedTheme);

  const themeToggleButtons = document.querySelectorAll('.btn-theme-toggle');
  themeToggleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const nextTheme = current === 'dark' ? 'contrast' : (current === 'contrast' ? 'light' : 'dark');
      applyTheme(nextTheme);
    });
  });

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('cp_theme', theme);

    // Update theme toggle icons if present
    document.querySelectorAll('.theme-icon').forEach(icon => {
      if (theme === 'light') {
        icon.className = 'bi bi-sun-fill theme-icon text-warning';
      } else if (theme === 'contrast') {
        icon.className = 'bi bi-circle-half theme-icon text-cyan';
      } else {
        icon.className = 'bi bi-moon-stars-fill theme-icon text-primary';
      }
    });
  }

  // =========================================================================
  // 2. Sidebar Navigation (Desktop Collapse & Mobile Drawer)
  // =========================================================================
  const sidebar = document.getElementById('sidebar');
  const sidebarToggle = document.getElementById('btnSidebarToggle');
  const mobileBackdrop = document.getElementById('sidebarBackdrop');

  // Restore desktop collapsed state from preferences
  const isCollapsed = localStorage.getItem('cp_sidebar_collapsed') === 'true';
  if (sidebar && isCollapsed && window.innerWidth > 991) {
    sidebar.classList.add('collapsed');
  }

  // If on History page without an explicit per_page URL parameter, apply saved page size preference
  if (window.location.pathname.endsWith('/history')) {
    const savedPageSize = localStorage.getItem('cp_page_size');
    const urlParams = new URLSearchParams(window.location.search);
    if (savedPageSize && !urlParams.has('per_page') && savedPageSize !== '15') {
      urlParams.set('per_page', savedPageSize);
      window.location.search = urlParams.toString();
    }
  }

  if (sidebarToggle && sidebar) {
    sidebarToggle.addEventListener('click', () => {
      if (window.innerWidth <= 991) {
        // Mobile toggle
        sidebar.classList.toggle('mobile-open');
        if (mobileBackdrop) mobileBackdrop.classList.toggle('active');
      } else {
        // Desktop collapse toggle
        sidebar.classList.toggle('collapsed');
        localStorage.setItem('cp_sidebar_collapsed', sidebar.classList.contains('collapsed'));
      }
    });
  }

  if (mobileBackdrop && sidebar) {
    mobileBackdrop.addEventListener('click', () => {
      sidebar.classList.remove('mobile-open');
      mobileBackdrop.classList.remove('active');
    });
  }

  // =========================================================================
  // 3. Interactive URL Scanner & Sample Quick-Fills
  // =========================================================================
  const urlInput = document.getElementById('urlInput');
  const btnClearInput = document.getElementById('btnClearInput');
  const samplePills = document.querySelectorAll('.sample-pill');

  function updateClearButton() {
    if (!urlInput || !btnClearInput) return;
    btnClearInput.style.display = urlInput.value.trim().length > 0 ? 'inline-flex' : 'none';
  }

  if (urlInput) {
    urlInput.addEventListener('input', updateClearButton);
    updateClearButton();
  }

  if (btnClearInput && urlInput) {
    btnClearInput.addEventListener('click', () => {
      urlInput.value = '';
      updateClearButton();
      urlInput.focus();
    });
  }

  samplePills.forEach(pill => {
    pill.addEventListener('click', () => {
      const sampleUrl = pill.getAttribute('data-sample');
      if (urlInput && sampleUrl) {
        urlInput.value = sampleUrl;
        updateClearButton();
        urlInput.focus();

        // Visual pulse feedback
        const parentBox = urlInput.closest('.scanner-console-box') || urlInput;
        parentBox.classList.add('border-primary');
        setTimeout(() => parentBox.classList.remove('border-primary'), 350);
      }
    });
  });

  // URL Form Submit & Animated Radar Overlay
  const analyzeForm = document.getElementById('analyzeForm');
  const loadingOverlay = document.getElementById('loadingOverlay');
  const loadingStatusText = document.getElementById('loadingStatusText');

  if (analyzeForm) {
    analyzeForm.addEventListener('submit', (e) => {
      const urlVal = urlInput ? urlInput.value.trim() : '';
      if (!urlVal) {
        e.preventDefault();
        alert('Please enter a target website URL to scan.');
        return;
      }

      // Check if animation is enabled in preferences (default: true)
      const enableAnimation = localStorage.getItem('cp_enable_animations') !== 'false';
      if (loadingOverlay && enableAnimation) {
        loadingOverlay.style.display = 'flex';

        const scanSteps = [
          'Parsing URL lexical syntax...',
          'Extracting 17 heuristic features...',
          'Checking IP and host redirection indicators...',
          'Evaluating Scikit-Learn Random Forest Classifier...',
          'Computing calibrated threat confidence score...'
        ];
        let stepIdx = 0;
        const interval = setInterval(() => {
          stepIdx++;
          if (stepIdx < scanSteps.length && loadingStatusText) {
            loadingStatusText.textContent = scanSteps[stepIdx];
          } else {
            clearInterval(interval);
          }
        }, 320);
      }
    });
  }

  // Dismiss overlay when page restores from browser back cache
  window.addEventListener('pageshow', () => {
    if (loadingOverlay) loadingOverlay.style.display = 'none';
  });

  // =========================================================================
  // 4. Clipboard Copy Helper (with legacy fallback for non-HTTPS/IP access)
  // =========================================================================
  const copyButtons = document.querySelectorAll('.btn-copy-url');
  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetText = btn.getAttribute('data-copy');
      if (!targetText) return;

      const notifySuccess = () => {
        const originalHTML = btn.innerHTML;
        btn.innerHTML = '<i class="bi bi-check2 text-success"></i> Copied!';
        setTimeout(() => {
          btn.innerHTML = originalHTML;
        }, 2000);
      };

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(targetText).then(notifySuccess).catch(() => {
          fallbackCopy(targetText);
        });
      } else {
        fallbackCopy(targetText);
      }

      function fallbackCopy(text) {
        try {
          const ta = document.createElement('textarea');
          ta.value = text;
          ta.setAttribute('readonly', '');
          ta.style.position = 'fixed';
          ta.style.opacity = '0';
          ta.style.pointerEvents = 'none';
          document.body.appendChild(ta);
          ta.select();
          document.execCommand('copy');
          document.body.removeChild(ta);
          notifySuccess();
        } catch (e) {
          console.warn('Copy to clipboard failed:', e);
        }
      }
    });
  });

  // =========================================================================
  // 5. Auto-dismiss Flash Alerts
  // =========================================================================
  document.querySelectorAll('.alert-dismissible').forEach(alertEl => {
    setTimeout(() => {
      if (window.bootstrap && bootstrap.Alert) {
        const bsAlert = bootstrap.Alert.getInstance(alertEl) || new bootstrap.Alert(alertEl);
        bsAlert.close();
      }
    }, 5000);
  });

  // =========================================================================
  // 6. Chart.js Invocations by Page Context
  // =========================================================================
  if (typeof Chart !== 'undefined') {
    // Cyber Operations Theme Defaults for Chart.js
    Chart.defaults.color = '#94a3b8';
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.plugins.tooltip.backgroundColor = '#151F30';
    Chart.defaults.plugins.tooltip.borderColor = 'rgba(59, 130, 246, 0.3)';
    Chart.defaults.plugins.tooltip.borderWidth = 1;

    // Overview Page Charts
    if (!window.OVERVIEW_ANALYTICS_DATA) {
      const el = document.getElementById('overviewAnalyticsData');
      if (el && el.dataset.analytics) {
        try { window.OVERVIEW_ANALYTICS_DATA = JSON.parse(el.dataset.analytics); } catch (e) { console.warn('Failed to parse overview data:', e); }
      }
    }
    if (window.OVERVIEW_ANALYTICS_DATA) {
      renderOverviewCharts(window.OVERVIEW_ANALYTICS_DATA);
    }

    // Threat Analytics Page Charts
    if (!window.ANALYTICS_PAGE_DATA) {
      const el = document.getElementById('analyticsPageData');
      if (el && el.dataset.analytics) {
        try { window.ANALYTICS_PAGE_DATA = JSON.parse(el.dataset.analytics); } catch (e) { console.warn('Failed to parse analytics data:', e); }
      }
    }
    if (window.ANALYTICS_PAGE_DATA) {
      renderAnalyticsPageCharts(window.ANALYTICS_PAGE_DATA);
    }

    // Model Performance Page Charts
    if (!window.METRICS_DATA) {
      const el = document.getElementById('metricsData');
      if (el && el.dataset.metrics) {
        try { window.METRICS_DATA = JSON.parse(el.dataset.metrics); } catch (e) { console.warn('Failed to parse metrics data:', e); }
      }
    }
    if (window.METRICS_DATA) {
      renderModelPerformanceCharts(window.METRICS_DATA);
    }
  }

  // =========================================================================
  // 7. Settings Page Preferences Logic
  // =========================================================================
  const settingsForm = document.getElementById('settingsPreferencesForm');
  if (settingsForm) {
    // Populate current values
    const selTheme = document.getElementById('prefTheme');
    const chkAnimations = document.getElementById('prefAnimations');
    const selSidebar = document.getElementById('prefSidebar');
    const selPageSize = document.getElementById('prefPageSize');

    if (selTheme) selTheme.value = localStorage.getItem('cp_theme') || 'dark';
    if (chkAnimations) chkAnimations.checked = localStorage.getItem('cp_enable_animations') !== 'false';
    if (selSidebar) selSidebar.value = localStorage.getItem('cp_sidebar_collapsed') === 'true' ? 'collapsed' : 'expanded';
    if (selPageSize) selPageSize.value = localStorage.getItem('cp_page_size') || '15';

    settingsForm.addEventListener('submit', (e) => {
      e.preventDefault();
      if (selTheme) {
        applyTheme(selTheme.value);
      }
      if (chkAnimations) {
        localStorage.setItem('cp_enable_animations', chkAnimations.checked ? 'true' : 'false');
      }
      if (selSidebar) {
        const shouldCollapse = selSidebar.value === 'collapsed';
        localStorage.setItem('cp_sidebar_collapsed', shouldCollapse ? 'true' : 'false');
        if (sidebar) sidebar.classList.toggle('collapsed', shouldCollapse);
      }
      if (selPageSize) {
        localStorage.setItem('cp_page_size', selPageSize.value);
      }

      // Show toast confirmation
      const toastEl = document.getElementById('settingsSavedToast');
      if (toastEl && window.bootstrap && bootstrap.Toast) {
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
      } else {
        alert('Settings successfully updated!');
      }
    });

    const btnResetPrefs = document.getElementById('btnResetPreferences');
    if (btnResetPrefs) {
      btnResetPrefs.addEventListener('click', () => {
        localStorage.removeItem('cp_theme');
        localStorage.removeItem('cp_enable_animations');
        localStorage.removeItem('cp_sidebar_collapsed');
        localStorage.removeItem('cp_page_size');
        applyTheme('dark');
        if (sidebar) sidebar.classList.remove('collapsed');
        alert('Preferences reset to default values.');
        window.location.reload();
      });
    }
  }
});

// =========================================================================
// Chart.js Rendering Functions
// =========================================================================

/**
 * Render Overview Dashboard Charts
 */
function renderOverviewCharts(data) {
  // Chart 1: Detection Distribution Doughnut
  const distCtx = document.getElementById('overviewDistributionChart');
  if (distCtx && data.stats) {
    const legit = data.stats.legitimate || 0;
    const phish = data.stats.phishing || 0;

    new Chart(distCtx, {
      type: 'doughnut',
      data: {
        labels: ['Safe / Legitimate', 'Phishing Threat'],
        datasets: [{
          data: [legit, phish],
          backgroundColor: ['#22C55E', '#EF4444'],
          borderColor: '#151F30',
          borderWidth: 2,
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { boxWidth: 12, padding: 15, color: '#94a3b8' }
          }
        },
        cutout: '72%'
      }
    });
  }

  // Chart 2: Daily Scan Activity Timeline
  const actCtx = document.getElementById('overviewActivityChart');
  if (actCtx && data.daily_trends && data.daily_trends.length > 0) {
    const dates = data.daily_trends.map(d => d.scan_date);
    const safeCounts = data.daily_trends.map(d => d.legitimate);
    const phishCounts = data.daily_trends.map(d => d.phishing);

    new Chart(actCtx, {
      type: 'bar',
      data: {
        labels: dates,
        datasets: [
          {
            label: 'Safe URLs',
            data: safeCounts,
            backgroundColor: 'rgba(34, 197, 94, 0.75)',
            borderColor: '#22C55E',
            borderWidth: 1,
            borderRadius: 4
          },
          {
            label: 'Phishing URLs',
            data: phishCounts,
            backgroundColor: 'rgba(239, 68, 68, 0.75)',
            borderColor: '#EF4444',
            borderWidth: 1,
            borderRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { stacked: true, grid: { display: false } },
          y: { stacked: true, grid: { color: 'rgba(255, 255, 255, 0.05)' }, beginAtZero: true }
        },
        plugins: {
          legend: { position: 'top', labels: { boxWidth: 12, color: '#94a3b8' } }
        }
      }
    });
  }
}

/**
 * Render Threat Analytics Page Charts
 */
function renderAnalyticsPageCharts(data) {
  // Chart 1: Volume & Trends
  const volCtx = document.getElementById('analyticsVolumeChart');
  if (volCtx && data.daily_trends && data.daily_trends.length > 0) {
    const labels = data.daily_trends.map(d => d.scan_date);
    const totals = data.daily_trends.map(d => d.total);
    const phish = data.daily_trends.map(d => d.phishing);

    new Chart(volCtx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Total Scans',
            data: totals,
            borderColor: '#3B82F6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            fill: true,
            tension: 0.35,
            pointRadius: 4
          },
          {
            label: 'Phishing Intercepted',
            data: phish,
            borderColor: '#EF4444',
            backgroundColor: 'rgba(239, 68, 68, 0.1)',
            fill: true,
            tension: 0.35,
            pointRadius: 4
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: { grid: { color: 'rgba(255, 255, 255, 0.04)' } },
          y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
        }
      }
    });
  }

  // Chart 2: Threat Ratio Doughnut
  const ratioCtx = document.getElementById('analyticsRatioChart');
  if (ratioCtx && data.stats) {
    new Chart(ratioCtx, {
      type: 'doughnut',
      data: {
        labels: ['Safe Verified', 'Phishing Flagged'],
        datasets: [{
          data: [data.stats.legitimate, data.stats.phishing],
          backgroundColor: ['#22C55E', '#EF4444'],
          borderColor: '#151F30',
          borderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } },
        cutout: '70%'
      }
    });
  }

  // Chart 3: Confidence Score Bracket Distribution
  const confCtx = document.getElementById('analyticsConfidenceChart');
  if (confCtx && data.confidence_distribution) {
    const confLabels = Object.keys(data.confidence_distribution);
    const confValues = Object.values(data.confidence_distribution);

    new Chart(confCtx, {
      type: 'bar',
      data: {
        labels: confLabels,
        datasets: [{
          label: 'Scan Count',
          data: confValues,
          backgroundColor: [
            'rgba(34, 197, 94, 0.8)',
            'rgba(59, 130, 246, 0.8)',
            'rgba(6, 182, 212, 0.8)',
            'rgba(245, 158, 11, 0.8)',
            'rgba(239, 68, 68, 0.8)'
          ],
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // Chart 4: Risk Level Distribution
  const riskCtx = document.getElementById('analyticsRiskChart');
  if (riskCtx && data.risk_distribution) {
    const riskLabels = Object.keys(data.risk_distribution);
    const riskValues = Object.values(data.risk_distribution);

    new Chart(riskCtx, {
      type: 'bar',
      data: {
        labels: riskLabels,
        datasets: [{
          label: 'URLs',
          data: riskValues,
          backgroundColor: riskLabels.map(l => {
            if (l.includes('High')) return 'rgba(239, 68, 68, 0.8)';
            if (l.includes('Moderate')) return 'rgba(245, 158, 11, 0.8)';
            return 'rgba(34, 197, 94, 0.8)';
          }),
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { beginAtZero: true, grid: { color: 'rgba(255, 255, 255, 0.05)' } },
          y: { grid: { display: false } }
        }
      }
    });
  }
}

/**
 * Render Model Performance Center Charts
 */
function renderModelPerformanceCharts(metrics) {
  // Chart 1: Candidate Algorithm Comparison
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
            backgroundColor: 'rgba(59, 130, 246, 0.85)',
            borderColor: '#3B82F6',
            borderWidth: 1,
            borderRadius: 3
          },
          {
            label: 'Precision (%)',
            data: precisions,
            backgroundColor: 'rgba(34, 197, 94, 0.85)',
            borderColor: '#22C55E',
            borderWidth: 1,
            borderRadius: 3
          },
          {
            label: 'Recall (%)',
            data: recalls,
            backgroundColor: 'rgba(245, 158, 11, 0.85)',
            borderColor: '#F59E0B',
            borderWidth: 1,
            borderRadius: 3
          },
          {
            label: 'F1-Score (%)',
            data: f1s,
            backgroundColor: 'rgba(168, 85, 247, 0.85)',
            borderColor: '#A855F7',
            borderWidth: 1,
            borderRadius: 3
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { color: '#F8FAFC' } },
          tooltip: {
            callbacks: {
              label: (ctx) => `${ctx.dataset.label}: ${ctx.raw}%`
            }
          }
        },
        scales: {
          y: {
            min: 75,
            max: 100,
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { callback: (v) => v + '%' }
          },
          x: { grid: { display: false } }
        }
      }
    });
  }

  // Chart 2: Top Heuristic Feature Importances
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
          backgroundColor: 'rgba(6, 182, 212, 0.82)',
          borderColor: '#06B6D4',
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
            callbacks: { label: (ctx) => `Weight: ${ctx.raw}%` }
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.05)' },
            ticks: { callback: (v) => v + '%' }
          },
          y: { grid: { display: false } }
        }
      }
    });
  }
}
