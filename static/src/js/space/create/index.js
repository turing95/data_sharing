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
    if (evt.detail.successful && evt.detail.xhr.status === 201) {
        if (evt.target.id === 'create-contact-form')
            document.getElementById('htmx-modal').children[0].querySelector('[data-modal-hide]').click();
    }

});




