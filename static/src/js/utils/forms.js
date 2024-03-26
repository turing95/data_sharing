export function preventEnter() {
    //prevent submit on all forms when enter is pressed, instead trigger event blur on the input
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('keypress', function (e) {
            if (e.target.tagName === 'TEXTAREA') {
                // If it is a textarea, allow the default behavior (go to a new line)
                return; 
            }
            if (e.key === 'Enter') {
                e.preventDefault();
                e.target.blur();
            }
        });
    });
}

export function initLanguageForm() {
        // init submit button of the language modal
        const languageSelectionButtons = document.querySelectorAll('.language-selection-button');
        languageSelectionButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                // get the language code from the button data-language attribute
                const languageCode = button.getAttribute('data-language');
                // set the language and submit the form
                document.getElementById('languageInput').value = languageCode;
                document.getElementById('languageForm').submit();
            });
        });
    }