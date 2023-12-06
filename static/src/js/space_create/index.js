import {initEmailInput} from "./email_input_widget.js";
import {toggleRename,handleTagDropdownChange, initRequestForms } from "./request/index.js";
window.toggleRename = toggleRename;
window.handleTagDropdownChange = handleTagDropdownChange;

document.addEventListener('DOMContentLoaded', function() {
    initRequestForms();
    initEmailInput();


});
