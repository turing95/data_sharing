import {initializeEventListeners as initEmailListeners} from "./email_input_widget.js";
import {toggleRename,handleTagDropdownChange, initializeEventListeners as initRequestListeners} from "./request_form.js";
window.toggleRename = toggleRename;
window.handleTagDropdownChange = handleTagDropdownChange;

document.addEventListener('DOMContentLoaded', function() {
    initRequestListeners();
    initEmailListeners();


});
