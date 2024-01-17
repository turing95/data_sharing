import {initEmailInput} from "./emailInputWidget.js";
import {initRequestForms,toggleRename,handleTagDropdownChange,addFileTypeTag, toggleFileTypeRestrict } from "./request/index.js";
import { initGooglePicker,handleAuthClick } from './googlePicker.js'
import {toggleDeadlineNotify, setNotificationDatetime, toggleDeadlineSettings} from './eventHandlers.js';

window.toggleRename = toggleRename;
window.toggleFileTypeRestrict= toggleFileTypeRestrict
window.handleTagDropdownChange = handleTagDropdownChange;
window.handleAuthClick = handleAuthClick;
window.addFileTypeTag = addFileTypeTag;
document.addEventListener('DOMContentLoaded', function() {
    initGooglePicker();
    initRequestForms();
    initEmailInput();

    let notifyDeadlineToggle = document.querySelector('#id_notify_deadline');
    if (notifyDeadlineToggle) {
        notifyDeadlineToggle.addEventListener('change', toggleDeadlineNotify);
        toggleDeadlineNotify(notifyDeadlineToggle)
    }

    // Select the inputs
    const deadlineInput = document.getElementById('id_deadline');
    const noticeDaysInput = document.getElementById('id_deadline_notice_days');
    const noticeHoursInput = document.getElementById('id_deadline_notice_hours');

    // Add event listeners
    if (deadlineInput) {
        deadlineInput.addEventListener('change', setNotificationDatetime);
        deadlineInput.addEventListener('change', toggleDeadlineSettings);
        toggleDeadlineSettings(deadlineInput);
    }
    if (noticeDaysInput) {
        noticeDaysInput.addEventListener('change', setNotificationDatetime);
    }
    if (noticeHoursInput) {
        noticeHoursInput.addEventListener('change', setNotificationDatetime);
    }
    


});





