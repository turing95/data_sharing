export function initBetaAccessForm() {
    // get all element with id starting with beta-access-form-button
    const showFormButtons = document.querySelectorAll('[id^="beta-access-form-button"]')
    if (showFormButtons) {
        showFormButtons.forEach(function(button) {
            button.addEventListener('click', function(event) {
                const formContainer = document.getElementById('beta-access-form-container');
                const introContainer = document.getElementById('beta-access-intro');

                if (formContainer && introContainer) {
                    formContainer.classList.toggle('hidden');
                    introContainer.classList.toggle('hidden');
                }
            })
        })
    }
}