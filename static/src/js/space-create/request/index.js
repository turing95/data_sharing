import {toggleAccordion, toggleRename, toggleFileTypeRestrict} from './eventHandlers.js';
import {initializeFileTypes, setupFileTypeCloseButton} from './fileTypeInput.js';
export {handleTagDropdownChange,toggleRename, toggleFileTypeRestrict} from './eventHandlers.js';
export {addFileTypeTag,initializeFileTypes} from './fileTypeInput.js';
export {selectFolder}  from './folderPicker.js'



export function initRequestForms() {
    // Click event for adding new request forms
    let addButton = document.getElementById('add-request-btn');
    if (addButton) {
        addButton.addEventListener('click', addNewRequestForm);
    }

    document.querySelectorAll('[id^="id_requests-"][id$="-rename"]').forEach(element => {
        if (/^id_requests-\d+-rename$/.test(element.id)) {
            toggleRename(element);
        }
    });
    document.querySelectorAll('.request-form').forEach(form=>{
        initializeFileTypes(form);
    });

    const fileTypePattern = /^id_requests-\d+-file_type_restrict$/;
    document.querySelectorAll('[id^="id_requests-"][id$="-file_type_restrict"]').forEach(element => {
        if (fileTypePattern.test(element.id)) {
            toggleFileTypeRestrict(element);
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
        document.dispatchEvent(new Event("initSearch"));
        setupFileTypeCloseButton(newForm);
        

    }

}

function cloneRequestForm(formCount) {
    const templateForm = document.querySelector('.request-form');
    if (!templateForm) {
        console.error('Request form template not found!');
        return null;
    }

    const newForm = templateForm.cloneNode(true);
    cleanErrors(newForm);
    updateElementIdentifiers(newForm, formCount);
    setupCloseButton(newForm);
    htmx.process(newForm);
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


                const tooltip = new Tooltip(element, tooltipButton);
            }

        }
        if (element.name) {
            element.name = element.name.replace(/-\d+-/, `-${formCount}-`);
        }
        if (element.type !== 'checkbox' && element.type !== 'radio') {
            if (!element.id.includes('-google_destination_display') && !element.id.includes('-google_destination') && !element.id.includes('file_types')) {
                element.value = ''; // Reset value for text inputs, textareas, and selects
            }
        }
        if (element.id.startsWith('id_search-file-types')){
            element.setAttribute('hx-params', element.name)

            }

    });


    // New logic to update hx-get and hx-post attributes
    newForm.querySelectorAll('[hx-get], [hx-post]').forEach(element => {
        // For hx-get
        if (element.hasAttribute('hx-get')) {
            let hxGetUrl = new URL(element.getAttribute('hx-get'), window.location.origin);
            hxGetUrl.searchParams.set('request_index', formCount);
            element.setAttribute('hx-get', hxGetUrl.toString());
        }

        // For hx-post
        if (element.hasAttribute('hx-post')) {
            let hxPostUrl = new URL(element.getAttribute('hx-post'), window.location.origin);
            hxPostUrl.searchParams.set('request_index', formCount);
            element.setAttribute('hx-post', hxPostUrl.toString());
        }
    });
    // Update hx-get and hx-post attributes
    updateHxAttributes(newForm, formCount);
    // Update labels
    updateLabelsForAttribute(newForm, formCount);
}

function updateHxAttributes(newForm, formCount) {
    newForm.querySelectorAll('[hx-get], [hx-post]').forEach(element => {
        if (element.hasAttribute('hx-get')) {
            updateHxAttribute(element, 'hx-get', formCount);
        }
        if (element.hasAttribute('hx-post')) {
            updateHxAttribute(element, 'hx-post', formCount);
        }
    });
}

function updateHxAttribute(element, attributeName, formCount) {
    const url = new URL(element.getAttribute(attributeName), window.location.origin);
    url.searchParams.set('request_index', formCount);
    element.setAttribute(attributeName, url.toString());
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

function cleanErrors(newForm) {
    //remove errors from the new form
    newForm.querySelectorAll('.error-message').forEach(errorEl => {
        errorEl.remove();
    });
}






