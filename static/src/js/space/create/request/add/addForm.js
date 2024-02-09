import {setupFileTypeCloseButton} from "../fileTypeInput.js";
import {cleanForm, setupCloseButton, updateElementIdentifiers} from "./utils.js";

export function addNewRequestForm() {

    let totalForms = document.getElementById('id_requests-TOTAL_FORMS');
    if (!totalForms) return;

    let newForm = cloneRequestForm();
    let formCount = parseInt(totalForms.value);
    prepareNewForm(newForm, formCount);
    postProcessNewForm(newForm, formCount, totalForms);


}

function cloneRequestForm() {
    const templateForm = document.querySelector('.request-form');
    if (!templateForm) {
        console.error('Request form template not found!');
        return null;
    }

    return templateForm.cloneNode(true);
}
function prepareNewForm(newForm, formCount) {
    cleanForm(newForm);
    updateElementIdentifiers(newForm, formCount);
    setupCloseButton(newForm);
    htmx.process(newForm);
}

function postProcessNewForm(newForm, formCount, totalForms){
        if (newForm) {
        document.getElementById('accordion-open').appendChild(newForm);
        totalForms.value = formCount + 1;
        document.dispatchEvent(new Event("initRequestForm"));
        setupFileTypeCloseButton(newForm);

    }
}



