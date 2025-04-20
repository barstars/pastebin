async function send() {
	const text = document.getElementById("textInput").value;

	const response = await fetch("/add-text", {
		method: "POST",
		headers: {
			"Content-Type": "application/json"
		},
		body: JSON.stringify({ text: text })
	});

	if (!response.ok) {
		console.error("Ошибка при отправке запроса:", response.status);
		return;
	}

	const data = await response.json(); // только ОДИН раз
	const result = data.url;

	console.log(result);
	document.getElementById("result").innerHTML = `<a href="${result}" target="_blank">${result}</a>`;
}
