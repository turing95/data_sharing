document.addEventListener('DOMContentLoaded', function() {
        let isPublicCheckbox = document.getElementById('id_is_public');
        let participantsDiv = document.getElementById('participants-input');

        // Check if elements exist
        if (!isPublicCheckbox || !participantsDiv) {
            console.error('Form elements not found!');
            return; // Exit if elements are not found
        }

        function toggleParticipantsInput() {
            // Check the checkbox state
            if (isPublicCheckbox.checked) {
                participantsDiv.style.display = 'none';
            } else {
                participantsDiv.style.display = 'block';
            }
        }

        // Initial check for the state of the checkbox
        toggleParticipantsInput();


        document.getElementById('add-request-btn').addEventListener('click', function() {
        let totalForms = document.getElementById('id_requests-TOTAL_FORMS');
        let formCount = parseInt(totalForms.value);
        let newForm = document.querySelector('.request-form').cloneNode(true);

        // Replace the form number in the cloned form
        newForm.innerHTML = newForm.innerHTML.replace(/-\d+-/g, `-${formCount}-`);

        // Add a remove button to the cloned form
        let removeBtn = document.createElement('button');
        removeBtn.type = 'button';
        removeBtn.textContent = 'Remove';
        removeBtn.className = 'text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800';
        removeBtn.addEventListener('click', function() {
            this.parentNode.remove();
            totalForms.value = parseInt(totalForms.value) - 1;
        });

        newForm.appendChild(removeBtn);

        document.getElementById('requests-container').appendChild(newForm);
        totalForms.value = formCount + 1;
    });
        // Event listener for changes in the 'is_public' checkbox
        isPublicCheckbox.addEventListener('change', toggleParticipantsInput);



    });