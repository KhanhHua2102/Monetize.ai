$(document).ready(function() {
    // Your jQuery code goes here
    $(".collapsible").click(function() {
        console.log("Clicked on collapsible element");

        $(this).toggleClass("active");
        var section = $(this).next();
        if (section.css("max-height") !== "0px") {
            section.css("max-height", "0px");
        } else {
            section.css("max-height", section.prop("scrollHeight") + "px");
        }
    });
});