
let submitbtn = document.getElementById("submitbtn")
let formElem = document.getElementById("formtosubmit")
let photoInput = document.getElementById('profilepicture')
let frontEndMsgElem = document.getElementById("frontEndMsg")
let frotnEndMsgPElem = document.getElementById("frontEndMessage")

function displayError(message) {
    frotnEndMsgPElem.innerText = message
    frontEndMsgElem.style.display = "block"
    setTimeout(() => {
        frontEndMsgElem.style.display = "none"
    }, 2000)
}

formElem.addEventListener('submit', (e) => {
    e.preventDefault();

    if (document.getElementById("fname").value.trim().length < 1) {
        const message = "The first name field is required"
        displayError(message)
        return;
    }

    if (document.getElementById("lname").value.trim().length < 1) {
        const message = "The last name field is required"
        displayError(message)
        return;
    }

    phone = document.getElementById('phone').value
    if (phone.trim().length < 10) {
        const message = "Incorrect phone number"
        displayError(message)
        return;
    }
    else if (isNaN(Number(phone.trim()))) {
        const message = 'Incorrect phone number omit +255, eg. 0712344520'
        displayError(message)
        return;
    }



    if (photoInput.value.trim().length > 1) {
        let value = photoInput.value.trim()
        let arrElem = value.split('.')
        ext = arrElem[arrElem.length - 1]

        if (ext != 'png' && ext != 'jpg' && ext != 'jpeg' && ext != 'gif') {
            const message = "unrecognized image format, use .png, .jpg, .jpeg or .gif"
            displayError(message)
            return;
        }
    }

    formElem.submit()
})