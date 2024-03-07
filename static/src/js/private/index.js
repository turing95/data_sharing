import {selectCompany} from "./space/create/companyInput.js";
import {hideShowSearch} from "./space/create/eventHandlers.js";

function selectContact(liElement, contactEmail, contactId) {
    let searchContainer = liElement.closest('.contact-search-container');
    let widgetContainer = liElement.closest('.contact-widget-container');
    if (!searchContainer || !widgetContainer) {
        return;
    }
    let contactInput = widgetContainer.querySelector('input[type="hidden"]');
    searchContainer.querySelector('input').value = contactEmail;
    contactInput.value = contactId;
}

document.addEventListener('click', function (event) {
    hideShowSearch(event);
});
window.selectCompany = selectCompany;
window.selectContact = selectContact;


htmx.onLoad(function (content) {
    const sortables = content.querySelectorAll(".sortable");
    console.log(sortables);
    for (let i = 0; i < sortables.length; i++) {
        let sortable = sortables[i];
        console.log(sortable);
        let sortableInstance = new Sortable(sortable, {
            animation: 150,
            ghostClass: 'blue-background-class',

            // Make the `.htmx-indicator` unsortable
            filter: ".htmx-indicator",
            onMove: function (evt) {
                return evt.related.className.indexOf('htmx-indicator') === -1;
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