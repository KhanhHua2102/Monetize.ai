/**
 * @fileoverview This file contains all client-side functions for the menu.
 */
$(document).ready(function () {
	// Toggle side menu for portfolio page and mobile interface when menu icon is clicked
	$("#menu-icon").click(function () {
		$(".menu a").toggle();
	});
});
