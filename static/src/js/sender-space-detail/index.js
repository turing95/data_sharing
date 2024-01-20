
import {initUploadRequestForms, handleFilesUpload} from "./request/index.js";

window.handleFilesUpload = handleFilesUpload
document.addEventListener('DOMContentLoaded', function() {
    initUploadRequestForms();
});