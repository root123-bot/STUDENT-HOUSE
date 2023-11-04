// this script intended to check only the 'user' status and at the end to submit our form
let check = document.getElementById("isactive")

check.addEventListener("click", (e) => {
    const isChecked = check.checked
    check.checked = isChecked
    console.log('is checked ', isChecked)
})