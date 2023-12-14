
export function activateLoading(button) {
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
