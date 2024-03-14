import {initEmailInput} from "./emailInput.js";
export function initForm(){
    preventFormSubmit();
    initEmailInput();
}
function preventFormSubmit(){
    const form = document.querySelector('form');
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