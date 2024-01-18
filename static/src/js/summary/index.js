import {initModal} from "./files_modal/index.js";

document.body.addEventListener('htmx:afterSwap', function(event) {

        if (event.target.id.startsWith('modal-')) {
            const modalElement = event.target.children[0]; 
            if (modalElement) {
                initModal(modalElement.id);
            }
        }
});


document.addEventListener('DOMContentLoaded', () => {
    const elements = document.querySelectorAll('[id^="sender_actions_dropdown_button"]');

    elements.forEach((element, index) => {
        element.addEventListener('click', () => {
            // Constructing the ID for initModal function
            const modalId = `sender_actions_dropdown_${index}`;
            initModal2(modalId);
        });
    });
});

function initModal2(id) {
    const modalElement = document.getElementById(id);
    if (!modalElement) {
        console.error('Modal element not found');
        return;
    }
    const modal = new Modal(modalElement, {
        onHide: () => {
            modalElement.remove();
        },
        backdropClasses:
        'fixed inset-0 z-[5]',
    });

    // show the modal upon initialization
    modal.show();
}