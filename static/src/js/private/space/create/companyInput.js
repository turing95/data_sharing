export function selectCompany(liElement,companyName,companyId) {
    let searchContainer =liElement.closest('.company-search-container');
    let widgetContainer = liElement.closest('.company-widget-container');
    if (!searchContainer || !widgetContainer) {
        return;
    }
    let companyInput = widgetContainer.querySelector('input[type="hidden"]');
    searchContainer.querySelector('input').value = companyName;
    companyInput.value = companyId;
}
