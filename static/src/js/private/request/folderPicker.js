export function selectFolder(liElement,folderName,folderId,destinationType,sharePointSiteId) {
    // get the closest element with class input-request-detail-container
    let inputRequestDetailContainer = liElement.closest('.input-request-detail-container');
    let selectedInputDisplay = inputRequestDetailContainer.querySelector('.destination-display');
    let selectedInput = inputRequestDetailContainer.querySelector('.destination');
    let selectedDestinationTypeInput = inputRequestDetailContainer.querySelector('.destination-type');
    let selectedSharePointSite = inputRequestDetailContainer.querySelector('.sharepoint-site');

    selectedInputDisplay.value = folderName;
    selectedInput.value = folderId;
    selectedDestinationTypeInput.value = destinationType;
    selectedSharePointSite.value = sharePointSiteId;


    // clear search results
    inputRequestDetailContainer.querySelector('.search-results').innerHTML = '';
    inputRequestDetailContainer.querySelector('.search-input').value = '';
    selectedDestinationTypeInput.dispatchEvent(new CustomEvent("change"));
    selectedInput.dispatchEvent(new CustomEvent("change"));


    }
