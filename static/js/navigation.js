var activePage = function(link){
    var activeLink = $('#nav-wrap nav > a.active');
    var activeSecondary = null;
    var currentPage = activeLink.text();

    if (link) {
        activeLink = link;
        if (activeLink.parent().hasClass('secondary')) {
            currentPage = activeLink.parent().prev('.has-secondary').text();
        } else {
            currentPage = activeLink.text();
        }

        // change active classes
        if (!activeLink.hasClass('active')) {
            // remove all active classes
            $('nav:not(#secondary) a').removeClass('active');
            // add active class to link that was clicked
            activeLink.addClass('active');
            // add active class to link's parent if nested
            if (activeLink.parent().hasClass('secondary')) {
                activeLink.parent().prev('.has-secondary').addClass('active');
            }
            // add active class to first child if there are any
            if (activeLink.hasClass('has-secondary')) {
                activeLink.next('.secondary').find('a:first-child').addClass('active');
            }
        }
    }
    // populate current primary page text in mobile nav
    $('#current-page').text(currentPage);

    // populate desktop #secondary nav
    if (activeLink.hasClass('has-secondary')) {
        activeSecondary = activeLink.next('.secondary').html();
        $('#secondary').html(activeSecondary).show();
    }
    else if (activeLink.parent().hasClass('secondary')) {
        activeSecondary = activeLink.parent().html();
        $('#secondary').html(activeSecondary).show();
    }
    else {
        activeSecondary = null;
        $('#secondary').html(activeSecondary).hide();
    }
}

$(document).ready(function () {
    activePage();
    var sidebar = $('section#main').hasClass('sidebar');

    // change active nav item
    $('nav#utility, nav#primary').on('click', 'a', function() {
        activePage($(this));
    });
    $('nav#secondary').on('click', 'a', function() {
        if (!$(this).hasClass('active')) {
            // set active
            $(this).addClass('active').siblings('a').removeClass('active');
            // set mobile version active
            $('nav#utility, nav#primary').find('.secondary a').removeClass('active');
            $('nav#utility, nav#primary').find('.secondary a:contains("' + $(this).text() + '")').addClass('active');
        }
    });

    // show/hide primary children (secondary nav) for mobile
    $('nav a.has-secondary i').click(function(e){
        $(this).toggleClass('icons8-visible').toggleClass('icons8-hide');
        $(this).parent('a').next('.secondary').slideToggle(200);
        // stop parent link from going anywhere
        e.preventDefault();
        e.stopPropagation();
    });

    // Responsive actions
    $('i.icons8-menu').click(function() {
        var menuIcon = $(this);
        if (menuIcon.hasClass('icons8-menu')) {
            // icon
            menuIcon.fadeOut(200);
            setTimeout(function(){
                menuIcon.removeClass('icons8-menu').addClass('icons8-delete').fadeIn(200);
            }, 200);

            // current page
            $('#mobile-menu #current-page').css('opacity', 0);

            // navs
            $('#nav-wrap').slideDown(200);
            setTimeout(function(){
                $('#nav-wrap nav').css('opacity', 1);
            }, 200);
        } else if (menuIcon.hasClass('icons8-delete')) {
            // icon
            menuIcon.fadeOut(200);
            setTimeout(function(){
                menuIcon.removeClass('icons8-delete').addClass('icons8-menu').fadeIn(200);
            }, 200);

            // current page
            setTimeout(function(){
                $('#mobile-menu #current-page').css('opacity', 1);
            }, 200);

            // navs
            $('#nav-wrap nav').css('opacity', 0);
            setTimeout(function(){
                $('#nav-wrap').slideUp(200);
            }, 200);
        }
    });

    // window resize
    var windowWidth = $(window).width();
    $(window).resize(function() {
        // helps determine width increase or decrease
        var oldWidth = windowWidth;
        if ($(this).width() != windowWidth){
            windowWidth = $(this).width();
            var newWidth = windowWidth;
        }
        // go back to desktop styles
        if (windowWidth > 999) {
            // reset menu stuff
            $('#nav-wrap').css('display','table-cell');
            $('#nav-wrap nav').css('opacity', 1);
            $('#mobile-menu i').removeClass('icons8-delete').addClass('icons8-menu');
            $('.secondary').hide();
            $('a.has-secondary i').removeClass('icons8-hide').addClass('icons8-visible');
            if ($('#secondary').html() != '') {
                if (sidebar) {
                    $('#secondary').css('display','table-cell');
                } else {
                    $('#secondary').show();
                }
            }
        }
        // go to collapsed mobile styles
        else if (oldWidth >= 1000 && newWidth <= 999) {
            $('#nav-wrap').css('display','none');
            $('#nav-wrap nav').css('opacity', 0);
            $('#mobile-menu #current-page').css('opacity', 1);
        }
    });
});
