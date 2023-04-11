$(document).ready(function () {
	$.post({
		url: "http://127.0.0.1:8080/generate",
		data: JSON.stringify({query: "hello can you introduce yourself"}),
		contentType: "application/json",
		dataType: "json",
	}).done(function (data) {
		console.log(data);
		$("#generated-text").text(data.response);
	});
});
