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

//handle enter button behavior
document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.querySelector('#space-form');
    if (form) {
        form.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.target.matches('input:not([type="submit"]):not([type="button"]):not([type="hidden"]), select, textarea')) {
                e.preventDefault(); // Prevent form submission

                const formInputs = Array.from(form.querySelectorAll('input:not([type="submit"]):not([type="button"]):not([type="hidden"]), select, textarea'));
                const currentIndex = formInputs.indexOf(e.target);

                if (currentIndex !== -1) {
                    let nextIndex = currentIndex + 1;
                    while (nextIndex < formInputs.length) {
                        const nextInput = formInputs[nextIndex];
                        if (!nextInput.disabled) { // add && !nextInput.readOnly to include read only fields
                            nextInput.focus();
                            if (document.activeElement === nextInput) {
                                break; // Focus successfully moved
                            }
                        }
                        nextIndex++;
                    }
                }
            }
        });
    }
});





