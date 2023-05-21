/*
  This is the menu.js file, which contains JavaScript code for handling the menu functionality.
  It uses jQuery to interact with the DOM and handle events.
  The code toggles the visibility of menu links when the menu icon is clicked.
*/
$(document).ready(function () {
	// Event handler for menu icon click
	$("#menu-icon").click(function () {
	  $(".menu a").toggle();
	});
  });
  