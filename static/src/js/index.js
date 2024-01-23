import {initMessageBar} from "./utils/messageBar.js";
import { initSubmitButtons } from './utils/submitButton.js';
import { initNav } from './utils/navbar.js';
import {initHtmxModal} from "./utils/htmxModal.js";
import {handleSenderUpdated} from "./summary/index.js";

document.addEventListener('DOMContentLoaded', function() {
        initSubmitButtons();
        initMessageBar();
        initNav();
});

document.addEventListener('htmx:afterRequest', function(evt) {
        initMessageBar();
        handleSenderUpdated(evt);
});

document.body.addEventListener('htmx:afterSwap', function(evt) {

        if (evt.target.id.startsWith('htmx-modal')) {
            const modalElement = evt.target.children[0];
            if (modalElement) {
                initHtmxModal(modalElement);
            }
        }

    if (evt.detail.elt.classList.contains('sender-pull')) {
            const senderUuid = evt.detail.elt.getAttribute('sender-uuid')

            const infoEl = document.getElementById('sender-info-container'+senderUuid);
            htmx.process(infoEl);

            const senderRowEl = document.getElementById("sender-row-container-"+senderUuid);
            htmx.process(senderRowEl);
    }
});
