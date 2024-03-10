document.addEventListener('htmx:afterSwap', function(evt) {
    // if the event target id is custom_field_container_id
    if(evt.target.id === 'custom_field_container_id') {
        // get the modal element whose id is starts with htmx-modal
        const modalElement = document.querySelector('[id^="htmx-modal"]');
        if (modalElement) {
            const modal = FlowbiteInstances.getInstance('Modal', document.getElementById('htmx-modal').children[0].id);
            modal.hide();
            modalElement.remove();
        }
    }
});