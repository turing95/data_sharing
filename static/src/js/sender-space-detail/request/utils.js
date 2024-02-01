export function checkTotalFileSizeWithNewFiles(inputElement) {
    const limit = 50 * 1024 * 1024; // X MB to bytes
    let totalSize = 0;
    const fileInputs = document.querySelectorAll('input[type="file"]');

    // Calculate the total size of already selected files
    fileInputs.forEach(input => {
        if (input !== inputElement) { // Skip the current input to calculate its files later
            Array.from(input.files).forEach(file => totalSize += file.size);
        }
    });

    // Calculate the size with the new files
    Array.from(inputElement.files).forEach(file => totalSize += file.size);

    if (totalSize > limit) {
        alert(`Adding these files would exceed the total limit of 50 MB. Please select fewer or smaller files.`);
        inputElement.value = ''; // Clears the recent selection, not allowing addition
        return false;
    }
    return true;
}
