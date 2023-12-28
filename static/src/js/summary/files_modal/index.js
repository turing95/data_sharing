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
            modalElement.remove();
        },
        backdropClasses:
        'bg-gray-900/70 dark:bg-gray-900/80 fixed inset-0 z-40',
    });

    const closeButton = modalElement.querySelector('[data-modal-hide]');
    if (closeButton) {
        closeButton.addEventListener('click', function(event) {
            modal.hide(); // Flowbite's hide method
        });
    }

    // show the modal upon initialization
    modal.show();
}