export function initDriveProviderSwitch() {

    const driveService = document.getElementById('drive-service');
    let currentService = 'Google Drive.';

    setInterval(() => {
        // Start the fade-out effect
        driveService.classList.remove('opacity-100');
        driveService.classList.add('opacity-0');

        setTimeout(() => {
            // Change the text after the fade-out effect
            currentService = currentService === 'Google Drive.' ? 'OneDrive.' : 'Google Drive.';
            driveService.textContent = currentService;

            // Start the fade-in effect
            driveService.classList.remove('opacity-0');
            driveService.classList.add('opacity-100');
        }, 400); // This duration should match the transition duration
    }, 5000);
}
