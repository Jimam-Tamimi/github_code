
    $(document).ready(function () {
        $('#blogSlider').multislider({
            duration: 1000,
            // from 750
            interval: 3000
        });

    })




    $(document).ready(function () {
        $('#autoWidth').lightSlider({
            autoWidth: true,
            loop: true,
            onSliderLoad: function () {
                $('#autoWidth').removeClass('cS-hidden');
            }
        });
    });


    $(document).ready(function () {
        $('#autoWidth-2').lightSlider({
            autoWidth: true,
            loop: true,
            onSliderLoad: function () {
                $('#autoWidth-2').removeClass('cS-hidden');
            }
        });
    });

    $(document).ready(function () {
        $('#autoWidth-3').lightSlider({
            autoWidth: true,
            loop: true,
            onSliderLoad: function () {
                $('#autoWidth-3').removeClass('cS-hidden');
            }
        });
    });

    $(document).ready(function () {

        if ($(window).width() <= 768) {
            $('#modasty-features').css("display", "none");
            $('#section-services').css({
                "padding-top": "0",
                "padding-bottom": "30px"
            });
        }

    });

    $(document).ready(function () {

        if ($(window).width() > 768) {
            $('#modasty-features-small').css("display", "none");
        }
    });

    /* When the user clicks on the button,
    toggle between hiding and showing the dropdown content */
    function myFunction() {
        if ($(window).width() <= 768) {
            document.getElementById("myDropdown").classList.toggle("show");
        }
    }

    // Close the dropdown menu if the user clicks outside of it
    window.onclick = function (event) {
        if (!event.target.matches('.dropbtn')) {
            var dropdowns = document.getElementsByClassName("dropdown-content");
            var i;
            for (i = 0; i < dropdowns.length; i++) {
                var openDropdown = dropdowns[i];
                if (openDropdown.classList.contains('show')) {
                    openDropdown.classList.remove('show');
                }
            }
        }
    }


    $(document).ready(function(){
$('.customer-logos').slick({
slidesToShow: 6,
slidesToScroll: 1,
autoplay: true,
autoplaySpeed: 1000,
arrows: false,
dots: false,
pauseOnHover: false,
responsive: [{
  breakpoint: 768,
  settings: {
    slidesToShow: 4
  }
}, {
  breakpoint: 520,
  settings: {
    slidesToShow: 3
  }
}]
});
});



$(document).ready(function(){
$('.customer-logos').slick({
slidesToShow: 6,
slidesToScroll: 1,
autoplay: true,
autoplaySpeed: 1000,
arrows: false,
dots: false,
pauseOnHover: false,
responsive: [{
  breakpoint: 768,
  settings: {
    slidesToShow: 4
  }
}, {
  breakpoint: 520,
  settings: {
    slidesToShow: 3
  }
}]
});
});


$(document).ready(function(){

$(".Modern-Slider").slick({
autoplay:true,
autoplaySpeed:10000,
speed:600,
slidesToShow:1,
slidesToScroll:1,
pauseOnHover:false,
dots:true,
pauseOnDotsHover:true,
cssEase:'linear',
// fade:true,
draggable:false,
prevArrow:'<button class="PrevArrow"></button>',
nextArrow:'<button class="NextArrow"></button>', 
});

})


    $(document).ready(function(){
var docEl = $(document),
  headerEl = $('header'),
  headerWrapEl = $('.wrapHead'),
  navEl = $('nav'),
  linkScroll = $('.scroll');

docEl.on('scroll', function(){
if ( docEl.scrollTop() > 60 ){
  headerEl.addClass('fixed-to-top');
  headerWrapEl.addClass('fixed-to-top');
  navEl.addClass('fixed-to-top');
}
else {
  headerEl.removeClass('fixed-to-top');
  headerWrapEl.removeClass('fixed-to-top');
  navEl.removeClass('fixed-to-top');
}
});

//   linkScroll.click(function(e){
//       e.preventDefault();
//       $('body, html').animate({
//          scrollTop: $(this.hash).offset().top
//       }, 500);
//    });
});

function sticky_relocate() {
var window_top = $(window).scrollTop();
var div_top = $('#sticky-anchor').offset().top;
if (window_top > div_top) {
$('#sticky').addClass('stick');
} else {
$('#sticky').removeClass('stick');
}
}

$(function() {
$(window).scroll(sticky_relocate);
sticky_relocate();
});

var acordion = document.getElementsByClassName('accordion-12');

var i;
var len = acordion.length;
for(i = 0; i<len; i++){
acordion[i].addEventListener('click', function(){
    this.classList.toggle('active');
    var panal = this.nextElementSibling;
    if(panal.style.maxHeight){
        panal.style.maxHeight = null;
    }else{
        panal.style.maxHeight = panal.scrollHeight + 'px';
    }
})
}
