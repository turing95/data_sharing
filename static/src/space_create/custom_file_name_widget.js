document.addEventListener('DOMContentLoaded', function () {
    attachDropdownListeners();

    // Function to attach event listeners to each dropdown
    function attachDropdownListeners() {
        const dropdowns = document.querySelectorAll('[id^="id_requests-"][id$="-available_tags_dropdown"]');
        const textInputs = document.querySelectorAll('[id^="id_requests-"][id$="-file_naming_formula"]');

        dropdowns.forEach((dropdown, index) => {
            const textInput = textInputs[index];
            if (textInput && !dropdown.hasListenerAttached) {
                addDropdownListener(dropdown, textInput);
                dropdown.hasListenerAttached = true; // Mark the dropdown as having an event listener
            }
        });
    }

    // Function to add event listeners to each dropdown
    function addDropdownListener(dropdown, textInput) {
        dropdown.addEventListener('change', function () {
            const selectedTag = `{${this.value}}`;
            insertText(textInput, selectedTag);
            if (selectedTag) {
                this.value = ""; // Reset the dropdown
            }
        });
    }

    // Function to insert text into the corresponding text input
    function insertText(textInput, selectedValue) {
        let lastCaretPosition = textInput.selectionStart;
        const currentValue = textInput.value;

        if (lastCaretPosition || currentValue.length === 0) {
            textInput.value = currentValue.slice(0, lastCaretPosition) + selectedValue + currentValue.slice(lastCaretPosition);
        } else {
            textInput.value = selectedValue + currentValue;
        }

        lastCaretPosition = textInput.selectionStart + selectedValue.length;
        textInput.focus(); // Focus back on the text input
    }

    // Attach this function to the button used to add new requests
    const addButton = document.getElementById('add-request-btn');
    addButton.addEventListener('click', function() {
        // Assuming new requests are added here...
        // After adding new requests, reattach event listeners
        setTimeout(attachDropdownListeners, 0); // Timeout ensures DOM updates are completed
    });
});


