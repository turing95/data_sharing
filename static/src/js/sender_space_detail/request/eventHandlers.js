import {createFileTag} from './filesUploadWidget.js'

export let selectedFiles = {}; // Global object to store files for each input

export function handleFilesUpload(inputElement) {
    const inputId = inputElement.id; // Unique identifier for the input field
    selectedFiles[inputId] = selectedFiles[inputId] || []; // Initialize array for this input if not already done

    // Retrieve the tag container to add tags
    const parentDiv = inputElement.closest('.request-accordion-body');
    const tagContainer = parentDiv.querySelector('.file-tags-container');
    if (!tagContainer) return;

    // Add title paragraph if not already there
    if (tagContainer.querySelectorAll('.mb-2.text-sm').length === 0) {
        let titleParagraph = document.createElement('p');
        titleParagraph.className = 'mb-2 text-sm';
        titleParagraph.textContent = 'Files ready to be uploaded:';
        tagContainer.appendChild(titleParagraph);
    }

    // Get the current set of filenames for this input
    let currentFileNames = Array.from(tagContainer.querySelectorAll(`.tag-${inputId}`)).map(tag => tag.title);

    // Add new files to the specific input's array and update the UI
    for (let file of inputElement.files) {
        // Check if file is already in the list to avoid duplication
        if (!currentFileNames.includes(file.name)) {
            selectedFiles[inputId].push(file);

            const tag = createFileTag(file.name);
            tag.classList.add(`tag-${inputId}`); // Add a class to identify tags for this input
            tagContainer.appendChild(tag);
        }
    }
}

