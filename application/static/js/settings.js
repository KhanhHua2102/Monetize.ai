$(document).ready(function () {
	$(".api-key button").click(function (event) {
		event.preventDefault();
		apiKey = $(".api-key input").val().trim();
		updateKey(apiKey);
	});
});

function findApiKey(text) {
	const pattern = /([A-Za-z0-9]{32})/;
	const matches = text.match(pattern);
	if (matches) {
		return matches[0];
	} else {
		return null;
	}
}

function updateKey(apiKey) {
	// check if valid key
	if (!findApiKey(apiKey)) {
		// invalid key
		alert("Invalid API key");
		return false;
	}

	console.log("updating api key");
	$.post({
		url: "/update_openai_key",
		data: JSON.stringify({ key: apiKey }),
		contentType: "application/json",
		dataType: "json",
	}).done(function (data) {
		if (data.response === "success") {
			alert("OpenAI key updated");
			console.log("updated key");
			return true;
		} else {
			alert("Error updating OpenAI key");
			return false;
		}
	});
}
