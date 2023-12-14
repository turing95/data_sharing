
function closeMessage() {
    let messageBar = document.getElementById('messageBar');
    if (messageBar) {
        messageBar.style.opacity = '0';
        messageBar.style.transform = 'translateY(-100%)';
        setTimeout(function() {
            messageBar.remove();
        }, 500); // Wait for fade-out and slide-up to complete
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    // Automatically close the message bar after 5 seconds
    setTimeout(closeMessage, 5000);
});