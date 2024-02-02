import {initRequestForms,toggleRename,handleTagDropdownChange,addFileTypeTag, toggleFileTypeRestrict,selectFolder } from "./request/index.js";
import {initForm} from "./form.js";
import {hideShowSearch} from "./eventHandlers.js";

window.toggleRename = toggleRename;
window.toggleFileTypeRestrict= toggleFileTypeRestrict
window.handleTagDropdownChange = handleTagDropdownChange;
window.addFileTypeTag = addFileTypeTag;
window.selectFolder = selectFolder;
document.addEventListener('DOMContentLoaded', function() {
    initForm();
    initRequestForms();
});
document.addEventListener('click',function(event) {
    hideShowSearch(event);

});




