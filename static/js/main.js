

// Examples

var examplesButton = $("#examples-button");
var examplesButtonText = $("#examples-button p");
var examples = $("#examples");

examplesButton.on("click", function(){
    examplesButtonText.toggleClass("active");
    examples.toggleClass("active");
});