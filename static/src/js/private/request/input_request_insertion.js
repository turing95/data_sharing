// Assuming you have htmx setup to add new elements

// Listen for htmx's afterSwap event, which occurs after htmx swaps content
document.body.addEventListener('htmx:afterSwap', function(event) {
    // Assuming new elements are added directly inside #sortable-list
    const list = document.getElementById('sortable-list');
    const newItem = list.lastElementChild; // The new element added by htmx

    const desiredPosition = 3; // Between the third and fourth items

    // Check if the list has enough items to insert the new item in the desired position
    if (list.children.length > desiredPosition) {
        const nextSibling = list.children[desiredPosition];
        list.insertBefore(newItem, nextSibling);
    }

    // Update positions if necessary
    updateElementPositions();
});

function updateElementPositions() {
    const list = document.getElementById('sortable-list');
    const children = list.children;
    for (let i = 0; i < children.length; i++) {
        // Assuming you're using a data attribute for position, adjust as needed
        children[i].setAttribute('data-position', i + 1);

        // If you need to send updated positions to the backend, do so here
        // For example, you could collect the new positions and use fetch() to send them
    }
}

// Initialize SortableJS on the list
new Sortable(document.getElementById('sortable-list'), {
    // SortableJS options here
});