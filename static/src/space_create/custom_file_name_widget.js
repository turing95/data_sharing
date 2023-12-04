document.addEventListener('DOMContentLoaded', function () {
    const nameInput = true// TODO: Refactor this to use the same approach as the email input widget
    if (nameInput) {

        let timeout = null;

        const getTextInput = () => document.getElementById('textInput');
        const validTags = ['l','original file name', 'upload date', 'uploader email', 'space title', 'request title']

        let lastCaretPosition = 0;
        let lastSpan

        /**
         * Get the character offset the caret is currently at
         *
         * @param {Element} element
         * @return {number}
         */
        function getCaretOffset(element) {
            let sel = element.ownerDocument.defaultView.getSelection()
            if (sel.rangeCount === 0) return 0

            let range = element.ownerDocument.defaultView.getSelection().getRangeAt(0)
            let preCaretRange = range.cloneRange()
            preCaretRange.selectNodeContents(element)
            preCaretRange.setEnd(range.endContainer, range.endOffset)
            lastCaretPosition = preCaretRange.toString().length;
            lastSpan = element
            return preCaretRange.toString().length
        }

    // Appends a partial element for the user to type into
        function appendPartial(initialText = '', selectAfterAppending = false, currentSpan) {
            const newSpan = document.createElement('span')
            newSpan.className = 'partial focus-visible:outline-none'
            newSpan.contentEditable = true

            newSpan.addEventListener('input', () => {
                parseChips(newSpan);
            })
            
            newSpan.addEventListener('click', () => {
                getCaretOffset(newSpan)
            })


            if (initialText) {
                newSpan.innerHTML = initialText
            }

            if (currentSpan) {
                getTextInput().insertBefore(newSpan, currentSpan.nextSibling)
            } else {
                getTextInput().append(newSpan) // appends initial partial
            }
            if (selectAfterAppending) {
                newSpan.focus();
            }

            return newSpan
        }

        appendPartial()


    // appends a chip
        function appendChip(tagName, currentSpan) {
            const newChip = document.createElement('span')
            newChip.className = 'inline-flex items-center px-2 mr-2 bg-gray-200 rounded tag'
            newChip.innerHTML = `${tagName.slice(1, tagName.length - 1)}
            <span class="close-tag cursor-pointer ml-1">
                <svg viewBox="0 0 24 24" width="12" height="12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" class="feather feather-x">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </span>`


            const currentPosition = getCaretOffset(currentSpan);
            const [leftSeg, rightSeg] = [currentSpan.innerText.slice(0, currentPosition), currentSpan.innerText.slice(currentPosition)];
            currentSpan.innerText = leftSeg.replace(tagName, '');

            const appendedSpan = appendPartial(rightSeg, true, currentSpan);
            getTextInput().insertBefore(newChip, appendedSpan);

            // Attach event listeners to close buttons
            newChip.querySelector('.close-tag').addEventListener('click', () => removeTag(newChip));

            return newChip
        }


        function parseChips(currentSpan) {
            let text = currentSpan.innerHTML;
            let removedChars = 0
            const match = text.match(/\{([^}]+)\}/g)

            if (!match || match.length === 0) {
                return [text, 0]
            }

            match.forEach(tagName => {
                const tagContent = tagName.slice(1, tagName.length - 1)

                if (!validTags.includes(tagContent)) {
                    return
                }

                const newEl = appendChip(tagName, currentSpan)
            })

        }

        function removeTag(element) {
            element.closest('.tag').remove();
        }

        // initially populates the metadata dropdown
        function populateDropdown() {
            const dropdown = document.getElementById('validTagsDropdown');
            validTags.forEach(tag => {
                const option = document.createElement('option');
                option.value = tag;
                option.textContent = tag;
                dropdown.appendChild(option);
            });
        }
        populateDropdown()



        


        document.getElementById('validTagsDropdown').addEventListener('change', function() {
            const selectedTag = `{${this.value}}`;
            insertTextAtPosition(selectedTag);
        });
        
        function insertTextAtPosition(text) {
            const textInput = getTextInput();
            const range = document.createRange();
            const sel = window.getSelection();
        
            // Find the right node and offset within the textInput
            let {node, offset} = getNodeAndOffset(textInput, lastCaretPosition);
        
            range.setStart(node, offset);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
        
            document.execCommand('insertText', false, text);
        }
        
        function getNodeAndOffset(node, offset) {
            // Traverse the node to find the exact child node and offset
            // where the caret should be placed.
            for (const child of node.childNodes) {
                if (child.nodeType === Node.TEXT_NODE) {
                    if (offset <= child.length) {
                        return { node: child, offset: offset };
                    }
                    offset -= child.length;
                } else {
                    const result = getNodeAndOffset(child, offset);
                    if (result) {
                        return result;
                    }
                    offset -= child.textContent.length;
                }
            }
        
            return { node: node, offset: Math.min(offset, node.length) };
        }

    }
});