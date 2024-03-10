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
    contactInput.dispatchEvent(new CustomEvent("change"));

}

document.addEventListener('click', function (event) {
    hideShowSearch(event);
});
window.selectCompany = selectCompany;
window.selectContact = selectContact;


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

            const children = sortableInstance.el.children;
            if (children.length > 0) {
                const lastItem = children[children.length - 1];
                //get target position of last item, if empty was not added in this swap
                let desiredPosition = parseInt(lastItem.getAttribute("data-position")); 
                if (!isNaN(desiredPosition)) {
                    // Ensure desiredPosition is within bounds before attempting to move the element
                    if (desiredPosition > 0 && desiredPosition <= children.length-1) {
                        const targetChild = children[desiredPosition];
                        if (targetChild !== lastItem) { // avoid moving if it's already in the correct position
                            sortableInstance.el.insertBefore(lastItem, targetChild);                            
                        }
                        
                    }
                    lastItem.setAttribute("data-position", ""); // Clear the attribute 
                }
            }
            
        });
    }
})
