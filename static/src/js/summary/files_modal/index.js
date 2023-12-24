document.body.addEventListener('htmx:afterSwap', function(event) {

        if (event.target.id.startsWith('modal-')) {
            const modalElement = event.target.children[0]; 
            if (modalElement) {
                initModal(modalElement.id);
            }
        }
});


export function initModal(id) {
    const modalElement = document.getElementById(id);
    if (!modalElement) {
        console.error('Modal element not found');
        return;
    }
    const modal = new Modal(modalElement, {
        onHide: () => {
            console.log('Modal is being hidden');
            modalElement.remove();
            // Reset the flag
            modalElement.dataset.initialized = 'false';
        },
    });

    // Find the close button within the modal
    const closeButton = modalElement.querySelector('[data-modal-hide]');
    if (closeButton) {
        closeButton.addEventListener('click', function(event) {
            modal.hide(); // Use Flowbite's hide method
        });
    }

    // Immediately show the modal upon initialization
    modal.show();
}