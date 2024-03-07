import {toggleDeadlineNotify, toggleDeadlineSettings} from "./eventHandlers.js";

export function initDeadlineInput(){
    let notifyDeadlineToggle = document.querySelector('#id_notify_deadline');
    if (notifyDeadlineToggle) {
        notifyDeadlineToggle.addEventListener('change', toggleDeadlineNotify);
        toggleDeadlineNotify(notifyDeadlineToggle)
    }

    // Select the inputs
    const deadlineInput = document.getElementById('id_deadline');

    // Add event listeners
    if (deadlineInput) {
        deadlineInput.addEventListener('change', toggleDeadlineSettings);
        toggleDeadlineSettings(deadlineInput);
    }
}
