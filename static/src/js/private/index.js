import {hideShowSearch} from "./eventHandlers.js";
window.selectCompany = selectCompany;
window.selectContact = selectContact;
function selectContact(liElement, contactEmail, contactId) {
    let searchContainer = liElement.closest('.contact-search-container');
    let widgetContainer = liElement.closest('.contact-widget-container');
    if (!searchContainer || !widgetContainer) {
        return;
    }
    let contactInput = widgetContainer.querySelector('input[type="hidden"]');
    searchContainer.querySelector('input').value = contactEmail;
    contactInput.value = contactId;
    contactInput.dispatchEvent(new CustomEvent("change"));

}
export function selectCompany(companyName,companyId) {
    let searchContainer =document.querySelector('.company-search-container');
    let widgetContainer = document.querySelector('.company-widget-container');
    if (!searchContainer || !widgetContainer) {
        return;
    }
    let companyInput = widgetContainer.querySelector('input[type="hidden"]');
    searchContainer.querySelector('input').value = companyName;
    companyInput.value = companyId;
    // clean error messages if any
    let parentElement = searchContainer.parentNode.parentNode;
    let errorMessages = parentElement.querySelectorAll('.error-message');
    errorMessages.forEach(errorMessage => {
        errorMessage.textContent = ''; // Clear the content of each error message
    });

}

document.body.addEventListener("selectCompany", function(evt){
    selectCompany(evt.detail.name,evt.detail.uuid)
})

document.addEventListener('click', function (event) {
    hideShowSearch(event);
});

document.addEventListener('DOMContentLoaded', function () {
    preventFormSubmit();
});


htmx.onLoad(function (content) {
    const sortables = content.querySelectorAll(".sortable");
    for (let i = 0; i < sortables.length; i++) {
        let sortable = sortables[i];
        let sortableInstance = new Sortable(sortable, {
            animation: 150,
            dragClass: 'bg-blue-100',

            // Make the `.htmx-indicator` unsortable
            filter: ".my-htmx-indicator",
            onMove: function (evt) {
                return evt.related.className.indexOf('my-htmx-indicator') === -1;
            },

            // Disable sorting on the `end` event
            onEnd: function (evt) {
            this.option("disabled", true);
          }
        });

        // Re-enable sorting on the `htmx:afterSwap` event
        sortable.addEventListener("htmx:afterSwap", function () {
            sortableInstance.option("disabled", false);

        });
    }
})


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