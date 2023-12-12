import {initEmailInput} from "./emailInputWidget.js";
import {initRequestForms,toggleRename,handleTagDropdownChange } from "./request/index.js";
import { initGooglePicker,handleAuthClick } from './googlePicker.js'

window.toggleRename = toggleRename;
window.handleTagDropdownChange = handleTagDropdownChange;
window.handleAuthClick = handleAuthClick;
document.addEventListener('DOMContentLoaded', function() {
    initGooglePicker();
    initRequestForms();
    initEmailInput();



});
