import {initEmailInput} from "./emailInputWidget.js";
import {initRequestForms,toggleRename,handleTagDropdownChange, handleCheckboxChange, toggleFileTypeRestrict } from "./request/index.js";
import { initGooglePicker,handleAuthClick } from './googlePicker.js'

window.toggleRename = toggleRename;
window.toggleFileTypeRestrict= toggleFileTypeRestrict
window.handleCheckboxChange = handleCheckboxChange
window.handleTagDropdownChange = handleTagDropdownChange;
window.handleAuthClick = handleAuthClick;
document.addEventListener('DOMContentLoaded', function() {
    initGooglePicker();
    initRequestForms();
    initEmailInput();



});
