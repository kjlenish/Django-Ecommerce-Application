(function($){
    $(document).ready(function() {
        // Navbar animation on scroll
        var navbar = $('.navbar-custom');
        var navHeight = navbar.height();

        $(window).on('scroll', function() {
            navbarAnimation(navbar, navHeight);
        });

        navbarAnimation(navbar, navHeight);

        function navbarAnimation(navbar, navHeight) {
            var topScroll = $(window).scrollTop();
            if (topScroll >= navHeight) {
                navbar.removeClass('navbar-transparent')
                      .css('background-color', 'rgba(10, 10, 10, 0.9)')
                      .fadeIn();
            } else {
                navbar.addClass('navbar-transparent')
                      .css('background-color', 'transparent')
                      .fadeIn();
            }
        }

        // Image switching functionality
        const mainImage = document.getElementById('main-image');
        const thumbnails = document.querySelectorAll('.product-gallery .thumbnail');

        thumbnails.forEach(function(thumbnail) {
            thumbnail.addEventListener('click', function(event) {
                event.preventDefault();
                
                // Get the image URL from the clicked thumbnail
                const newImageUrl = thumbnail.getAttribute('data-image-url');
                
                if (newImageUrl) {
                    // Update the main image source
                    mainImage.setAttribute('src', newImageUrl);

                    // Remove the 'active' class from all thumbnails
                    thumbnails.forEach(function(thumb) {
                        thumb.querySelector('img').classList.remove('active');
                    });

                    // Add the 'active' class to the clicked thumbnail
                    thumbnail.querySelector('img').classList.add('active');
                } else {
                    console.error("Image URL is not found!");
                }
            });
        });
    });
})(jQuery);
