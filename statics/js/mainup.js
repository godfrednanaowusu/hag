$(document).ready(function (e) {

    $('.scrollitem').click(function (e) {
        $this = $(this);
        var show = $this.attr('href');
        $('html, body').animate({
            scrollTop: $(show).offset().top - 80
        },
            1000
        );
        $('#mobilvenav').hide();

        e.preventDefault();
    });

    // $(".alert.alert-success").delay(4000).slideUp(200, function() {
    //     $(this).alert('close');
    // });

    // $(".alert.alert-info").delay(4000).slideUp(200, function() {
    //     $(this).alert('close');
    // });

});

//Check to see if the window is top if not then display button
$(window).scroll(function () {

    if ($(this).scrollTop() > 100) {
        // $('#mainlogo').attr({'src': '/static/images/toplogo_white.png'});
        // $('#header').css({'background': '#fff', 'border-bottom':'1px solid #ddd'});
        // $('.subheader').css({'background': '#fff'});
        //     $('#mainnav ul li a').css({'color': '#009cde'});
        //     $('#menubutton').css({'color': '#009cde'});     
        //     $('.loginbut').css({'color':'#009cde', 'border':'1px solid #009cde' }); 
        //     $('.registerbut').css({'background':'#009cde', 'color':'#fff'});      
    }

    else {
        // $('#mainlogo').attr({'src': '/static/images/toplogo.png'});
        //     $('#header').css({'background': 'none', 'border-bottom':'none'});
        // $('.subheader').css({'background': 'rgba(255, 255, 255,1)'});  
        //     $('#mainnav ul li a').css({'color': '#fff'});  
        //     $('#menubutton').css({'color': '#fff'}); 
        //     $('.loginbut').css({'color':'#fff', 'border':'1px solid #fff'}); 
        //     $('.registerbut').css({'background':'#fff', 'color':'#009cde'});        
    }

    if ($(this).scrollTop() > 760) {

        $('.scrollToTop').fadeIn();
        //$('#topheader, #topheader_overlay').animate({height: "60px"},"slow");

    }

    else {
        $('.scrollToTop').fadeOut();

    }

});


$(document).click(function (e) {
    var elem = $(e.target).attr('id');
    var elem2 = $(e.target).attr('class');

    if (elem != 'menubutton' && elem2 != 'naviconspan') {
        $('#mobilenav').slideUp();
        $('#nav-icon2').removeClass('open');

    }
    e.stopPropagation();


});

function toggleMobileMenu() {

    //$("#mobilenav").slideToggle();
    if ($('#mobilenav').is(':hidden')) {
        $('#mobilenav').slideDown();
        $('#nav-icon2').addClass('open');
        // $('#mobilenav').animate({'right':'0px'});
        // setTimeout(function() { $('#mobilenav').animate({'right':'-20px'});   }, 100);
    }

    else if ($('#mobilenav').is(':visible')) {
        $('#mobilenav').slideUp();
        $('#nav-icon2').removeClass('open');
        // $('#mobilenav').animate({'right':'0px'});
        // setTimeout(function() { $('#mobilenav').animate({'right':'-500px'}); /*$('#header').hide();*/   }, 100);
        // setTimeout(function() { $('#mobilenav').hide();   }, 500);	  
    }

}

//Click event to scroll to top
function scrolltothetopsmoothly() {
    $('html, body').animate({ scrollTop: 0 }, 800);
    return false;
}