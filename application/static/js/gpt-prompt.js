$(document).ready(function () {
	$("#prompt-button").click(function (event) {
		event.preventDefault();
		let input = $("#prompt-input").val();
		console.log(input);
		$.post({
			url: "http://127.0.0.1:8080/generate",
			data: JSON.stringify({ prompt: input }),
			contentType: "application/json",
			dataType: "json",
		}).done(function (data) {
			console.log("finished query");
			console.log(data);
			$("#generated-text").text(data.response);
		});
	});
});