window.onload = adjustSidebarPadding;
window.onresize = adjustSidebarPadding;
window.onload = applySameLeftMargin;
window.onresize = applySameLeftMargin;

document.body.addEventListener('htmx:afterOnLoad', function(event) {
    console.log("HTMX event detail:", event.detail);
    if (event.detail.pathInfo) {
        const fullPath = event.detail.pathInfo.finalRequestPath;
        // Assuming the URL format is /documentation/content/article_name/
        const articleName = fullPath.split('/').slice(-2, -1)[0]; // Get the article_name from the URL
        const newUrl = `/documentation/${articleName}`;
        history.pushState({}, '', newUrl);
    }
});

function adjustSidebarPadding() {
    const footer = document.getElementById('page_footer');
    const sidebar = document.getElementById('logo-sidebar');
    if (footer && sidebar) {
        const footerHeight = footer.offsetHeight;
        sidebar.style.paddingBottom = footerHeight + 'px';
    }
}

function applySameLeftMargin() {
    const navbar = document.getElementById("main-navbar");
    const navbarWidth = navbar.offsetWidth;
    const screenWidth = window.innerWidth;
    const leftMargin = (screenWidth - navbarWidth) / 2 + 'px';

    let targetElement = document.getElementById("logo-sidebar");
    targetElement.style.marginLeft = leftMargin;
    targetElement = document.getElementById("sidebar-button-container");
    targetElement.style.marginLeft = leftMargin;
}

