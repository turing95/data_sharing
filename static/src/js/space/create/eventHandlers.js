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


export function hideShowSearch(event) {
    let clickedElement = event.target;

    // Check if the clicked element doesn't meet the criteria
    if (!clickedElement.id.startsWith('id_search')) {

        // Find all elements with the class 'search-results'
        let searchResults = document.querySelectorAll('.search-results');

        // Add the 'hidden' class to each of these elements
        searchResults.forEach(function(element) {
            element.classList.add('hidden');
        });
    }else{
        //show only search results next to element
        let form = clickedElement.closest('form')
        if(form) {
            let searchResults = form.querySelector('.search-results');
            searchResults.classList.remove('hidden');
        }else{
            let searchResults = clickedElement.closest('.search-container').querySelector('.search-results');
            searchResults.classList.remove('hidden');
        }
        

    }
}