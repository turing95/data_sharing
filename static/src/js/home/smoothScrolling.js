function getNavbarHeight() {
    const navbar = document.getElementById('navbar');
    return navbar ? navbar.offsetHeight : 0;
}

function smoothScrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        window.scrollTo({
            top: section.offsetTop - getNavbarHeight(),
            behavior: 'smooth'
        });
    }
}

export function initSmoothScrolling() {
    document.querySelectorAll('a[href*="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const url = new URL(this.href);
            const currentPath = window.location.pathname;

            if (url.pathname === currentPath || url.pathname === '') {
                e.preventDefault();
                smoothScrollToSection(url.hash.substring(1));
            }
        });
    });
}

function adjustScrollPositionWithDebounce() {
    let timeout = null;
    return function() {
        clearTimeout(timeout);
        timeout = setTimeout(function() {
            if (window.location.hash) {
                smoothScrollToSection(window.location.hash.substring(1));
            }
        }, 100);
    };
}

export function adjustScrollPosition() {
    window.addEventListener('load', adjustScrollPositionWithDebounce());
    window.addEventListener('resize', adjustScrollPositionWithDebounce());
}

