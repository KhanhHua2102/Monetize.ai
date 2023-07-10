$(document).ready(function () {
	var fieldChanged = [];
	$("#name").change(function () {
		console.log("changed to: ", $(this).val().trim());
		fieldChanged.push("name");
	});
	$("#email").change(function () {
		console.log("changed to: ", $(this).val().trim());
		fieldChanged.push("email");
	});
	$("#phone").change(function () {
		console.log("changed to: ", $(this).val().trim());
		fieldChanged.push("phone");
	});

	$("#save-button").click(function (event) {
		event.preventDefault();
		fieldChanged.forEach((field) => {
			updateField(field);
		});
		alert("Update successfully");
		// apiKey = $("#openai-key").val().trim();
		// updateKey(apiKey);
	});
});

async function updateField(field) {
	var newValue = $("#" + field)
		.val()
		.trim();
	console.log(field, newValue);

	response = await $.post({
		url: "/update_field",
		data: JSON.stringify({ field: field, newValue: newValue }),
		contentType: "application/json",
		dataType: "json",
	});

	if (response.response === "success") {
		// if the updated field is an email, update browser cookie
		if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(newValue)) {
			document.cookie = "email=" + newValue;
			console.log("udpated cookie");
		}

		console.log("Update successfully");
		return true;
	} else {
		return false;
	}
}

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
