import {initMessageBar} from "./utils/messageBar.js";
import { initSubmitButtons } from './utils/submitButton.js';
import { initNav } from './utils/navbar.js';
import {initHtmxModal} from "./utils/htmxModal.js";
import {handleHtmxError} from "./utils/errors.js";
import {preventEnter} from "./utils/forms.js";
import {initLanguageForm} from "./utils/forms.js";

document.addEventListener('DOMContentLoaded', function() {
    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone; // e.g. "America/New_York"
    document.cookie = "django_timezone=" + timezone + ";path=/;Secure;SameSite=Lax";
    initSubmitButtons();
    initMessageBar();
    initNav();
    preventEnter();
});
document.addEventListener('htmx:afterRequest', function(evt) {
    initMessageBar();
});
document.body.addEventListener('htmx:afterSwap', function(evt) {
    initFlowbite();
    preventEnter();
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


document.addEventListener('htmx:afterSettle', function(evt) {
    initLanguageForm();
});