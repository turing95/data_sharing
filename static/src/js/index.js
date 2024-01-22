import {initMessageBar} from "./utils/messageBar.js";
import { initSubmitButtons } from './utils/submitButton.js';
import { initNav } from './utils/navbar.js';
import {initHtmxModal} from "./utils/htmxModal.js";

document.addEventListener('DOMContentLoaded', function() {
        initSubmitButtons();
        initMessageBar();
        initNav();
});

document.addEventListener('htmx:afterRequest', function(evt) {
        initMessageBar();

        if (evt.detail.elt.classList.contains('sender-updating')) {
            const senderUuid = evt.detail.elt.getAttribute('sender-uuid')
            document.dispatchEvent(new Event("senderUpdated"));
            const eventName = "senderUpdated-" + senderUuid;
            document.dispatchEvent(new Event(eventName));

        }



});

document.body.addEventListener('htmx:afterSwap', function(event) {

        if (event.target.id.startsWith('htmx-modal')) {
            const modalElement = event.target.children[0]; 
            if (modalElement) {
                initHtmxModal(modalElement);
            }
        }
});
