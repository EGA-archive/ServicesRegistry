// Add box-shadow to wll the form when the input is focused

$("#query-form > input").focus(function(){
    $(this).parent().addClass('active')
});

$("#query-form > input").focusout(function(){
    $(this).parent().removeClass('active')
});
