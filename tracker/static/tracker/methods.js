function clickEdit(id) {
    clickNewMethodCancel();
    const newMethodButton = document.getElementById("addMethodButton");
    newMethodButton.style.display ="none";    

    const title = document.getElementById("method" + id + "Title");
    const input = document.getElementById("method" + id + "Input");

    const del = document.getElementById("method" + id + "ToggleActive");
    const cancel = document.getElementById("method" + id + "Cancel");

    const edit = document.getElementById("method" + id + "Edit");
    const submit = document.getElementById("method" + id + "Submit");

    title.setAttribute("hidden", "true");
    input.removeAttribute("hidden");

    del.setAttribute("hidden", "true");
    cancel.removeAttribute("hidden");

    edit.setAttribute("hidden", "true");
    submit.removeAttribute("hidden");
}

function clickCancel(id) {
    const title = document.getElementById("method" + id + "Title");
    const input = document.getElementById("method" + id + "Input");

    const del = document.getElementById("method" + id + "ToggleActive");
    const cancel = document.getElementById("method" + id + "Cancel");

    const edit = document.getElementById("method" + id + "Edit");
    const submit = document.getElementById("method" + id + "Submit");

    input.setAttribute("hidden", "true");
    title.removeAttribute("hidden");

    cancel.setAttribute("hidden", "true");
    del.removeAttribute("hidden");

    submit.setAttribute("hidden", "true");
    edit.removeAttribute("hidden");

    const newMethodButton = document.getElementById("addMethodButton");
    newMethodButton.style.display ="block"
}

function clickNew() {
    const newMethodButton = document.getElementById("addMethodButton");
    newMethodButton.style.display ="none";

    const newMethodRow = document.getElementById("addNewMethodRow");
    newMethodRow.style.display = "grid";

}

function clickNewMethodCancel() {
    const newMethodRow = document.getElementById("addNewMethodRow");
    newMethodRow.style.display = "none";

    const newMethodButton = document.getElementById("addMethodButton");
    newMethodButton.style.display ="block";
}