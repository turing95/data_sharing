let addedEmails = new Set();

export function initEmailInput() {
    initializeEmailTags();

    const emailInput = document.getElementById('id_search-contacts');

    emailInput.addEventListener('blur', () => {
        const email = emailInput.value.trim();
        if (isValidEmail(email)) {
            addEmailTag(email);
            emailInput.value = '';
        }
    });

    emailInput.addEventListener('keydown', (e) => {
        if ([' ', ',', ';', 'Enter'].includes(e.key)) {
            e.preventDefault();
            emailInput.value = processInputText(emailInput.value);
        }
    });

    emailInput.addEventListener('paste', (e) => {
        e.preventDefault();
        emailInput.value = processInputText((e.clipboardData || window.clipboardData).getData('text'));
    });

    document.getElementById("space-form").addEventListener('submit', () => {
        document.getElementById('id_senders_emails').value = Array.from(addedEmails).join(',');
    });

}

function isValidEmail(email) {
    return /\S+@\S+\.\S+/.test(email);
}

function createTag(email) {
    const tag = document.createElement('span');
    tag.className = 'inline-flex items-center bg-blue-100 text-blue-800 text-sm font-semibold px-2.5 py-0.5';
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

export function processInputText(inputText) {
    const parts = inputText.split(/[\s,]+/);
    return parts.reduce((remainingText, part) => {
        if (isValidEmail(part.trim())) {
            addEmailTag(part.trim());
        } else {
            remainingText.push(part);
        }
        return remainingText;
    }, []).join(' ');
}

function initializeEmailTags() {
    const sendersInput = document.getElementById('id_senders_emails');
    sendersInput.value.split(',').forEach(email => email.trim() && addEmailTag(email.trim()));
    sendersInput.value = '';
}