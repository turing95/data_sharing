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

export function initMessageBar() {
    setTimeout(closeMessage, 5000);

}