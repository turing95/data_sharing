export function selectFolder(liElement,folderName,folderId,destinationType) {
    let form =liElement.closest('.request-form')
    let selectedInputDisplay = form.querySelector('.destination-display');
    let selectedInput = form.querySelector('.destination');
    let selectedDestinationTypeInput = form.querySelector('.destination-type');
        selectedInputDisplay.value = folderName;
        
        form.dispatchEvent(new Event("selectedFolder"));

        document.dispatchEvent(new Event("initSearch"));
        selectedInput.value = folderId;
        selectedDestinationTypeInput.value = destinationType;

    }
