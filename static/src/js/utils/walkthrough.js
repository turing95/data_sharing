export function initWalkthroughTipbox() {
    let closeButton = document.querySelector('#walkthrough-tipbox-container #close-btn');
    if (closeButton) {
        closeButton.addEventListener('click', closeTipbox);
    }

    let tipbox = document.getElementById('walkthrough-tipbox');
    if (tipbox) {
        let targetId = tipbox.getAttribute('data-target');
        let targetEl = document.getElementById(targetId);

        if (targetEl) {
            adjustTipboxAndBackdrop(targetEl, tipbox);
        }
        // Listen for multiple events and reinitialize the tipbox
        window.addEventListener('resize', reinitializeTipbox);
        window.addEventListener('click', reinitializeTipbox);
        window.addEventListener('keydown', reinitializeTipbox);

    }
}

function reinitializeTipbox() {
    let tipbox = document.getElementById('walkthrough-tipbox');
    if (tipbox && tipbox.getAttribute('data-target')) {
        initWalkthroughTipbox();
    }
}



function adjustTipboxAndBackdrop(targetEl, tipbox) {
    let rect = targetEl.getBoundingClientRect();
    let rectTop = Math.round(rect.top);
    let rectBottom = Math.round(rect.bottom);
    let rectLeft = Math.round(rect.left);
    let rectRight = Math.round(rect.right);
    let scrollTop = Math.round(window.scrollY || document.documentElement.scrollTop);
    let scrollLeft = Math.round(window.scrollX || document.documentElement.scrollLeft);

    const gap = 10;

    // Rounding the positions and dimensions to the nearest pixel
    let topHeight = rectTop + scrollTop - gap;
    let leftWidth = Math.round(rectLeft + scrollLeft - gap);
    let rectHeight = Math.round(rect.height) + 2 * gap;
    let bottomStart = topHeight + rectHeight;

    // Calculate the total document height
    const docHeight = Math.max(document.body.scrollHeight, document.body.offsetHeight, 
        document.documentElement.clientHeight, document.documentElement.scrollHeight, 
        document.documentElement.offsetHeight);
    let bottomHeight = docHeight - bottomStart;

    // Dynamically set styles for precise positioning
    tipbox.style.position = 'absolute';
    tipbox.style.top = `${Math.round(rectBottom + scrollTop + gap)}px`;
    tipbox.style.left = `${Math.round(rectLeft + scrollLeft + gap)}px`;

    // Adjust backdrop parts to include the gap around the target element
    document.getElementById('walkthrough-backdrop-top').classList.remove('hidden');
    document.getElementById('walkthrough-backdrop-top').style.cssText = `top: 0px; left: 0px; width: 100%; height: ${topHeight}px;`;

    // For the bottom part, setting the bottom style to 0px ensures it touches the bottom of the page.
    document.getElementById('walkthrough-backdrop-bottom').classList.remove('hidden');
    document.getElementById('walkthrough-backdrop-bottom').style.cssText = `top: ${bottomStart}px; left: 0px; width: 100%; height:${bottomHeight}px;`;

    // The left part remains unchanged
    document.getElementById('walkthrough-backdrop-left').classList.remove('hidden');
    document.getElementById('walkthrough-backdrop-left').style.cssText = `top: ${topHeight}px; left: 0px; width: ${leftWidth}px; height: ${rectHeight}px;`;

    // For the right part, since we want it to take all available space, we adjust the left property to the right edge of the target element plus the gap.
    // Ensure the right part stretches to the right edge of the document by not setting a specific width.
    document.getElementById('walkthrough-backdrop-right').classList.remove('hidden');
    document.getElementById('walkthrough-backdrop-right').style.cssText = `top: ${topHeight}px; left: ${Math.round(rect.right + scrollLeft + gap)}px; right: 0px; height: ${rectHeight}px;`;

    // Scroll to include the target element if it's not fully in the window view
    scrollToTargetElement(targetEl);
}



function scrollToTargetElement(targetEl) {
    const rect = targetEl.getBoundingClientRect();
    const visibleTopMargin = 50; // Distance from the top of the window we want the element to be after scrolling
    const visibleBottomMargin = 50; // Distance from the bottom of the window we want the element to be

    // Check if the element's top is above the viewport
    if (rect.top < visibleTopMargin) {
        // Scroll up to bring the element's top into view, with a 50px margin or to the top of the document
        window.scrollBy({ top: rect.top - visibleTopMargin, behavior: 'smooth' });
    }
    // Check if the element's bottom is below the viewport
    else if (rect.bottom > window.innerHeight - visibleBottomMargin) {
        // Scroll down to bring the element's bottom into view, with a 50px margin or to the bottom of the document
        window.scrollBy({ top: rect.bottom - window.innerHeight + visibleBottomMargin, behavior: 'smooth' });
    }
}


function closeTipbox() {
    let tipboxContainer = document.getElementById('walkthrough-tipbox-container');

    if (tipboxContainer) {
        tipboxContainer.innerHTML = '';
    }
    
}

