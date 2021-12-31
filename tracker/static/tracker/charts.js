const transactionData = JSON.parse(document.getElementById('transactionData').textContent);
console.log(transactionData)
const dates = transactionData.netByDate.map(t => t.date)
const amounts = transactionData.netByDate.map(t => parseFloat(t.total))

Chart.defaults.font.family = "'JetBrains Mono', monospace"

const data = {
labels: dates,
    datasets: [{
        label: 'Net Transactions',
        backgroundColor: '#FFFFFF',
        borderColor: '#FFFFFF',
        data: amounts,
    }]
};

const config = {
    type: 'line',
    data: data,
    options: {
        
    }
};
const myChart = new Chart(
    document.getElementById('myChart'),
    config
);