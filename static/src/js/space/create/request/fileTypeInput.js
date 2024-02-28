
export function initializeFileTypes(requestForm) {
    const fileTypeInput = requestForm.querySelector('.file-types');
    if(!fileTypeInput) return;
    if (fileTypeInput.value){
        fileTypeInput.value.split(',').forEach(fileTypeSlug =>{
    let fileTypeInput =  requestForm.querySelector('.file-types');
        const tag = createTag(fileTypeSlug,fileTypeInput);
        requestForm.querySelector('.file-type-tags').appendChild(tag);
        requestForm.querySelector('.file-type-title').classList.remove('hidden');
        requestForm.querySelector('.no-file-types').classList.add('hidden');
    } );
    }

}

function createTag(fileType,fileTypeInput) {
    const tag = document.createElement('span');
    tag.className = 'file-type-tag-span inline-flex items-center bg-blue-100 text-blue-800 text-sm font-semibold px-2.5 py-0.5 mr-1 mb-1';
    tag.textContent = fileType;

    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = '&times;';
    closeBtn.className = 'ml-2 cursor-pointer';
    closeBtn.onclick = () => {
        if (tag.parentElement.children.length === 1) {
            tag.parentElement.parentElement.querySelector('.file-type-title').classList.add('hidden');
            tag.parentElement.parentElement.querySelector('.no-file-types').classList.remove('hidden');
        }
        tag.remove();
        let addedFileTypes = new Set(fileTypeInput.value.split(',').filter(x => x));
        addedFileTypes.delete(fileType);
        addedFileTypes = Array.from(addedFileTypes).join(',');
        fileTypeInput.value = addedFileTypes

    };

    tag.appendChild(closeBtn);
    return tag;
}
export function addFileTypeTag(liElement,fileTypeSlug) {
    let form =liElement.closest('.request-form')
    let fileTypeInput = form.querySelector('.file-types');
    let addedFileTypes = new Set(fileTypeInput.value.split(',').filter(x => x));
    if (!addedFileTypes.has(fileTypeSlug)) {
        const tag = createTag(fileTypeSlug,fileTypeInput);

        if (fileTypeInput.value === '') {
            fileTypeInput.value = fileTypeSlug;
            form.querySelector('.file-type-title').classList.remove('hidden')
            form.querySelector('.no-file-types').classList.add('hidden')
        } else {
            fileTypeInput.value += ',' + fileTypeSlug;
        }
        form.querySelector('.file-type-tags').appendChild(tag);
    }
}

export function setupFileTypeCloseButton(requestForm) {
    requestForm.querySelectorAll('.file-type-tags .file-type-tag-span').forEach(tag => {
        const closeBtn = tag.querySelector('span');
        closeBtn.onclick = () => {
            if (tag.parentElement.children.length === 1) {
                tag.parentElement.parentElement.querySelector('.file-type-title').classList.add('hidden');
                tag.parentElement.parentElement.querySelector('.no-file-types').classList.remove('hidden');
            }
            tag.remove();
            let addedFileTypes = new Set(requestForm.querySelector('.file-types').value.split(',').filter(x => x));
            addedFileTypes.delete(tag.childNodes[0].textContent.trim());
            addedFileTypes = Array.from(addedFileTypes).join(',');
            requestForm.querySelector('.file-types').value = addedFileTypes

        };
    });
}