export function initSocialAccountsTable() {
    // get all element in dom with class 'social-account-input' and loop through them
    document.querySelectorAll('.account-to-disconnect-input').forEach(function (input) {
        //get the form id
        const id = input.closest('form').id;
        //if id ends with google, set the value of the input to 'google'
        if (id.endsWith('-custom_google')) {
            input.value = 'custom_google';
        } else if (id.endsWith('-custom_microsoft')) {
            input.value = 'custom_microsoft';
        }
    });
}