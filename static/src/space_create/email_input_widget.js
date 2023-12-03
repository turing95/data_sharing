document.addEventListener('DOMContentLoaded', function () {

    let addedEmails = new Set();

    function isValidEmail(email) {
        // Simple regex for email validation
        return /\S+@\S+\.\S+/.test(email);
    }

    function createTag(email) {
        const tag = document.createElement('span');
        tag.className = 'inline-flex items-center bg-blue-100 text-blue-800 text-sm font-semibold px-2.5 py-0.5 ';
        tag.textContent = email;

        const closeBtn = document.createElement('span');
        closeBtn.innerHTML = '&times;';
        closeBtn.className = 'ml-2 cursor-pointer';
        closeBtn.onclick = () => {
            tag.remove();
            addedEmails.delete(email);
        };

        tag.appendChild(closeBtn);
        return tag;
    }

    function addEmailTag(email) {
        if (isValidEmail(email) && !addedEmails.has(email)) {
            const tag = createTag(email);
            document.getElementById('tags').appendChild(tag);
            addedEmails.add(email);
        }
    }

    document.getElementById('email-input').addEventListener('keydown', (e) => {
        if ([' ', ',', ';', 'Enter'].includes(e.key)) {
            e.preventDefault();
            const input = e.target;
            const inputText = input.value;
            const parts = inputText.split(/[\s,]+/);

            let remainingText = '';

            parts.forEach(part => {
                if (isValidEmail(part.trim())) {
                    addEmailTag(part.trim());
                } else {
                    remainingText += part + ' ';
                }
            });

            input.value = remainingText.trim();
        }
    });

    document.getElementById('email-input').addEventListener('paste', (e) => {
        e.preventDefault();
        const pastedText = (e.clipboardData || window.clipboardData).getData('text');
        const emails = pastedText.split(/[\s,]+/);

        let nonEmailText = '';

        emails.forEach(email => {
            if (isValidEmail(email.trim())) {
                addEmailTag(email.trim());
            } else {
                nonEmailText += email + ' ';
            }
        });

        document.getElementById('email-input').value = nonEmailText.trim();
    });

    document.getElementById("space-form").addEventListener('submit', (e) => {
        const hiddenInput = document.getElementById('hidden-email-input');
        hiddenInput.value = Array.from(addedEmails).join(',');
    });
});