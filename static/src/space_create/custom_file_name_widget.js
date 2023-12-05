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
    };


    function handleTagDropdownChange(dropdown) {
        const parentDiv = dropdown.closest('.request-form');
        const childDiv= parentDiv.querySelector('.file-naming-formula-class');
        if (!childDiv) return;
            const selectedTag = `{${dropdown.value}}`;
            insertText(childDiv, selectedTag)
            if (selectedTag) {
                this.value = ""; // Reset the dropdown
            }
    }







