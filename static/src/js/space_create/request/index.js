import {toggleAccordion,toggleRename} from './eventHandlers.js';
export {handleTagDropdownChange,toggleRename} from './eventHandlers.js';


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
        document.getElementById('accordion-open').appendChild(newForm);
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
    newForm.querySelectorAll('input, select, textarea, [id^="accordion-"]').forEach(element => {
        if (element.id) {
            // Replace the form number in the ID
            const newId = element.id.replace(/-\d+-/, `-${formCount}-`);
            element.id = newId;

            // Update accordion button target for accordion body
            if (element.id.includes('-open-body')) {
                const buttonSelector = `button[data-accordion-target="#${element.id.replace(/-\d+-/, '-0-')}"]`;
                const accordionButton = newForm.querySelector(buttonSelector);
                if (accordionButton) {
                    accordionButton.setAttribute('data-accordion-target', `#${newId}`);
                    accordionButton.setAttribute('aria-controls', `#${newId}`);
                    accordionButton.addEventListener('click', toggleAccordion);
                }
            }

            // Update aria-labelledby for accordion body
            if (element.id.includes('-open-heading')) {
                const accordionBodySelector = `div[aria-labelledby="${element.id.replace(/-\d+-/, '-0-')}"]`;
                const accordionBody = newForm.querySelector(accordionBodySelector);
                if (accordionBody) {
                    accordionBody.setAttribute('aria-labelledby', newId);
                }
            }
        }
        if (element.name) {
            element.name = element.name.replace(/-\d+-/, `-${formCount}-`);
        }
        if (element.type !== 'checkbox' && element.type !== 'radio') {
            element.value = ''; // Reset value for text inputs, textareas, and selects
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







