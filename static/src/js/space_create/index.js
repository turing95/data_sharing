import {initEmailInput} from "./emailInputWidget.js";
import {initRequestForms,toggleRename,handleTagDropdownChange } from "./request/index.js";
window.toggleRename = toggleRename;
window.handleTagDropdownChange = handleTagDropdownChange;

document.addEventListener('DOMContentLoaded', function() {
    initRequestForms();
    initEmailInput();


});
