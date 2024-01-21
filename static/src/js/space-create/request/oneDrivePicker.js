export function selectOneDriveFolder(liElement,folderName,folderId) {
    let form =liElement.closest('.request-form')
    let selectedInputDisplay = form.querySelector('.one-drive-destination-display');
    let selectedInput = form.querySelector('.one-drive-destination');
    selectedInputDisplay.value = folderName;
    selectedInput.value = folderId;

}