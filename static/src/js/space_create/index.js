import {initEmailInput} from "./emailInputWidget.js";
import {initRequestForms,toggleRename,handleTagDropdownChange } from "./request/index.js";
import { initGooglePicker,handleAuthClick,handleSignoutClick } from './googlePicker.js'

window.toggleRename = toggleRename;
window.handleTagDropdownChange = handleTagDropdownChange;
window.handleAuthClick = handleAuthClick;
window.handleSignoutClick = handleSignoutClick;
document.addEventListener('DOMContentLoaded', function() {
    initGooglePicker();
    initRequestForms();
    initEmailInput();    document.addEventListener('DOMContentLoaded', () => {
    });



});
