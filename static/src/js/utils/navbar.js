export function initNav()  {
    // Handle click event on navbar links
    const navLinks = document.querySelectorAll('#navbar-menu a:not(.signin)');
    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            navLinks.forEach(link => {
                link.classList.remove('text-blue-500');
                link.classList.add('text-gray-900');
                // set to hidden element with id navbar-menu
                const navbarMenu = document.getElementById('navbar-menu');
                navbarMenu.classList.add('hidden'); 

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

    const navbarMenu = document.getElementById('navbar-menu');
    if (navbarMenu) {

        const navButton = document.getElementById('navbar-menu-button');

        // Toggle the navbar menu on button click
        navButton.addEventListener('click', function () {
            // This checks if the navbar is hidden and toggles the display
            navbarMenu.classList.toggle('hidden');
        });

        // Close the navbar menu when clicking outside of it
        document.addEventListener('click', function (event) {
            const isClickInsideMenu = navbarMenu.contains(event.target);
            const isClickOnButton = navButton.contains(event.target);

            if (!isClickInsideMenu && !isClickOnButton && !navbarMenu.classList.contains('hidden')) {
                navbarMenu.classList.add('hidden');
                
            }
        });
    }
    // close  the navbar user menu when the price modal is opened
    const priceModalButton = document.getElementById('plan_pricing_modal_button_navbar');
    if (priceModalButton) {
        const userDropdown = document.getElementById('user-dropdown');

         // Toggle the navbar menu on button click
         priceModalButton.addEventListener('click', function () {
            // This checks if the navbar is hidden and toggles the display
            userDropdown.classList.toggle('hidden');
        });

    }
    let modal;
   
    // set the modal menu element
    const pricingModalEl = document.getElementById('plan_pricing_modal');
    if (pricingModalEl) {

        // options with default values
        const options = {
            backdropClasses:
                'bg-gray-900/50 dark:bg-gray-900/80 fixed inset-0 z-[51]',
        };
        // instance options object
        const instanceOptions = {
            override: true
        };

        modal = new Modal(pricingModalEl, options, instanceOptions);
    }

    // setup all the buttons that open the modal
    const pricingModalButtons = document.querySelectorAll('[id^="plan_pricing_modal_button"]');
    if (pricingModalButtons) {
        // Iterate over each button and add the click event listener
        pricingModalButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                modal.show();
            });
        });
    }


    // set the modal for languages
    const languageModalEl = document.getElementById('language_modal');
    if (languageModalEl) {

        // options with default values
        const options = {
            backdropClasses:
                'bg-gray-900/50 dark:bg-gray-900/80 fixed inset-0 z-[51]',
        };
        // instance options object
        const instanceOptions = {
            override: true
        };

        modal = new Modal(languageModalEl, options, instanceOptions);
    }

    // setup all the buttons that open the modal
    const languageModalButtons = document.querySelectorAll('[id^="language_modal_button"]');
    if (languageModalButtons) {
        // Iterate over each button and add the click event listener
        languageModalButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                modal.show();
            });
        });
    }

    // init submit button of the language modal
    const languageSelectionButtons = document.querySelectorAll('.language-selection-button');
    languageSelectionButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            // get the language code from the button data-language attribute
            const languageCode = button.getAttribute('data-language');
            // set the language and submit the form
            document.getElementById('languageInput').value = languageCode;
            document.getElementById('languageForm').submit();
        });
    });


}