import {initEmailInput} from "./emailInputWidget.js";
import {initRequestForms } from "./request/index.js";
import {toggleRename,handleTagDropdownChange } from "./request/eventHandlers.js";
window.toggleRename = toggleRename;
window.handleTagDropdownChange = handleTagDropdownChange;

document.addEventListener('DOMContentLoaded', function() {
    initRequestForms();
    initEmailInput();


});
