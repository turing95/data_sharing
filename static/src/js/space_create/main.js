import {initializeEventListeners as initEmailListeners} from "./email_input_widget.js";
import {gapiLoaded,gisLoaded,handleAuthClick,handleSignoutClick} from "./google_picker.js";
import {toggleRename,handleTagDropdownChange, initializeEventListeners as initRequestListeners} from "./request_form.js";
window.toggleRename = toggleRename;
window.handleTagDropdownChange = handleTagDropdownChange;
window.gapiLoaded = gapiLoaded;
window.gisLoaded = gisLoaded;
window.handleAuthClick = handleAuthClick;
window.handleSignoutClick = handleSignoutClick;

document.addEventListener('DOMContentLoaded', function() {
    initRequestListeners();
    initEmailListeners();


});
