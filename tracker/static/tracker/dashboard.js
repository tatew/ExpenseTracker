function clickedAllData() {
    const allTimeDataInput = document.getElementById("id_allData");
    allTimeDataInput.setAttribute("value", "true");
    document.getElementById("chartFilterForm").submit();
}



// ChartJS 
const chartData = JSON.parse(document.getElementById('chartData').textContent);
console.log(chartData);

const blue = '#0d6efd';
const indigo = '#6610f2';
const purple = '#6f42c1';
const pink = '#d63384';
const red = '#dc3545';
const orange = '#fd7e14';
const yellow = '#ffc107';
const green = '#198754';
const teal = '#20c997';
const cyan = '#0dcaf0';
const gray = '#adb5bd';

const gridColor = '#6c757d';
const labelColor = '#6c757d';
Chart.defaults.font.family = "'JetBrains Mono', monospace";
Chart.defaults.color = labelColor;

const netByDateDates = chartData.netByDate.map(t => t.date);
const netByDateAmounts = chartData.netByDate.map(t => parseFloat(t.total));

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

const transactionsByDateDates = chartData.incomesByDate.map(t => t.date)
const incomes = chartData.incomesByDate.map(t => parseFloat(t.total))
const expenses = chartData.expensesByDate.map(t => parseFloat(t.total))

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

const categories = chartData.categoryData.map(c => c.name);
const amountPerCategory = chartData.categoryData.map(c => parseInt(c.total));

const expensesPerCategoryData = {
    labels: categories,
    datasets: [{
        label: 'Categories',
        data: amountPerCategory,
        backgroundColor: [red, orange, yellow, green, teal, cyan, blue, indigo, purple, pink]
    }],
};

const display = window.innerWidth > 635 

const expensesPerCategoryConfig = {
    type: 'pie',
    data: expensesPerCategoryData,
    options: {
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Total Expenses by Category',
                color: '#FFFFFF',
                font: {
                    weight: 'bold',
                    size: '20'
                }
            },
            legend: {
                position: 'left',
                display: display
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        let label = context.label || '';

                        if (label) {
                            label += ': ';
                        }
                        if (context.parsed !== null) {
                            label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed);
                        }
                        return label;
                    }
                }
            }
        }
    }
};

const expensesPerCategory = new Chart(
    document.getElementById('expensesPerCategory'),
    expensesPerCategoryConfig
);

