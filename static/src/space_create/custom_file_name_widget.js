document.addEventListener('DOMContentLoaded', function () {
    var emailInput = false //document.getElementById('id_email_input'); // TODO: Refactor this to use the same approach as the email input widget
    if (emailInput) {

        let timeout = null;

        const getTextInput = () => document.getElementById('textInput');
        const validTags = ['original file name', 'upload date', 'uploader email', 'space title', 'request title']

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
    }
});