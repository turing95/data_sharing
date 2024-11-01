import {handleTagDropdownChange, toggleRename} from './eventHandlers.js';
import {selectFolder} from './folderPicker.js'
import {initDeadlineInput} from "./deadlineInput.js";

window.toggleRename = toggleRename;
window.handleTagDropdownChange = handleTagDropdownChange;
window.selectFolder = selectFolder;

export function initRequestForms() {
    document.querySelectorAll('input[id*="-rename"]').forEach(element => {
        toggleRename(element);
    });
    initDeadlineInput();

}

document.addEventListener('DOMContentLoaded', function () {
    initRequestForms();
});


document.body.addEventListener('htmx:afterSwap', function (evt) {
    document.querySelectorAll('input[id*="-rename"]').forEach(element => {
        toggleRename(element);
    });
    initDeadlineInput();
});

document.addEventListener('htmx:afterRequest', function (evt) {
    if (evt.detail.successful && evt.detail.xhr.status === 200) {
        let trgEvent = evt.detail.requestConfig.triggeringEvent;
        if (trgEvent && trgEvent.srcElement && trgEvent.srcElement.classList.contains('select-destination-type')) {
            let srcElement = trgEvent.srcElement;
            let form = srcElement.closest('form');
            let destinationType = srcElement.options[srcElement.selectedIndex].value;
            if (destinationType === 'kezyy') {
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






