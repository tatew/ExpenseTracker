const transactionData = JSON.parse(document.getElementById('transactionData').textContent);
const dates = transactionData.netByDate.map(t => t.date);
const amounts = transactionData.netByDate.map(t => parseFloat(t.total))
const labels = dates

Chart.defaults.font.family = "'JetBrains Mono', monospace"

const data = {
labels: labels,
    datasets: [{
        label: 'Net Transactions',
        backgroundColor: '#FFFFFF',
        borderColor: 'rgb(255, 99, 132)',
        data: amounts,
    }]
};

const config = {
    type: 'bar',
    data: data,
    options: {
        
    }
};
const myChart = new Chart(
    document.getElementById('myChart'),
    config
);