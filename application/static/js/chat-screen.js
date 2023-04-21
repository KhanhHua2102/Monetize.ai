$(document).ready(function () {
    // Toggle menu
    $('#menu-icon').click(function () {
        $('.menu button').toggle();
    });

    // Send message and receive response from gpt
    $("#submit-button")
			.click(function (event) {
                event.preventDefault();
                console.log("submit button clicked");
				sendQuery();
			});

    $("#chat-input")
			.on("keypress", function (event) {
                if (event.which === 13) {
                    event.preventDefault();
                    console.log("enter pressed");
					sendQuery();
				}
            });

	$("#portfolio")
			.click(function (event) {
                // event.preventDefault();
                console.log("portfolio page clicked");
				portfolio();
			});
});

function sendQuery() {
	console.log("sending query");

	let input = $("#chat-input").val().trim();
	$("#chat-input").val("");

	if (input != "") {
		$("section").append(
			"<div class='messages user-messages'>" + input + "</div>"
		);
		$(".user-messages").css("visibility", "visible");
	}
	console.log(input);

	// Loading animation
	var animation = `
            <div class="loading-messages">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
            `;
	$("section").append(animation);

	// Post request to gpt
	postRequest(input);
}

function postRequest(input) {
	console.log("posting request");
	$.post({
		url: "/generate",
		data: JSON.stringify({ prompt: input}),
		contentType: "application/json",
		dataType: "json",
	}).done(function (data) {
		console.log("finished query");
		console.log(data);
		$(".loading-messages").remove();
		$("section").append(
			"<div class='messages bot-messages'>" + data.response + "</div>"
		);
		$(".bot-messages").css("visibility", "visible");
	});
}

function portfolio() {
	$.get("/portfolio", function (response) {
	});
}
