import {toggleAccordion, toggleRename} from './eventHandlers.js';

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
    newForm.id = newForm.id.replace(/-\d+/, `-${formCount}`);
    newForm.querySelectorAll('input, select, textarea, [id^="accordion-"], [id^="tooltip-"]').forEach(element => {
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

            // New logic for tooltip
            if (element.id.startsWith('tooltip-')) {
                const newId = element.id.replace(/-\d+-/, `-${formCount}-`);
                element.id = newId;

                // Update the tooltip-target for the corresponding button
                const buttonSelector = `button[data-tooltip-target="${element.id.replace(/-\d+-/, '-0-')}"]`;
                const tooltipButton = newForm.querySelector(buttonSelector);
                if (tooltipButton) {
                    tooltipButton.setAttribute('data-tooltip-target', `${newId}`);
                }
                // set the tooltip content element
                const $targetEl = buttonSelector
                // set the element that trigger the tooltip 
                const $triggerEl = tooltipButton
                const tooltip = new Tooltip($targetEl, $triggerEl);
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
        closeButton.removeAttribute('hx-confirm')
        closeButton.removeAttribute('hx-swap')
        closeButton.removeAttribute('hx-post')
        closeButton.addEventListener('click', function() {
            let form = this.closest('.request-form')
            let forms = document.querySelectorAll('.request-form');
            let lastForm = forms[forms.length - 1];
            if (form !== lastForm) {
                    // Extract the form number from the ID of the form being removed
                let formNumber = parseInt(form.id.replace('form-', ''));
                // Update the IDs of the lastForm
                updateElementIdentifiers(lastForm, formNumber);
            }
            form.remove();
            const totalForms = document.getElementById('id_requests-TOTAL_FORMS');
            if (totalForms) {
                totalForms.value = parseInt(totalForms.value) - 1;
            }
        });
    }
}
function check_delete(form){
    let checkboxElement = form.querySelector('input[id^="id_requests-"][id$="-DELETE"]');

    if (checkboxElement) {
        // Checkbox found, you can now manipulate it
        checkboxElement.checked = true;
    } else {
        // No checkbox found with the given pattern
        console.log("No checkbox found with the given pattern");
    }
}







