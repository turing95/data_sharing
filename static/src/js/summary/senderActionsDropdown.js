export function initSenderDropdowns() {
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
}

