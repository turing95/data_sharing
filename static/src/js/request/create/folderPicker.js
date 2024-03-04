export function selectFolder(liElement,folderName,folderId,destinationType,sharePointSiteId) {
    let form =liElement.closest('form')
    let selectedInputDisplay = form.querySelector('.destination-display');
    let selectedInput = form.querySelector('.destination');
    let selectedDestinationTypeInput = form.querySelector('.destination-type');
    let selectedSharePointSite = form.querySelector('.sharepoint-site');

    selectedInputDisplay.value = folderName;
    selectedInput.value = folderId;
    selectedDestinationTypeInput.value = destinationType;
    selectedSharePointSite.value = sharePointSiteId;


    // clear search results
    form.querySelector('.search-results').innerHTML = '';
    form.querySelector('.search-input').value = '';
    selectedDestinationTypeInput.dispatchEvent(new CustomEvent("change"));


    }
