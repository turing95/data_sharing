import {handleFilesUpload} from "./request/index.js";


document.addEventListener('DOMContentLoaded', function() {
    // Attach the change event listener to all file input elements
    document.querySelectorAll('input[type="file"]').forEach(function(input) {
            input.addEventListener('change', function() {
        handleFilesUpload(this);
    });
    });
});
