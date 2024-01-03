export function handleTagDropdownChange(dropdown) {
    const parentDiv = dropdown.closest('.request-form');
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
}

export function toggleFileTypeRestrict(checkbox){
    const parentDiv = checkbox.closest('.request-form');
    const childDiv1= parentDiv.querySelector('.file-type-restriction-container');
    if (!childDiv1) return;

    if (checkbox.checked) {
        childDiv1.classList.remove('hidden');
    } else {
        childDiv1.classList.add('hidden');
    }

}
export function toggleRename(checkbox) {
    const parentDiv = checkbox.closest('.request-form');
    const childDiv1= parentDiv.querySelector('.file-name-container');
    if (!childDiv1) return;

    if (checkbox.checked) {
        childDiv1.classList.remove('hidden');
    } else {
        childDiv1.classList.add('hidden');
    }
}

export function toggleAccordion(event) {
    const accordionButton = event.currentTarget;
    const targetId = accordionButton.getAttribute('data-accordion-target');
    const targetElement = document.querySelector(targetId);

    if (targetElement) {
        targetElement.classList.toggle('hidden');
        accordionButton.setAttribute('aria-expanded', String(targetElement.classList.contains('hidden')));
    }
}

export function handleCheckboxChange(checkbox) {
    // Determine if this is a group checkbox or a sub-checkbox
    const isGroupCheckbox = checkbox.classList.contains('group-checkbox');
    const groupId = checkbox.dataset.groupId; // Assuming you set a data-group-id attribute on group checkboxes

    if (isGroupCheckbox) {
        // If this is a group checkbox, find all related sub-checkboxes
        document.querySelectorAll(`input[data-group-id="${groupId}"]`).forEach(subCheckbox => {
            subCheckbox.checked = checkbox.checked;
        });
    } else {
        // If this is a sub-checkbox, find the parent group checkbox
        const groupCheckbox = document.querySelector(`input.group-checkbox[data-group-id="${groupId}"]`);
        if (!groupCheckbox) return;

        const subCheckboxes = document.querySelectorAll(`input[data-group-id="${groupId}"]:not(.group-checkbox)`);
        const allChecked = Array.from(subCheckboxes).every(subCheckbox => subCheckbox.checked);

        if (checkbox.checked) {
            // If all sub-checkboxes are now checked, check the group checkbox
            groupCheckbox.checked = allChecked;
        } else {
            // If any sub-checkbox is unchecked, uncheck the group checkbox
            groupCheckbox.checked = false;
        }
    }
}
