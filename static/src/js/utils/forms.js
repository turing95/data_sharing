export function preventEnter() {
    //prevent submit on all forms when enter is pressed, instead trigger event blur on the input
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                e.target.blur();
            }
        });
    });
}