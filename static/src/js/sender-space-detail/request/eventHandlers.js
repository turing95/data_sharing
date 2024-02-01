import {checkTotalFileSizeWithNewFiles} from "./utils.js";

export function handleFilesUpload(inputElement) { //function to call onchange on the inputElement
    let sizeOk =checkTotalFileSizeWithNewFiles(inputElement);
    if (!sizeOk) return;
    // retrieve the tag container to which to add tags
    const parentDiv = inputElement.closest('.request-accordion-body'); //add class to form
    const tagContainer= parentDiv.querySelector('.file-tags-container'); 
    tagContainer.innerHTML = ''; //remove all children
    if(!tagContainer) return;
    
    // add title paragraph  
    let titleParagraph = document.createElement('p');
    titleParagraph.className = 'mb-2 text-sm';
    titleParagraph.textContent = 'Files ready to be uploaded:';
    tagContainer.appendChild(titleParagraph);
    

    const fileList = inputElement.files; // list of files from the input

    // these are the files currently added in the input Field
    for (let i = 0; i < fileList.length; i++) {        
        const tag = createFileTag(fileList[i].name);
        tagContainer.appendChild(tag)
    }
}

function createFileTag(fileName) {
    const tag = document.createElement('span');

    tag.className = 'inline-flex items-center bg-blue-100 text-blue-800 text-sm font-medium px-2.5 py-0.5 my-1 break-all';
    tag.title = fileName;



    //tag.appendChild(createCloseButton(tag));

    // text wrapper to apply styling
    const textWrapper = document.createElement('span');
    textWrapper.className = 'line-clamp-2';
    textWrapper.textContent = fileName;
    tag.appendChild(textWrapper);


    return tag;
}