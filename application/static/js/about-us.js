/*
    This jQuery script adds collapsible functionality to elements with the class "collapsible".
    When a "collapsible" element is clicked, it toggles the "active" class on the clicked element and performs an animation to expand or collapse the next sibling element.

    The purpose of this script is to create collapsible sections or panels on a web page.
    When a collapsible element is clicked, it expands or collapses the associated section by adjusting the CSS property "max-height".
    If the section is already expanded (i.e., its max-height is not "0px"), the script collapses it by setting max-height to "0px".
    Otherwise, if the section is collapsed (max-height is "0px"), the script expands it by setting max-height to the scroll height of the section.

    This code should be placed within a <script> tag or a JavaScript file that is loaded after jQuery library.
*/
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