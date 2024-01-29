document.addEventListener('htmx:afterRequest', function(evt) {
    if (evt.detail.successful) {
        handleSenderUpdated(evt);
    }
});

document.body.addEventListener('htmx:afterSettle', function(evt) {
    let trgElement = evt.target;
    if (evt.detail.successful) {
        if (trgElement.classList.contains('sender-pull')) {
            let senderUuid = trgElement.getAttribute('sender-uuid')

            let infoEl = document.getElementById('sender-info-container-' + senderUuid);
            if (infoEl) htmx.process(infoEl);//modal might  not be int the DOM!

            let senderRowEl = document.getElementById("sender-row-container-" + senderUuid);
            htmx.process(senderRowEl);
        }
    }
});

function handleSenderUpdated(evt) {
    let srcElement = evt.detail.requestConfig.triggeringEvent.srcElement;
    if (srcElement.classList && srcElement.classList.contains('sender-push')) {
        const senderUuid = srcElement.getAttribute('sender-uuid')
        const eventName = "senderUpdated-" + senderUuid;
        document.dispatchEvent(new Event(eventName));
    }


}