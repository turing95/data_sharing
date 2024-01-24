

export function initSelectedFoldersLogo() {

    // Select elements with IDs matching the pattern 'id_requests-{number}-destination_type_select'
    document.querySelectorAll('.destination-selected-folder-logo').forEach(element => {
        // get the children with the class google-image, onedrive-image, and std-image
        let form =element.closest('.request-form')
        let selectedDestinationTypeInput = form.querySelector('.destination-type');
        selectedDestinationTypeInput.value
         // set provider folder
        if (selectedDestinationTypeInput.value === 'GOOGLE_DRIVE') {
        form.querySelector('.google-image').classList.remove('hidden');
        form.querySelector('.onedrive-image').classList.add('hidden');
        form.querySelector('.std-image').classList.add('hidden');
        } else if (selectedDestinationTypeInput.value === 'ONE_DRIVE') {
        form.querySelector('.google-image').classList.add('hidden');
        form.querySelector('.onedrive-image').classList.remove('hidden');
        form.querySelector('.std-image').classList.add('hidden');
        } else {
        form.querySelector('.google-image').classList.add('hidden');
        form.querySelector('.onedrive-image').classList.add('hidden');
        form.querySelector('.std-image').classList.remove('hidden');
        }
    });
}
