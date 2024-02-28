function activateLoading(button) {

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

export function initSubmitButtons() {
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach((button) => {
        let form = button.closest('form')
        if (!form) {
            return;
        }
        if (button.classList.contains('requires-loading')) {
            form.onsubmit = function () {
                activateLoading(button);
            }
        }

    });
}
