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

        // Event listener for changes in the 'is_public' checkbox
        isPublicCheckbox.addEventListener('change', toggleParticipantsInput);
    });