export function hideShowSearch(event) {
    let clickedElement = event.target;

    // Check if the clicked element doesn't meet the criteria
    if (!clickedElement.classList.contains('search-input')) {

        // Find all elements with the class 'search-results'
        let searchResults = document.querySelectorAll('.search-results');

        // Add the 'hidden' class to each of these elements
        searchResults.forEach(function(element) {
            element.classList.add('hidden');
        });
    }else{
        //show only search results next to element
        let form = clickedElement.closest('form')
        if(form) {
            let searchResults = form.querySelector('.search-results');
            searchResults.classList.remove('hidden');
        }else{
            let searchResults = clickedElement.closest('.search-container').querySelector('.search-results');
            searchResults.classList.remove('hidden');
        }
        

    }
}