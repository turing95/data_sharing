document.addEventListener('htmx:afterRequest', function(evt) {
    let successStates = [200,201, 204];
    if (evt.detail.successful && successStates.includes(evt.detail.xhr.status)) {
        handleSenderUpdated(evt);
        handleFilesChanges(evt);
    }
});

document.body.addEventListener('htmx:afterSettle', function(evt) {
    if (evt.detail.successful) {
        initSenderPullElements(evt);
    }
});
document.body.addEventListener('htmxModal:init', function(evt) {
    initAccordions();
});
function handleSenderUpdated(evt) {
    let srcElement = evt.detail.requestConfig.triggeringEvent.srcElement;
    if (srcElement.classList && srcElement.classList.contains('sender-push')) {
        const senderUuid = srcElement.getAttribute('sender-uuid')
        const eventName = "senderUpdated-" + senderUuid;
        document.dispatchEvent(new Event(eventName));
    }


}
function handleFilesChanges(evt) {
    let srcElement = evt.detail.requestConfig.elt;
    if (srcElement.classList && srcElement.classList.contains('files-push')) {
        document.dispatchEvent(new Event('filesUpdated'));
    }
}

function initSenderPullElements(evt) {
    let trgElement = evt.target;
    if (trgElement.classList.contains('sender-pull')) {
        let senderUuid = trgElement.getAttribute('sender-uuid')

        let infoEl = document.getElementById('sender-info-container-' + senderUuid);
        if (infoEl) htmx.process(infoEl);//modal might  not be int the DOM!

        let senderRowEl = document.getElementById("sender-row-container-" + senderUuid);
        htmx.process(senderRowEl);
    }
}