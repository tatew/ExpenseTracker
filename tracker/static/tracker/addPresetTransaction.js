function clickedPresetType(type) {
    const incomeButton = document.getElementById("incomePresetType");
    const expenseButton = document.getElementById("expensePresetType");
    const isExpense = document.getElementById("id_isExpense");
    if (type === "income") {
        isExpense.setAttribute("value", false)
        incomeButton.className = "btn btn-primary btn-active card medium-card"
        expenseButton.className = "btn btn-primary card medium-card"
    } else {
        isExpense.setAttribute("value", true)
        incomeButton.className = "btn btn-primary card medium-card"
        expenseButton.className = "btn btn-primary btn-active card medium-card"
    }
}