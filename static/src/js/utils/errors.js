import {initMessageBar} from "./messageBar.js";



function createDjangoMessagesContainer() {
    let djangoMessages = document.getElementById('django-messages');
    if (!djangoMessages) {
        djangoMessages = document.createElement('div');
        djangoMessages.id = 'django-messages';
        djangoMessages.className = "fixed left-0 z-[1000] w-full transition-all duration-500 ease-in pointer-events-none top-2";

        const ulElement = document.createElement('ul');
        ulElement.className = "messages";
        djangoMessages.appendChild(ulElement);

        document.getElementById('messageBar').appendChild(djangoMessages);
    }
    return djangoMessages;
}

function createMessageElement(errorMessage) {
    const messageLi = document.createElement('li');
    messageLi.className = "flex justify-center";
    messageLi.innerHTML = `
        <div id="alert-500" class="flex items-center p-1 text-red-800 border-t-4 border-red-300 bg-red-50" role="alert">
            <svg class="flex-shrink-0 w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                                <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
            </svg>
            <div class="text-sm font-medium ms-3">
                ${errorMessage}
            </div>
            <button type="button" class=" pointer-events-auto ms-auto ml-0.5 bg-red-50 text-red-500 focus:ring-2 focus:ring-red-400 p-1.5 hover:bg-red-200 inline-flex items-center justify-center h-5 w-5 dark:bg-gray-800 dark:text-red-400 dark:hover:bg-gray-700" aria-label="Close" data-dismiss-target="#alert-500">
                <span class="sr-only">Dismiss</span>
                <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 14 14">
                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6"/>
                </svg>
           </button>
       </div>`;
    return messageLi;
}
function appendMessageToContainer(container, messageElement) {
    const ul = container.querySelector('.messages');
    ul.appendChild(messageElement);
}

export function handleHtmxError() {
    const errorMessage = "Unexpected error try again";
    const djangoMessagesContainer = createDjangoMessagesContainer();
    const messageElement = createMessageElement(errorMessage);
    appendMessageToContainer(djangoMessagesContainer, messageElement);
    initMessageBar();
}