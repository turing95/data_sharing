export function createFileTag(fileName) {
    const tag = document.createElement('span');

    tag.className = 'inline-flex items-center bg-blue-100 text-blue-800 text-sm font-medium px-2.5 py-0.5 my-1 break-all';
    tag.title = fileName;

    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = '&times;';
    closeBtn.className = 'mr-2 cursor-pointer';

    // to  deactivate for now
    // if there is only one tag left remove also the tags label
    closeBtn.onclick = () => {
        var parent = tag.parentNode;
    
        if (parent.children.length === 2) {
            parent.innerHTML = '';
        } else {
            tag.remove();
        }
    };

    tag.appendChild(closeBtn);
    
    // text wrapper to apply styling
    const textWrapper = document.createElement('span');
    textWrapper.className = 'line-clamp-2'; 
    textWrapper.textContent = fileName;
    tag.appendChild(textWrapper);
    

    return tag;
}