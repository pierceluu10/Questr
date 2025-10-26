// Questr Chart Utilities

// Initialize all charts when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
});

function initializeCharts() {
    // Initialize mood chart if element exists
    const moodChartElement = document.getElementById('moodChart');
    if (moodChartElement) {
        initializeMoodChart();
    }
    
    // Initialize category chart if element exists
    const categoryChartElement = document.getElementById('categoryChart');
    if (categoryChartElement) {
        initializeCategoryChart();
    }
}

function initializeMoodChart() {
    fetch('/api/mood-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('moodChart').getContext('2d');
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.dates,
                    datasets: [{
                        label: 'Mood Score',
                        data: data.scores,
                        borderColor: 'rgb(102, 126, 234)',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.4,
                        pointBackgroundColor: 'rgb(102, 126, 234)',
                        pointBorderColor: '#fff',
                        pointBorderWidth: 2,
                        pointRadius: 6,
                        pointHoverRadius: 8
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        tooltip: {
                            backgroundColor: 'rgba(0, 0, 0, 0.8)',
                            titleColor: '#fff',
                            bodyColor: '#fff',
                            borderColor: 'rgb(102, 126, 234)',
                            borderWidth: 1,
                            cornerRadius: 8
                        }
                    },
                    scales: {
                        x: {
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            },
                            ticks: {
                                color: '#666'
                            }
                        },
                        y: {
                            beginAtZero: true,
                            min: -1,
                            max: 1,
                            grid: {
                                color: 'rgba(0, 0, 0, 0.1)'
                            },
                            ticks: {
                                color: '#666',
                                callback: function(value) {
                                    if (value > 0.1) return 'Positive';
                                    if (value < -0.1) return 'Negative';
                                    return 'Neutral';
                                }
                            }
                        }
                    },
                    interaction: {
                        intersect: false,
                        mode: 'index'
                    }
                }
            });
        })
        .catch(error => {
            console.error('Error loading mood data:', error);
            // Show placeholder message with more padding
            const chartContainer = document.querySelector('#moodChart').parentElement;
            chartContainer.innerHTML = '<div class="text-center text-muted" style="padding: 80px 20px;"><i class="fas fa-chart-line fa-3x mb-3 d-block"></i><p class="mb-0">No mood data available yet</p></div>';
        });
}

function initializeCategoryChart() {
    // This will be populated with actual data from the template
    const ctx = document.getElementById('categoryChart').getContext('2d');
    
    // Get data from the template (this is a simplified version)
    const socialCount = parseInt(document.querySelector('[data-social-count]')?.dataset.socialCount || '0');
    const healthCount = parseInt(document.querySelector('[data-health-count]')?.dataset.healthCount || '0');
    const mindfulnessCount = parseInt(document.querySelector('[data-mindfulness-count]')?.dataset.mindfulnessCount || '0');
    
    // Check if there's any data
    const totalCount = socialCount + healthCount + mindfulnessCount;
    if (totalCount === 0) {
        const chartContainer = document.querySelector('#categoryChart').parentElement;
        chartContainer.innerHTML = '<div class="text-center text-muted" style="padding: 80px 20px;"><i class="fas fa-chart-pie fa-3x mb-3 d-block"></i><p class="mb-0">Complete a quest first</p></div>';
        return;
    }
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Social', 'Health', 'Mindfulness'],
            datasets: [{
                data: [socialCount, healthCount, mindfulnessCount],
                backgroundColor: [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 12,
                            weight: '500'
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleColor: '#fff',
                    bodyColor: '#fff',
                    borderColor: 'rgba(255, 255, 255, 0.2)',
                    borderWidth: 1,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = total > 0 ? Math.round((context.parsed / total) * 100) : 0;
                            return `${context.label}: ${context.parsed} quests (${percentage}%)`;
                        }
                    }
                }
            },
            cutout: '60%'
        }
    });
}

// Utility function to refresh charts
function refreshCharts() {
    // Destroy existing charts
    Chart.helpers.each(Chart.instances, function(instance) {
        instance.destroy();
    });
    
    // Reinitialize charts
    initializeCharts();
}

// Add smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add loading states to buttons
document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', function() {
        if (this.type === 'submit' || this.href) {
            this.classList.add('loading');
            const originalText = this.innerHTML;
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
            
            // Reset after 3 seconds (in case of errors)
            setTimeout(() => {
                this.classList.remove('loading');
                this.innerHTML = originalText;
            }, 3000);
        }
    });
});

// Add fade-in animation to cards
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
        }
    });
}, observerOptions);

// Observe all cards
document.querySelectorAll('.card, .quest-card, .stat-card').forEach(card => {
    observer.observe(card);
});

// === THEME SWITCHER ===
document.addEventListener("DOMContentLoaded", () => {
    // Create floating theme toggle button
    const toggleBtn = document.createElement("button");
    toggleBtn.className = "theme-toggle";
    toggleBtn.innerHTML = "🌗";
    document.body.appendChild(toggleBtn);

    // Load previous theme or default to light
    let theme = localStorage.getItem("theme") || "light";
    applyTheme(theme);

    // Button click cycle: light → dark → custom → light
    toggleBtn.addEventListener("click", () => {
        if (theme === "light") {
            theme = "dark";
        } else if (theme === "dark") {
            theme = "custom";
            // You can set your custom theme colors here 🌈
            document.body.style.setProperty("--user-primary", "#ffcc5e");
            document.body.style.setProperty("--user-secondary", "#f5d97d");
            document.body.style.setProperty("--user-bg", "#ffb3c0");
        } else {
            theme = "light";
        }
        applyTheme(theme);
        localStorage.setItem("theme", theme);
    });

    // Apply the theme to body
    function applyTheme(mode) {
        document.body.classList.remove("dark-theme", "custom-theme");
        if (mode === "dark") {
            document.body.classList.add("dark-theme");
        } else if (mode === "custom") {
            document.body.classList.add("custom-theme");
        }
    }
});
