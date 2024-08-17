(function($){
    $(document).ready(function() {
        var navbar = $('.navbar-custom');
        var navHeight = navbar.height();

        // Trigger the animation on scroll
        $(window).scroll(function() {
            navbarAnimation(navbar, navHeight);
        });

        // Initial check on page load
        navbarAnimation(navbar, navHeight);

        function navbarAnimation(navbar, navHeight) {
            var topScroll = $(window).scrollTop();
            if (navbar.length > 0) {
                if (topScroll >= navHeight) {
                    navbar.removeClass('navbar-transparent').css('background-color', 'rgba(10, 10, 10, 0.9)').fadeIn();
                } else {
                    navbar.addClass('navbar-transparent').css('background-color', 'transparent').fadeIn();
                }
            }
        }
    });
})(jQuery);
