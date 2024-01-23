

export function initDestinationTypeSelect() {
    // Regular expression to match IDs
    const regex = /^id_requests-\d+-destination_type_select$/;

    // Select elements with IDs matching the pattern 'id_requests-{number}-destination_type_select'
    document.querySelectorAll('[id^="id_requests-"][id$="-destination_type_select"]').forEach(select => {
        // Iterate over each option in the select element
        select.querySelectorAll('option').forEach(option => {
            // Check for Google Drive "connect" option
            if (option.value === 'google_connect') {
                // Find and hide the Google Drive option
                const googleOption = Array.from(select.options).find(opt => opt.value === "'GOOGLE_DRIVE'");
                if (googleOption) googleOption.classList.add('hidden');
            }

            // Check for OneDrive "connect" option
            if (option.value === 'onedrive_connect') {
                // Find and hide the OneDrive option
                const onedriveOption = Array.from(select.options).find(opt => opt.value === "ONE_DRIVE");
                if (onedriveOption) onedriveOption.classList.add('hidden');
            }
        });
    });
}
