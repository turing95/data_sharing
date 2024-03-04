import {initForm} from "./form.js";
import {hideShowSearch} from "./eventHandlers.js";
import {processInputText} from "./emailInput.js";
import {selectCompany} from "./companyInput.js";

window.processInputText = processInputText;
window.selectCompany = selectCompany;
document.addEventListener('DOMContentLoaded', function () {
    initForm();
});
document.addEventListener('click', function (event) {
    hideShowSearch(event);

});

document.addEventListener('htmx:afterRequest', function (evt) {
    if (evt.detail.successful && evt.detail.xhr.status === 200) {
        if (evt.target.id === 'create-contact-form'){
            const modal = FlowbiteInstances.getInstance('Modal', document.getElementById('htmx-modal').children[0].id);
            modal.hide();
        }
    }

});




