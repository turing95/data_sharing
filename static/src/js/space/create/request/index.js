import { toggleRename, toggleFileTypeRestrict} from './eventHandlers.js';
import {initializeFileTypes} from './fileTypeInput.js';
import {addNewRequestForm} from './add/addForm.js';
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







