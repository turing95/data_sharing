import {toggleAccordion} from "../eventHandlers.js";

export function cleanForm(newForm){
    newForm.querySelectorAll('.error-message .request-suspended').forEach(element => {
        element.remove();
    });
}

function resetDestinationLogo(newForm) {
    let el = newForm.querySelector('.destination-logo');
    let tag = newForm.querySelector('.destination-type').value;
    htmx.ajax('GET', '/destinations/get-logo/?tag=' + tag, {target: el, swap: 'innerHTML'});

}

export function updateElementIdentifiers(newForm, formCount) {
    // Update IDs and names for inputs, selects, textareas, and accordions
    newForm.id = newForm.id.replace(/-\d+/, `-${formCount}`);
    newForm.querySelectorAll('input, select, textarea, [id^="tooltip-"]').forEach(element => {
        if (element.id) {
            // Replace the form number in the ID
            element.id = element.id.replace(/-\d+-/, `-${formCount}-`);
        }
        if (element.name) {
            element.name = element.name.replace(/-\d+-/, `-${formCount}-`);
        }
        if (element.type !== 'checkbox' && element.type !== 'radio') {
            if (!element.id.includes('destination_type') && !element.id.includes('destination_id') && !element.id.includes('destination_display') && !element.id.includes('file_types')) {
                element.value = ''; // Reset value for text inputs, textareas, and selects
            }
        }

    });
    updateTooltip(newForm, formCount);
    updateAccordion(newForm, formCount);
    updateHxAttributes(newForm, formCount);
    updateLabelsForAttribute(newForm, formCount);
}

function updateTooltip(newForm, formCount){
    newForm.querySelectorAll('[id^="tooltip-"]').forEach(element => {
            let newId = element.id.replace(/-\d+-/, `-${formCount}-`);
            element.id = newId;

            // Update the tooltip-target for the corresponding button
            const buttonSelector = `button[data-tooltip-target="${element.id.replace(/-\d+-/, '-0-')}"]`;
            const tooltipButton = newForm.querySelector(buttonSelector);
            if (tooltipButton) {
                tooltipButton.setAttribute('data-tooltip-target', `${newId}`);
            }

            const tooltip = new Tooltip(element, tooltipButton);
    });
}
function updateAccordion(newForm,formCount){
    newForm.querySelectorAll('[id^="accordion-"]').forEach(element => {
            let newId = element.id.replace(/-\d+-/, `-${formCount}-`);
            element.id = newId;
            // Update accordion button target for accordion body
            if (element.id.includes('-open-body')) {
                const buttonSelector = `button[data-accordion-target="#${element.id.replace(/-\d+-/, '-0-')}"]`;
                const accordionButton = newForm.querySelector(buttonSelector);
                if (accordionButton) {
                    accordionButton.setAttribute('data-accordion-target', `#${newId}`);
                    accordionButton.setAttribute('aria-controls', `#${newId}`);
                    accordionButton.addEventListener('click', toggleAccordion);// TODO use flowbite to init the accordion
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
    })
}
function updateHxAttributes(newForm, formCount) {
    newForm.querySelectorAll('[hx-get], [hx-post]').forEach(element => {
        ['hx-get', 'hx-post'].forEach(attributeName => {
            if (element.hasAttribute(attributeName)) {
                const url = new URL(element.getAttribute(attributeName), window.location.origin);
                url.searchParams.set('request_index', formCount);
                element.setAttribute(attributeName, url.toString());
            }
        });
    });
}

function updateLabelsForAttribute(newForm, formCount) {
    newForm.querySelectorAll('label').forEach(label => {
        if (label.htmlFor) {
            label.htmlFor = label.htmlFor.replace(/-\d+-/, `-${formCount}-`);
        }
    });
}

export function setupCloseButton(newForm) {
    const closeButton = newForm.querySelector('.request-close-button');
    if (closeButton) {
        closeButton.classList.remove('invisible');
        ['hx-confirm', 'hx-swap', 'hx-post'].forEach(attr => {
            closeButton.removeAttribute(attr);
        });
        closeButton.addEventListener('click', function () {
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
            totalForms.value = parseInt(totalForms.value) - 1;

        });
    }
}