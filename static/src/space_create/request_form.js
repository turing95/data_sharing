document.addEventListener('DOMContentLoaded', function() {
    initializeEventListeners();
});


    



function initializeEventListeners() {
    // Click event for adding new request forms
    let addButton = document.getElementById('add-request-btn');
    if (addButton) {
        addButton.addEventListener('click', addNewRequestForm);
    }

}

function addNewRequestForm() {
    let totalForms = document.getElementById('id_requests-TOTAL_FORMS');
    if (!totalForms) return;

    let formCount = parseInt(totalForms.value);
    let newForm = cloneRequestForm(formCount);

    if (newForm) {
        document.getElementById('requests-container').appendChild(newForm);
        totalForms.value = formCount + 1;
    }
}

function cloneRequestForm(formCount) {
    let templateForm = document.querySelector('.request-form');
    if (!templateForm) {
        console.error('Request form template not found!');
        return null;
    }

    let newForm = templateForm.cloneNode(true);

    // Update Accordion Content IDs and Button targets
    newForm.querySelectorAll('div[id^="accordion-open-body-"]').forEach(div => {
        // Generate the new ID for the accordion content
        let oldDivId = div.id;
        let newDivId = `accordion-open-body-${formCount}`;
        div.id = newDivId;

        // Find the corresponding button in the newForm and update its data-accordion-target attribute
        let buttonSelector = `button[data-accordion-target="#${oldDivId}"]`;
        let accordionButton = newForm.querySelector(buttonSelector);
        if (accordionButton) {
            accordionButton.setAttribute('data-accordion-target', `#${newDivId}`);
            accordionButton.addEventListener('click', function() {
                toggleAccordion(this);
            });
        }
    });

    function toggleAccordion(accordionButton) {
        let targetId = accordionButton.getAttribute('data-accordion-target');
        let targetElement = document.querySelector(targetId);
    
        if (targetElement) {
            targetElement.classList.toggle('hidden'); // Toggle visibility
            let isExpanded = accordionButton.getAttribute('aria-expanded') === 'true';
            accordionButton.setAttribute('aria-expanded', String(!isExpanded));
        }
    }




    // Update 'for' attribute of labels
    newForm.querySelectorAll('label').forEach(label => {
        if (label.htmlFor) {
            label.htmlFor = label.htmlFor.replace(/-\d+-/, `-${formCount}-`);
        }
    });

    // Remove any unwanted elements (like error messages) from the cloned form
    // newForm.querySelectorAll('.error-message').forEach(msg => msg.remove());

    // Reinitialize event listeners or plugins here, if necessary

    // Add event listener to the existing close button in the cloned form
    let closeButton = newForm.querySelector('.request-close-button'); // Replace '.close-button' with the correct class or ID of your close button
    if (closeButton) {
        // Remove 'hidden' class to make the button visible
        closeButton.classList.remove('invisible');

        closeButton.addEventListener('click', function() {
            this.closest('.request-form').remove();
            let totalForms = document.getElementById('id_requests-TOTAL_FORMS');
            if (totalForms) {
                totalForms.value = parseInt(totalForms.value) - 1;
            }
        });
    }

    return newForm;
}

function toggleRename(checkbox) {
    const parentDiv = checkbox.closest('.request-form');
    const childDiv1= parentDiv.querySelector('.file-name-container');
    if (!childDiv1) return;

    if (checkbox.checked) {
        childDiv1.classList.remove('hidden');
    } else {
        childDiv1.classList.add('hidden');
    }
}
