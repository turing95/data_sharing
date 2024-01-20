
export function initHtmxModal(id) {
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
        'bg-gray-900/70 dark:bg-gray-900/80 fixed inset-0 z-[51]',
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