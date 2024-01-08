export function initNav()  {
    // Handle click event on navbar links
    const navLinks = document.querySelectorAll('#navbar a');
    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            navLinks.forEach(link => {
                link.classList.remove('text-blue-500');
                link.classList.add('text-gray-900');

            });
            this.classList.add('text-blue-500');
            link.classList.remove('text-gray-900');
        });
    });


    window.addEventListener('scroll', function () {
        let current = '';
        const sections = document.querySelectorAll('section');
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.scrollY >= (sectionTop - sectionHeight / 3)) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('text-blue-500');
            link.classList.add('text-gray-900');
            if (new URL(link.href).hash === '#' + current) {
                link.classList.add('text-blue-500');
                link.classList.remove('text-gray-900');
            }
        });
    });
}