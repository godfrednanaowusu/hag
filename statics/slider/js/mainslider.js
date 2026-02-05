var screenHeight = $(window).height();
var calheight = 650;
var screenWidth = $(window).width() + 100;
var dimensions = screenWidth+", "+calheight;
// var dimensions = "1605, 600";

// alert(dimensions);

$(window).load(function(){
	$('.slider').fractionSlider({
		'slideTransition' : 'none', // default slide transition
		'slideTransitionSpeed' : 2000, // default slide transition time
		'slideEndAnimation' : true, // if set true, objects will transition out before next slide moves in      
		'position' : '0,0', // default position | should never be used
		'transitionIn' : 'left', // default in - transition
		'transitionOut' : 'left', // default out - transition
		'fullWidth' : false, // transition over the full width of the window
		'delay' : 0, // default delay for elements
		'timeout' : 2000, // default timeout before switching slides
		'speedIn' : 2500, // default in - transition speed
		'speedOut' : 1000, // default out - transition speed
		'easeIn' : 'easeOutExpo', // default easing in
		'easeOut' : 'easeOutCubic', // default easing out

		'controls' : true, // controls on/off
		'pager' : true, // pager inside of the slider on/off OR $('someselector') for a pager outside of the slider
		'autoChange' : false, // auto change slides
		'pauseOnHover' : true, // Pauses slider on hover (current step will still be completed)

		'backgroundAnimation' : false, // background animation
		'backgroundElement' : null, // element to animate | default fractionSlider element
		'backgroundX' : 500, // background animation x distance
		'backgroundY' : 500, // background animation y distance
		'backgroundSpeed' : 2500, // default background animation speed
		'backgroundEase' : 'easeOutCubic', // default background animation easing

		'responsive' : true, // responsive slider (see below for some implementation tipps)
		'increase' : true, // if set, slider is allowed to get bigger than basic dimensions
		'dimensions' : dimensions, 
		/* IMPORTANT:
		if you use the responsive option, you have to set dimensions to the origin (width,height) in px
		you use for data-position,heights of elements, etc. */

		'startCallback' : null, // callbacks, see below for more information on callbacks
		'startNextSlideCallback' : null,
		'stopCallback' : null,
		'pauseCallback' : null,
		'resumeCallback' : null,
		'nextSlideCallback' : null,
		'prevSlideCallback' : null,
		'pagerCallback' : null

	});

});





