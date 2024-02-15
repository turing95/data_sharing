import {initMessageBar} from "./utils/messageBar.js";
import { initSubmitButtons } from './utils/submitButton.js';
import { initNav } from './utils/navbar.js';
import {initHtmxModal} from "./utils/htmxModal.js";
import {handleHtmxError} from "./utils/errors.js";
import { initBetaAccessForm } from "./utils/beta-access-form.js";

document.addEventListener('DOMContentLoaded', function() {
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone; // e.g. "America/New_York"
    document.cookie = "django_timezone=" + timezone + ";path=/;Secure;SameSite=Lax";
    initSubmitButtons();
    initMessageBar();
    initNav();
    initBetaAccessForm();
});

document.addEventListener('htmx:beforeSwap', function(evt) {
    if (evt.detail.target.id.startsWith('htmx-modal')) {
        const modalElement = evt.detail.target.children[0];
        if (modalElement) {
            modalElement.remove();
        }
    }
});

document.body.addEventListener('htmx:afterSwap', function(evt) {

    if (evt.target.id.startsWith('htmx-modal')) {
        const modalElement = evt.target.children[0];
        if (modalElement) {
            initHtmxModal(modalElement);
        }
    }
});


document.body.addEventListener('htmx:sendError', function(evt) {
    handleHtmxError(evt);

});

document.body.addEventListener('htmx:responseError', function(evt) {
    handleHtmxError(evt);

});