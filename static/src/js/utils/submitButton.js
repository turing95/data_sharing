
function activateLoading(button) {
        const form = button.form; // Assuming the button is within the form
        if (form.checkValidity()) {
            const spinner = button.querySelector('.spinner');
            const buttonTextSpan = button.querySelector('.button-content');
            spinner.classList.remove('hidden');
            buttonTextSpan.classList.add('hidden');
            button.classList.remove('bg-marian-blue-400');
            button.classList.add('bg-marian-blue-300');

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
            if (button.classList.contains('space-delete-alert')) {
                return confirm('Are you sure you want to delete this space?');

            }
            if (button.classList.contains('account-delete-alert')) {
                return confirm('Are you sure you want to delete your account?');

            }
            if (button.classList.contains('requires-loading')) {
            activateLoading(button);
            }
        }
    });
}
