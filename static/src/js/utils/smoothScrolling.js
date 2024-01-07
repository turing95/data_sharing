export function initSmoothScrolling() {
    const navbar = document.getElementById('navbar');
    const navbarHeight = navbar ? navbar.offsetHeight : 0;

    document.querySelectorAll('a[href*="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            const path = href.split('#')[0];
            const currentPath = window.location.pathname;

            if (path === '' || path === currentPath) {
                e.preventDefault();
                const sectionId = href.split('#')[1];
                const section = document.getElementById(sectionId);

                if (section) {
                    const sectionTop = section.offsetTop;
                    window.scrollTo({
                        top: sectionTop - navbarHeight, // Adjusting for the navbar height
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

export function adjustScrollPositionOnPageLoad() {
    setTimeout(function() {
        const navbar = document.getElementById('navbar');
        const navbarHeight = navbar ? navbar.offsetHeight : 0;
        const currentPath = window.location.pathname;
        const hash = window.location.hash;

        if (hash) {
            const sectionId = hash.substring(1); // Remove '#' from hash
            const section = document.getElementById(sectionId);

            if (section) {
                const sectionTop = section.offsetTop;

                // Jump to the section adjusted by navbar height
                window.scrollTo({
                    top: sectionTop - navbarHeight, // Adjusting for the navbar height
                });

            }
        }
    }, 0);
}



  

