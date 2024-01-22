export function handleSenderUpdated(evt) {

    if (evt.detail.elt.classList.contains('sender-updating')) {
        const senderUuid = evt.detail.elt.getAttribute('sender-uuid')
        const eventName = "senderUpdated-" + senderUuid;
        document.dispatchEvent(new Event(eventName));

    }

}