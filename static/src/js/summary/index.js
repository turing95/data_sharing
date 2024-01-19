import {initModal} from "./files_modal/index.js";
import {initSenderDropdowns} from "./senderActionsDropdown.js";

document.body.addEventListener('htmx:afterSwap', function(event) {

        if (event.target.id.startsWith('modal-')) {
            const modalElement = event.target.children[0]; 
            if (modalElement) {
                initModal(modalElement.id);
            }
        }
});

document.addEventListener('DOMContentLoaded', function() {
    initSenderDropdowns()
});



