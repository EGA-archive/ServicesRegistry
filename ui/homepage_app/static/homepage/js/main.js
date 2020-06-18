// Add box-shadow to wll the form when the input is focused

$("#query-form > input").focus(function(){
    $(this).parent().addClass('active')
});

$("#query-form > input").focusout(function(){
    $(this).parent().removeClass('active')
});


// When the user scrolls down 50px from the top of the document, resize the header's font size
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
      console.log($("nav"))
    $("nav").addClass("small")
  } else {
    $("nav").removeClass("small")
  }
}