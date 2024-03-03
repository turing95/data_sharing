export function selectCompany(liElement,companyName,companyId) {
    let searchContainer =liElement.closest('.search-container');
    let companyInput = liElement.closest('.widget-container').querySelector('input[type="hidden"]');
    searchContainer.querySelector('input').value = companyName;
    companyInput.value = companyId;
}
