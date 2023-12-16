
function activateLoading(button) {
        const form = button.form; // Assuming the button is within the form
        if (form.checkValidity()) {
            const spinner = button.querySelector('.spinner');
            const buttonTextSpan = button.querySelector('.button-content');
            spinner.classList.remove('hidden');
            buttonTextSpan.classList.add('hidden');
            button.classList.add('bg-marian-blue-700');

            // Allow form submission
            setTimeout(() => {
                button.disabled = true;
            }, 10);
        }
}
export function initSubmitButtons() {
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach((button) => {
        button.onclick = function() {
            if (!button.classList.contains('delete-space-button')) {
            activateLoading(button);

            }else{
                return confirm('Are you sure you want to delete this?');
            }
        }
    });
}
