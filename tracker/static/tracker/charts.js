const transactionData = JSON.parse(document.getElementById('transactionData').textContent);
console.log(transactionData)
const dates = transactionData.netByDate.map(t => t.date)
const amounts = transactionData.netByDate.map(t => parseFloat(t.total))

const gridColor = '#6c757d'
const labelColor = '#6c757d'
Chart.defaults.font.family = "'JetBrains Mono', monospace"
Chart.defaults.color = labelColor

const data = {
labels: dates,
    datasets: [{
        label: transactionData.timelineChartTitle,
        backgroundColor: '#a3cfbb',
        borderColor: '#198754',
        data: amounts,
    }]
};

const config = {
    type: 'line',
    data: data,
    options: {
        maintainAspectRatio: false,
        scales: {
            x: {
                grid: {
                    color: gridColor
                }
            },
            y: {
                grid: {
                    color: gridColor
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Balance Over Time',
                color: '#FFFFFF',
                font: {
                    weight: 'bold',
                    size: '20'
                }
            }
        }
    }
};
const myChart = new Chart(
    document.getElementById('myChart'),
    config
);