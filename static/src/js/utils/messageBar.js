
function closeMessage() {
    let messageBar = document.getElementById('django-messages');

    if (messageBar) {
        messageBar.style.opacity = '0';
        messageBar.style.transform = 'translateY(-100%)';
        setTimeout(function() {
            messageBar.remove();
        }, 500); // Wait for fade-out and slide-up to complete
    }

}

export function initMessageBar() {
    let messageBar = document.getElementById('django-messages');
    if (!messageBar) {
        return;
    }
    messageBar.querySelectorAll('[role="alert"]').forEach(element => {
        new Dismiss(element, element.querySelector('button'));
    });
    setTimeout(closeMessage, 5000);

}