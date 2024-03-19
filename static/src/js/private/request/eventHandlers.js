export function handleTagDropdownChange(dropdown) {
    const parentDiv = dropdown.closest('form');
    const childDiv= parentDiv.querySelector('.file-naming-formula');
    if (!childDiv) return;
        const selectedTag = `{{${dropdown.value}}}`;
        insertText(childDiv, selectedTag)
        if (selectedTag) {
            dropdown.value = ""; // Reset the dropdown
            dropdown.options[0].disabled = true;
        }
}

function insertText(textInput, selectedValue) {
    let lastCaretPosition = textInput.selectionStart;
    const currentValue = textInput.value;

    if (lastCaretPosition || currentValue.length === 0) {
        textInput.value = currentValue.slice(0, lastCaretPosition) + selectedValue + currentValue.slice(lastCaretPosition);
    } else {
        textInput.value = selectedValue + currentValue;
    }

    textInput.focus(); // Focus back on the text input
    textInput.dispatchEvent(new CustomEvent("change"));

}

export function toggleRename(checkbox) {
    const parentDiv = checkbox.closest('.rename-container');
    const childDiv1= parentDiv.querySelector('.file-name-container');
    if (!childDiv1) return;

    if (checkbox.checked) {
        childDiv1.classList.remove('hidden');
    } else {
        childDiv1.classList.add('hidden');
    }
}


export function toggleDeadlineSettings(elOrEvent) {
    const deadlineEl = elOrEvent.target || elOrEvent;
    const parentDiv = deadlineEl.closest('#deadline-section');
    const childDiv1 = parentDiv.querySelector('.deadline-settings-container');
    if (!childDiv1) return;

    if (isNaN(deadlineEl.value)) {
        childDiv1.classList.remove('hidden');
    } else {
        childDiv1.classList.add('hidden');
    }
}

export function toggleDeadlineNotify(checkboxOrEvent) {
    const checkbox = checkboxOrEvent.target || checkboxOrEvent;
    const parentDiv = checkbox.closest('#deadline-section');
    const childDiv1 = parentDiv.querySelector('.deadline-notice-container');
    if (!childDiv1) return;

    if (checkbox.checked) {
        childDiv1.classList.remove('hidden');
    } else {
        childDiv1.classList.add('hidden');
    }
}