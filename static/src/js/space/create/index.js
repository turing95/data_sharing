import {
    initRequestForms,
    toggleRename,
    handleTagDropdownChange,
    addFileTypeTag,
    toggleFileTypeRestrict,
    selectFolder
} from "./request/index.js";
import {initForm} from "./form.js";
import {hideShowSearch} from "./eventHandlers.js";
import {processInputText} from "./emailInputWidget.js";

window.toggleRename = toggleRename;
window.toggleFileTypeRestrict = toggleFileTypeRestrict
window.handleTagDropdownChange = handleTagDropdownChange;
window.addFileTypeTag = addFileTypeTag;
window.selectFolder = selectFolder;
window.processInputText = processInputText;
document.addEventListener('DOMContentLoaded', function () {
    initForm();
    initRequestForms();
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
        let trgEvent = evt.detail.requestConfig.triggeringEvent;
        if (trgEvent && trgEvent.srcElement && trgEvent.srcElement.classList.contains('select-destination-type')){
            let srcElement = trgEvent.srcElement;
            let form = srcElement.closest('.request-form');
            let destinationType = srcElement.options[srcElement.selectedIndex].value;
            if(destinationType === 'kezyy'){
                let destinationTypeInput = form.querySelector('.destination-type');
                let selectedInput = form.querySelector('.destination');
                let selectedInputDisplay = form.querySelector('.destination-display');
                destinationTypeInput.value = destinationType;
                selectedInputDisplay.value = 'Kezyy'
                selectedInput.value = ''
                destinationTypeInput.dispatchEvent(new CustomEvent("change"));
            }

        }
    }

});




