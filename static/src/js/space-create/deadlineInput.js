import {setNotificationDatetime, toggleDeadlineNotify, toggleDeadlineSettings} from "./eventHandlers.js";

export function initDeadlineInput(){
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

}
