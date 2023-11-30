document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    let isPublicCheckbox = document.getElementById('id_is_public');
    let sendersInputs = document.getElementsByClassName('senders-input');


    if (!isPublicCheckbox || !sendersInputs) return;

    // Initial toggle for participants input
    toggleSendersInput(isPublicCheckbox, sendersInputs);

    // Change event for the public checkbox
    isPublicCheckbox.addEventListener('change', () => toggleSendersInput(isPublicCheckbox, sendersInputs));

    // Click event for adding new request forms
    let addButton = document.getElementById('add-request-btn');
    if (addButton) {
        addButton.addEventListener('click', addNewRequestForm);
    }
}

function toggleSendersInput(checkbox, divs) {
    for (let div of divs) {
        if (checkbox.checked) {
            div.classList.add('hidden');
        } else {
            div.classList.remove('hidden');
        }
    }
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
    let templateForm = document.querySelector('.request-form');
    if (!templateForm) {
        console.error('Request form template not found!');
        return null;
    }

    let newForm = templateForm.cloneNode(true);

    // Update IDs and names for inputs, and reset their values
    newForm.querySelectorAll('input, select, textarea').forEach(element => {
        element.id = element.id.replace(/-\d+-/, `-${formCount}-`);
        element.name = element.name.replace(/-\d+-/, `-${formCount}-`);
        if (element.type !== 'checkbox' && element.type !== 'radio') {
            element.value = ''; // Reset value for text inputs, textareas, and selects
        }
    });

    // Update 'for' attribute of labels
    newForm.querySelectorAll('label').forEach(label => {
        if (label.htmlFor) {
            label.htmlFor = label.htmlFor.replace(/-\d+-/, `-${formCount}-`);
        }
    });

    // Remove any unwanted elements (like error messages) from the cloned form
    // newForm.querySelectorAll('.error-message').forEach(msg => msg.remove());

    // Reinitialize event listeners or plugins here, if necessary

    // Add remove button
    let removeBtn = createRemoveButton();
    newForm.appendChild(removeBtn);

    return newForm;
}
function createRemoveButton() {
    let removeBtn = document.createElement('button');
    removeBtn.type = 'button';
    removeBtn.textContent = 'Remove';
    removeBtn.className = 'remove-btn-styles'; // Add your button styles here
    removeBtn.addEventListener('click', function() {
        this.parentNode.remove();
        let totalForms = document.getElementById('id_requests-TOTAL_FORMS');
        if (totalForms) {
            totalForms.value = parseInt(totalForms.value) - 1;
        }
    });

    return removeBtn;
}

function renameToggle(checkbox) {
    const parentDiv = checkbox.closest('.request-form');
    const childDiv = parentDiv.querySelector('.file-name-input');
    if (!childDiv) return;

    if (checkbox.checked) {
        childDiv.classList.remove('hidden');
    } else {
        childDiv.classList.add('hidden');
    }
}