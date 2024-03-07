import {selectCompany} from "./space/create/companyInput.js";
import {hideShowSearch} from "./space/create/eventHandlers.js";

function selectContact(liElement,contactEmail,contactId) {
    let searchContainer =liElement.closest('.contact-search-container');
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