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
