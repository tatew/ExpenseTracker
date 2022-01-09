const transactionData = JSON.parse(document.getElementById('transactionData').textContent);
console.log(transactionData)

const gridColor = '#6c757d'
const labelColor = '#6c757d'
Chart.defaults.font.family = "'JetBrains Mono', monospace"
Chart.defaults.color = labelColor

const netByDateDates = transactionData.netByDate.map(t => t.date)
const netByDateAmounts = transactionData.netByDate.map(t => parseFloat(t.total))

const netByDateData = {
labels: netByDateDates,
    datasets: [{
        label: 'Balance',
        backgroundColor: '#a3cfbb',
        borderColor: '#198754',
        data: netByDateAmounts,
    }]
};

const runningTransactionTotalConfig = {
    type: 'line',
    data: netByDateData,
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

const runningTransactionTotal = new Chart(
    document.getElementById('runningTransactionTotal'),
    runningTransactionTotalConfig
);

const transactionsByDateDates = transactionData.incomesByDate.map(t => t.date)
const incomes = transactionData.incomesByDate.map(t => parseFloat(t.total))
const expenses = transactionData.expensesByDate.map(t => parseFloat(t.total))

const transactionsByDateData = {
    labels: transactionsByDateDates,
        datasets: [
            {
                label: 'Incomes',
                backgroundColor: '#198754',
                data: incomes,
            },
            {
                label: 'Expenses',
                backgroundColor: '#dc3545',
                data: expenses,
            }
        ]
    };
    
const transactionsByDateConfig = {
    type: 'bar',
    data: transactionsByDateData,
    options: {
        maintainAspectRatio: false,
        scales: {
            x: {
                stacked: true,
                grid: {
                    color: gridColor
                }
            },
            y: {
                stacked: true,
                grid: {
                    color: gridColor
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Transactions By Date',
                color: '#FFFFFF',
                font: {
                    weight: 'bold',
                    size: '20'
                }
            }
        }
    }
};

const transactionsByDate = new Chart(
    document.getElementById('transactionsByDate'),
    transactionsByDateConfig
);