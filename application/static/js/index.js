$(document).ready(function () {
	// Start conversation with welcome message
	startMessage();
	getRecentMessages();
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
});

function startMessage() {
	// Loading animation
	var animation = `
            <div class="loading-messages">
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
                <div class="loading-dot"></div>
            </div>
            `;
	$("#messages-box").append(animation);

	// wait for 1 second
	function delay(time) {
		return new Promise((resolve) => setTimeout(resolve, time));
	}

	delay(1000).then(() => {
		$(".loading-messages").remove();
		$("#messages-box").append(
			"<div class='messages bot-messages'>" + 'Hi there, I am Monetize.ai - your personal financial chat bot advisor. I have access to the most recent, accurate and reliable financial data from Yahoo Finance to give you relevant financial information at a glance.' + "</div>"
		);
		$(".bot-messages").css("visibility", "visible");
	});
}

function sendQuery() {
	console.log("sending query");

	let input = $("#chat-input").val().trim();
	$("#chat-input").val("");

	if (input != "") {
		$("#messages-box").append(
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
	$("#messages-box").append(animation);

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
		$("#messages-box").append(
			"<div class='messages bot-messages'>" + data.response + "</div>"
		);
		$(".bot-messages").css("visibility", "visible");
	});
}

function getRecentMessages() {
	console.log("getting recent messages");
	$.get({
		method: "GET",
		url: "/get_messages",
		contentType: "application/json",
		dataType: "json",
	}).done(function (data) {
		console.log("finished getting recent messages");

		messagesLen = Object.keys(data.messages).length;

		userMessage = data.messages['0']['body'];
		if (userMessage != "") {
			$("#messages-box").append(
				"<div class='messages user-messages'>" + userMessage + "</div>"
			);
			$(".user-messages").css("visibility", "visible");
		}
		botMessage = data.messages['1']['body'];
		if (botMessage != "") {
			$("#messages-box").append(
				"<div class='messages bot-messages'>" + botMessage + "</div>"
			);
			$(".bot-messages").css("visibility", "visible");
		}
		userMessage = data.messages['2']['body'];
		if (userMessage != "") {
			$("#messages-box").append(
				"<div class='messages user-messages'>" + userMessage + "</div>"
			);
			$(".user-messages").css("visibility", "visible");
		}
		botMessage = data.messages['3']['body'];
		if (botMessage != "") {
			$("#messages-box").append(
				"<div class='messages bot-messages'>" + botMessage + "</div>"
			);
			$(".bot-messages").css("visibility", "visible");
		}
	});
}

function portfolio() {
	$.get("/portfolio", function (response) {
	});
}
