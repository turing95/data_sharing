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
    let currentOpenDropdown = null;
    const scrollableContainer = document.getElementById('scrollable-table-container');

    elements.forEach((element) => {
        element.addEventListener('click', () => {
            // Close the currently open dropdown, if any
            if (currentOpenDropdown && currentOpenDropdown !== element) {
                scrollableContainer.classList.remove('overflow-visible');
                scrollableContainer.classList.add('overflow-x-auto');
            }

            // Toggle the clicked dropdown
            if (currentOpenDropdown !== element) {
                // Open the clicked dropdown
                scrollableContainer.classList.add('overflow-visible');
                scrollableContainer.classList.remove('overflow-x-auto');
                currentOpenDropdown = element; // Update the currently open dropdown
            } else {
                // Close the clicked dropdown
                scrollableContainer.classList.remove('overflow-visible');
                scrollableContainer.classList.add('overflow-x-auto');
                currentOpenDropdown = null;
            }
        });
    });

    document.addEventListener('click', (event) => {
        // Check if the click is outside the current open dropdown
        if (currentOpenDropdown && !currentOpenDropdown.contains(event.target)) {
            // Close the dropdown
            scrollableContainer.classList.remove('overflow-visible');
            scrollableContainer.classList.add('overflow-x-auto');
            currentOpenDropdown = null;
        }
    });
});
