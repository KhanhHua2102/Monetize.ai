const form = document.querySelector("#prompt-form");
const generatedText = document.querySelector("#generated-text");

form.addEventListener("submit", async function (event) {
	event.preventDefault();
	const formData = new FormData(form);
	const response = await fetch("/generate", {
		method: "POST",
		body: formData,
	});
	const data = await response.json();
	generatedText.innerText = data.text;
});
