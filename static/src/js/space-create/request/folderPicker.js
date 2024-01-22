export function selectFolder(liElement,folderName,folderId) {
    let form =liElement.closest('.request-form')
    let selectedInputDisplay = form.querySelector('.destination-display');
    let selectedInput = form.querySelector('.destination');
    selectedInputDisplay.value = folderName;
    selectedInput.value = folderId;

}