document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});

function initializeEventListeners() {
    let isPublicCheckbox = getElement('id_is_public');
    let participantsDiv = getElement('participants-input');

    if (!isPublicCheckbox || !participantsDiv) return;

    // Initial toggle for participants input
    toggleParticipantsInput(isPublicCheckbox, participantsDiv);

    // Change event for the public checkbox
    isPublicCheckbox.addEventListener('change', () => toggleParticipantsInput(isPublicCheckbox, participantsDiv));

    // Click event for adding new request forms
    let addButton = getElement('add-request-btn');
    if (addButton) {
        addButton.addEventListener('click', addNewRequestForm);
    }
}

function getElement(id) {
    let element = document.getElementById(id);
    if (!element) {
        console.error(`Element with id ${id} not found!`);
    }
    return element;
}

function toggleParticipantsInput(checkbox, div) {
    div.style.display = checkbox.checked ? 'none' : 'block';
}

function addNewRequestForm() {
    let totalForms = getElement('id_requests-TOTAL_FORMS');
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
        let totalForms = getElement('id_requests-TOTAL_FORMS');
        if (totalForms) {
            totalForms.value = parseInt(totalForms.value) - 1;
        }
    });

    return removeBtn;
}

