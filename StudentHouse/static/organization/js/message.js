let elem = document.getElementById('message')
let pMessage = document.getElementById('pMessage')
if (pMessage.firstChild !== null) {
    console.log('can you clear me')
    setTimeout(() => {
        elem.style.display = 'none'
    }, 3000)
}