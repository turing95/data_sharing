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
    // Flag to track dragging state
    let isDragging = false;
    // Function to add or remove the 'hidden' class on drag-hidden elements of siblings
    function toggleHiddenClassOnSiblings(add) {
        // Find the parent node to get siblings from
        const parent = draggableParent.parentNode;
        // Iterate over each child of the parent node
        Array.from(parent.children).forEach(child => {
            // Skip if the child is the draggableParent itself
           
            // For each sibling, find .drag-hidden elements and toggle 'hidden' class
            const elementsToHide = child.querySelectorAll('.drag-hidden');
            elementsToHide.forEach(el => {
                if (add) {
                    el.classList.add('hidden');
                } else {
                    el.classList.remove('hidden');
                }
            });
            
        });
    }

    let sortEnableHoverElements = sortable.querySelectorAll('.sort-enable-hover');
    sortEnableHoverElements.forEach(function(sortEnableHoverElement) {
        sortEnableHoverElement.onmouseenter = function () {
            // Enable sorting on mouse enter if not dragging
            if (!isDragging) {
                sortableInstance.option("disabled", false);
            }
        };

        sortEnableHoverElement.onmouseleave = function () {
            setTimeout(() => {
                // Only disable sorting on mouse leave if not dragging
                if (!isDragging) {
                    sortableInstance.option("disabled", true);
                    console.log('left'); // For debugging
                }
            }, 100);
        };

        let draggableParent = sortEnableHoverElement.closest('.sort-el');

        // Listen for the start of dragging to set isDragging flag
        draggableParent.addEventListener('dragstart', function() {
            isDragging = true;
            console.log('drag  ')
             // Find all child elements that should be hidden during the drag
            // let elementsToHide = draggableParent.querySelectorAll('.drag-hidden');
            // elementsToHide.forEach(function(el) {
            //     el.classList.add('hidden'); // Add the 'hidden' class to hide the element
            // });
            // const parent = draggableParent.parentNode;
            // // Iterate over each child of the parent node
            // Array.from(parent.children).forEach(child => {
            //     // Skip if the child is the draggableParent itself
            
            //     // For each sibling, find .drag-hidden elements and toggle 'hidden' class
            //     const elementsToHide = child.querySelectorAll('.drag-hidden');
            //     elementsToHide.forEach(el => {
            //             el.classList.add('hidden');
            //    });
                
            //});
        });

        // Listen for the dragend event to clear the isDragging flag
        // This might need to be attached more broadly, depending on your application's structure
        draggableParent.addEventListener('dragend', function() {
            isDragging = false;
            console.log('drag stop ')
            // let elementsToHide = draggableParent.querySelectorAll('.drag-hidden');
            // elementsToHide.forEach(function(el) {
            //     el.classList.remove('hidden'); // Remove the 'hidden' class to show the element again
            // });
        });
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

// Function to toggle visibility and rotate the arrow
function initializeCollapsibles() {
    // Iterate over each element with the `data-collapsible-target` attribute
    document.querySelectorAll('[data-collapsible-target]').forEach(button => {
        toggleCollapsible(button)
    });
  }

function toggleCollapsible(button) {
    button.addEventListener('click', function() {
        // Get the ID of the target from the button's `data-collapsible-target` attribute
        const targetId = this.getAttribute('data-collapsible-target');
        // Find the corresponding div by its ID
        const targetDiv = document.querySelector(targetId);
  
        // Toggle the hidden property of the target div
        if (targetDiv) {
          targetDiv.hidden = !targetDiv.hidden;
        }
  
        // Assuming the first child is the SVG you want to rotate
        const svgArrow = this.children[0];
        if (svgArrow) {
          // Toggle the `rotate-180` class on the SVG arrow
          svgArrow.classList.toggle('rotate-180');
        }
      });
}
  
  // Call the function when the document is ready
  document.addEventListener('DOMContentLoaded', initializeCollapsibles);

  document.body.addEventListener('htmx:afterSwap', function(event) {
    // The event.target contains the newly loaded content
    // You can apply any necessary JavaScript behaviors here
  
    // For example, find all elements with `data-collapsible-target` within the new content and reapply behaviors
    event.target.querySelectorAll('[data-collapsible-target]').forEach(button => {
      // Since we're using delegation, you might want to ensure you're not adding multiple listeners
      // One way to do this is to add a class to mark that we've initialized this element and check for it
      if (!button.classList.contains('js-initialized')) {
        button.classList.add('js-initialized');
        // Your code to initialize the button, like adding specific event listeners or classes, goes here
        toggleCollapsible(button)
      }
    });
  });