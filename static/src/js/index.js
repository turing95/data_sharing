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
});

document.body.addEventListener('htmx:afterSwap', function(evt) {

        if (evt.target.id.startsWith('htmx-modal')) {
            const modalElement = evt.target.children[0];
            if (modalElement) {
                initHtmxModal(modalElement);
            }
        }
});
