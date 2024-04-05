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
    document.body.dispatchEvent(new CustomEvent("contactUpdated"));

}
document.body.addEventListener("htmx:afterSwap", function(evt) {
    if (evt.detail.target.id.startsWith('search-contacts-results-container')) {
        const searchContainer = evt.detail.target;
        const sender_uuid = searchContainer.getAttribute('data-sender-uuid');
        const newContactEl = searchContainer.querySelector(".new-contact-el");
        if (!newContactEl) {
            return;
        }
        // Prepare the hx-vals data with sender_uuid
        const hxValsData = JSON.stringify({ sender_uuid: sender_uuid });
        // Set the hx-vals attribute on the .new-contact-el element
        newContactEl.setAttribute('hx-vals', hxValsData);
    }
});

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

document.addEventListener('end', function (event) {
    // Get the item that triggered the event
    let targetItem = event.target;

    // Get the first ancestor with class "sortable" of the item that triggered the event
    let sortableAncestor = targetItem.closest('.sortable');

    // Get all the first level children with class "sort-el" of the sortable ancestor
    let sortElements = sortableAncestor.querySelectorAll(':scope > .sort-el');

    // Initialize an object to hold the query string components
    let queryStringComponents = {};

    // Loop through the list of sort-el elements
    sortElements.forEach((element, index) => {
        // Get the first child of the element
        let firstChildElement = element.children[0];

        // Check if the first child element exists and has a "value" property
        if (firstChildElement && firstChildElement.value) {
            // Construct an object with the name and value
            queryStringComponents[`el_${index + 1}`] = firstChildElement.value;
        }
    });

    // Convert the object to a JSON string
    let queryString = JSON.stringify(queryStringComponents);

    // Update the hx-vals attribute with the new value
    sortableAncestor.setAttribute('hx-vals', queryString);

    // Now dispatch a custom event named "endSort" with the original targetItem as the target
    let endSortEvent = new CustomEvent('endSort');
    targetItem.dispatchEvent(endSortEvent);

    // For debugging: log the updated hx-vals attribute value
    console.log(sortableAncestor.getAttribute('hx-vals'));
});


htmx.onLoad(function (content) {
    initializeSortables(content);
});

function initializeSortables(content) {
    let sortables = Array.from(content.querySelectorAll(".sortable"));
    if (content.classList.contains('sortable')) {
        sortables.push(content);
    }
    sortables.forEach(function(sortable) {
        let sortableInstance = new Sortable(sortable, {
            animation: 150,
            dragClass: 'bg-blue-100',
            filter: ".my-htmx-indicator",
            onMove: function (evt) {
                return evt.related.className.indexOf('my-htmx-indicator') === -1;
            },
            onEnd: function (evt) {
                this.option("disabled", true);
            },
            disabled: true,
        });

        attachHoverListeners(sortable, sortableInstance);

        // Re-initialize sorting enable-hover logic on HTMX afterSwap
        sortable.addEventListener("htmx:afterSwap", function () {
            attachHoverListeners(sortable, sortableInstance);
            // Potentially re-enable or re-disable sorting based on current hover state
            if (sortable.querySelector('.sort-enable-hover:hover')) {
                sortableInstance.option("disabled", false);
            } else {
                sortableInstance.option("disabled", true);
            }
        });
    });
}

function attachHoverListeners(sortable, sortableInstance) {
    let sortEnableHoverElements = sortable.querySelectorAll('.sort-enable-hover');
    sortEnableHoverElements.forEach(function(sortEnableHoverElement) {
        sortEnableHoverElement.onmouseenter = function () {
            sortableInstance.option("disabled", false);
        };

        sortEnableHoverElement.onmouseleave = function () {
            setTimeout(() => {
                // If not hovering over any sort-enable-hover elements, disable sorting
                if (!sortable.querySelector('.sort-enable-hover:hover')) {
                    sortableInstance.option("disabled", true);
                }
            }, 100);
        };
    });
}


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

