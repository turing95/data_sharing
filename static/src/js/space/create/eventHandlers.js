export function toggleDeadlineSettings(elOrEvent) {
    const deadlineEl = elOrEvent.target || elOrEvent; 
    const parentDiv = deadlineEl.closest('#deadline-section');
    const childDiv1 = parentDiv.querySelector('.deadline-settings-container');
    if (!childDiv1) return;

    if (isNaN(deadlineEl.value)) {
        childDiv1.classList.remove('hidden');
    } else {
        childDiv1.classList.add('hidden');
    }
}

export function toggleDeadlineNotify(checkboxOrEvent) {
    const checkbox = checkboxOrEvent.target || checkboxOrEvent;
    const parentDiv = checkbox.closest('#deadline-section');
    const childDiv1 = parentDiv.querySelector('.deadline-notice-container');
    if (!childDiv1) return;

    if (checkbox.checked) {
        childDiv1.classList.remove('hidden');
    } else {
        childDiv1.classList.add('hidden');
    }
}

export function setNotificationDatetime() {
    // Retrieve values
    const deadlineValue = document.getElementById('id_deadline').value;
    const noticeDays = parseFloat(document.getElementById('id_deadline_notice_days').value);
    const noticeHours = parseFloat(document.getElementById('id_deadline_notice_hours').value);
    const notificationDateContainer = document.getElementById('deadline-notification-date-container')

    // Parse the deadline value into a Date object
    const deadlineDate = new Date(deadlineValue);

    // Check if the deadline date is valid
    if (isNaN(deadlineDate.getTime())) {
        notificationDateContainer.textContent = "Invalid deadline"; // Exit the function if the deadline date is invalid
        notificationDateContainer.classList.remove('underline');
        notificationDateContainer.classList.add('text-red-500','bg-red-100', 'mt-0.5');
        return;
    }
    if (isNaN(noticeDays) || isNaN(noticeHours)) {
        notificationDateContainer.textContent = "Invalid notice days or hours";
        notificationDateContainer.classList.remove('underline');
        notificationDateContainer.classList.add('text-red-500','bg-red-100', 'mt-0.5');
        return;
    }
    notificationDateContainer.classList.remove('text-red-500', 'bg-red-100', 'mt-0.5');
    notificationDateContainer.classList.add('underline');

    // Calculate the notification datetime
    // Subtract days and hours from the deadline
    deadlineDate.setDate(deadlineDate.getDate() - noticeDays);
    deadlineDate.setMinutes(deadlineDate.getMinutes() - noticeHours*60 );

    // Format the date into "YYYY-MM-DD HH:mm"
    const formattedDate = formatDateTime(deadlineDate);

    // Set the calculated datetime in the div
    notificationDateContainer.textContent = formattedDate;
}

function formatDateTime(date) {
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');

    return `On the ${year}-${month}-${day} at ${hours}:${minutes}.`;
}


export function clickOutsideSearch(event) {
    let clickedElement = event.target;

    // Check if the clicked element doesn't meet the criteria
    if (!clickedElement.id.startsWith('id_search-folders')) {

        // Find all elements with the class 'search-results'
        let searchResults = document.querySelectorAll('.search-results');

        // Add the 'hidden' class to each of these elements
        searchResults.forEach(function(element) {
            element.innerHTML = '';
        });
    }
}