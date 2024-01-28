export function selectFolder(liElement,folderName,folderId,destinationType) {
    let form =liElement.closest('.request-form')
    let selectedInputDisplay = form.querySelector('.destination-display');
    let selectedInput = form.querySelector('.destination');
    let selectedDestinationTypeInput = form.querySelector('.destination-type');
    
    selectedInputDisplay.value = folderName;
    selectedInput.value = folderId;
    selectedDestinationTypeInput.value = destinationType;


    // clear search results
    form.querySelector('.search-results').innerHTML = '';
    form.querySelector('.search-input').value = '';


    }
