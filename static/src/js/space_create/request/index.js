
// style destination
// bottono add request
// fix border accordion
// fix bug checkbox name formula checked but not showing field when error in create page
// chek Maiusc IDs around
// remove error sentinel in create and request
// makemigration
// add allowed files to DB with command from MT in clack

export function initRequestForms() {
    // Click event for adding new request forms
    let addButton = document.getElementById('add-request-btn');
    if (addButton) {
        addButton.addEventListener('click', addNewRequestForm);
    }

    const renamePattern = /^id_requests-\d+-rename$/;
    document.querySelectorAll('[id^="id_requests-"][id$="-rename"]').forEach(element => {
        if (renamePattern.test(element.id)) {
            toggleRename(element);
        }
    });
}

function addNewRequestForm() {
    let totalForms = document.getElementById('id_requests-TOTAL_FORMS');
    if (!totalForms) return;

    let formCount = parseInt(totalForms.value);
    let newForm = cloneRequestForm(formCount);

    if (newForm) {
        document.getElementById('requests-container').appendChild(newForm);
        totalForms.value = formCount + 1;
    }
}

function cloneRequestForm(formCount) {
    const templateForm = document.querySelector('.request-form');
    if (!templateForm) {
        console.error('Request form template not found!');
        return null;
    }

    const newForm = templateForm.cloneNode(true);

    updateElementIdentifiers(newForm, formCount);
    setupCloseButton(newForm);

    return newForm;
}

function updateElementIdentifiers(newForm, formCount) {
    // Update IDs and names for inputs, selects, textareas, and accordions
    newForm.querySelectorAll('input, select, textarea, div[id^="accordion-open-body-"]').forEach(element => {
        if (element.id) {
            element.id = element.id.replace(/-\d+-/, `-${formCount}-`);
        }
        if (element.name) {
            element.name = element.name.replace(/-\d+-/, `-${formCount}-`);
        }
        if (element.type !== 'checkbox' && element.type !== 'radio') {
            element.value = ''; // Reset value for text inputs, textareas, and selects
        }
        if (element.matches('div[id^="accordion-open-body-"]')) {
            // Additional handling for accordion elements
            updateAccordionButton(newForm, element.id);
        }
    });

    // Update labels
    updateLabelsForAttribute(newForm, formCount);
}

function updateAccordionButton(newForm, accordionId) {
    const buttonSelector = `button[data-accordion-target="#${accordionId}"]`;
    const accordionButton = newForm.querySelector(buttonSelector);
    if (accordionButton) {
        accordionButton.setAttribute('data-accordion-target', `#${accordionId}`);
        accordionButton.addEventListener('click', toggleAccordion);
    }
}


function toggleAccordion(event) {
    const accordionButton = event.currentTarget;
    const targetId = accordionButton.getAttribute('data-accordion-target');
    const targetElement = document.querySelector(targetId);

    if (targetElement) {
        targetElement.classList.toggle('hidden');
        accordionButton.setAttribute('aria-expanded', String(targetElement.classList.contains('hidden')));
    }
}

function updateLabelsForAttribute(newForm, formCount) {
    newForm.querySelectorAll('label').forEach(label => {
        if (label.htmlFor) {
            label.htmlFor = label.htmlFor.replace(/-\d+-/, `-${formCount}-`);
        }
    });
}

function setupCloseButton(newForm) {
    const closeButton = newForm.querySelector('.request-close-button');
    if (closeButton) {
        closeButton.classList.remove('invisible');
        closeButton.addEventListener('click', function() {
            this.closest('.request-form').remove();
            const totalForms = document.getElementById('id_requests-TOTAL_FORMS');
            if (totalForms) {
                totalForms.value = parseInt(totalForms.value) - 1;
            }
        });
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

// Function to insert text into the corresponding text input
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


export function handleTagDropdownChange(dropdown) {
    const parentDiv = dropdown.closest('.request-form');
    const childDiv= parentDiv.querySelector('.file-naming-formula');
    if (!childDiv) return;
        const selectedTag = `{${dropdown.value}}`;
        insertText(childDiv, selectedTag)
        if (selectedTag) {
            this.value = ""; // Reset the dropdown
        }
}




