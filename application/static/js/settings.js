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
	$("#openai-key").change(function () {
		console.log("changed to: ", $(this).val().trim());
		fieldChanged.push("openai-key");
	});

	$("#save-button").click(async function (event) {
		event.preventDefault();
		var success = true;

		try {
			for (const field of fieldChanged) {
				await updateField(field);
			}
		} catch (error) {
			console.log(error.message);
			alert(error.message);
			success = false;
		}

		if (success) {
			console.log("Update successful");
			alert("Update successful");
		}
	});

});

async function updateField(field) {
	var newValue = $("#" + field)
		.val()
		.trim();
	console.log(field, newValue);

	// validating api key
	if (field == "openai-key" && findApiKey(newValue) == null) {
		throw new Error("Invalid API key!");
	}

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

		return true;
	} else {
		throw new Error(response.error);
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

async function updateKey(apiKey) {
	// check if valid key
	if (!findApiKey(apiKey)) {
		// invalid key
		alert("Invalid API key");
		return false;
	}

	console.log("updating api key");
	var response = await $.post({
		url: "/update_openai_key",
		data: JSON.stringify({ key: apiKey }),
		contentType: "application/json",
		dataType: "json",
	});
	if (response.response === "success") {
		alert("OpenAI key updated");
		console.log("updated key");
		return true;
	} else {
		alert("Error updating OpenAI key");
		return false;
	}
}
