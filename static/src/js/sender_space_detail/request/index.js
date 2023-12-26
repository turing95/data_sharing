import {handleFilesUpload} from './eventHandlers.js';
import { selectedFiles } from './eventHandlers.js';
export {handleFilesUpload} from './eventHandlers.js';


export function initUploadRequestForms() {
    // does nothing
}

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload_form'); // Replace with your form's ID
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        let formData = new FormData(this);

        // Example of appending files to FormData
        Object.keys(selectedFiles).forEach(inputId => {
            selectedFiles[inputId].forEach(file => {
                formData.append(inputId, file); // inputId matches the format like 'id_form-2-files'
            });
        });
        

        // Use HTMX to send the FormData
        htmx.ajax('POST', this.action, formData, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': this.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
    });
});


