function clickedShowMore() {
    const form = document.getElementById("listTransactionsForm");
    const numToShowElement = document.getElementsByName("numToShow")[0];
    const numToShow = parseInt(numToShowElement.getAttribute("value"));
    numToShowElement.setAttribute("value", numToShow + 10);
    form.submit();
}