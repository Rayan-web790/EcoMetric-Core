document.addEventListener('DOMContentLoaded', () => {
    const sections = ['overview', 'funnel', 'segments', 'behavior'];
    const navItems = document.querySelectorAll('nav li');
    const contentSections = document.querySelectorAll('.content-section');
    const refreshBtn = document.getElementById('refresh-data');

    // Navigation logic
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const sectionId = item.getAttribute('data-section');
            
            // Update active nav
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Update visible section
            contentSections.forEach(section => {
                section.style.display = section.id === `section-${sectionId}` ? 'block' : 'none';
            });

            // Update header title
            document.querySelector('header h1').innerText = item.innerText.trim();
        });
    });

    // Data Fetching
    async function fetchData() {
        try {
            const response = await fetch('./data/dashboard_data.json');
            if (!response.ok) throw new Error('Data not found');
            const data = await response.json();
            updateDashboard(data);
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            // Fallback for demo if needed
        }
    }

    function updateDashboard(data) {
        // Update KPIs
        const kpis = data.kpis;
        document.querySelector('#kpi-revenue .kpi-value').innerText = `$${kpis.total_revenue.toLocaleString()}`;
        document.querySelector('#kpi-users .kpi-value').innerText = kpis.total_users.toLocaleString();
        document.querySelector('#kpi-orders .kpi-value').innerText = kpis.total_orders.toLocaleString();
        document.querySelector('#kpi-cr .kpi-value').innerText = `${kpis.conversion_rate}%`;

        // Render Sparkline (Simple Chart.js)
        const ctx = document.getElementById('revenue-sparkline').getContext('2d');
        const dailyData = Object.values(data.daily_revenue);
        const dailyLabels = Object.keys(data.daily_revenue);

        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dailyLabels,
                datasets: [{
                    data: dailyData,
                    borderColor: '#38bdf8',
                    borderWidth: 2,
                    pointRadius: 0,
                    fill: true,
                    backgroundColor: 'rgba(56, 189, 248, 0.1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false } },
                scales: {
                    x: { display: false },
                    y: { display: false }
                }
            }
        });
    }

    refreshBtn.addEventListener('click', () => {
        refreshBtn.innerText = 'Refreshing...';
        setTimeout(() => {
            fetchData();
            refreshBtn.innerText = 'Refresh Data';
        }, 1000);
    });

    // Initial fetch
    fetchData();
});
