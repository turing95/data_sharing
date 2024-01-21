import {initRequestForms,toggleRename,handleTagDropdownChange,addFileTypeTag, toggleFileTypeRestrict,handleAuthClick,selectOneDriveFolder } from "./request/index.js";
import {initForm} from "./form.js";

window.toggleRename = toggleRename;
window.toggleFileTypeRestrict= toggleFileTypeRestrict
window.handleTagDropdownChange = handleTagDropdownChange;
window.handleAuthClick = handleAuthClick;
window.addFileTypeTag = addFileTypeTag;
window.selectOneDriveFolder = selectOneDriveFolder;
document.addEventListener('DOMContentLoaded', function() {
    initForm();
    initRequestForms();
});

//handle enter button behavior
document.addEventListener('DOMContentLoaded', (event) => {
    const form = document.querySelector('#space-form');
    if (form) {
        form.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.target.matches('input:not([type="submit"]):not([type="button"]):not([type="hidden"]):not([class*="email-input"]), select')) {
                e.preventDefault(); // Prevent form submission

                const formInputs = Array.from(form.querySelectorAll('input:not([type="submit"]):not([type="button"]):not([type="hidden"]), select, textarea'));
                const currentIndex = formInputs.indexOf(e.target);

                if (currentIndex !== -1) {
                    let nextIndex = currentIndex + 1;
                    while (nextIndex < formInputs.length) {
                        const nextInput = formInputs[nextIndex];
                        if (!nextInput.disabled) { // add && !nextInput.readOnly to include read only fields
                            nextInput.focus();
                            if (document.activeElement === nextInput) {
                                break; // Focus successfully moved
                            }
                        }
                        nextIndex++;
                    }
                }
            }
        });
    }
});





