document.addEventListener("DOMContentLoaded", function () {
	const uploadQuestionPaperButton = document.getElementById(
		"upload-question-paper-button"
	);
	const uploadAnswerSheetsButton = document.getElementById(
		"upload-answer-sheets-button"
	);
	const startCheckingSheetsButton = document.getElementById(
		"start-checking-sheets-button"
	);
	const popupOverlay = document.getElementById("popup");
	const popupClose = document.querySelector(".popup-close");
	const popupText = document.getElementById("popup-text");
	const spinner = document.getElementById("spinner");

	// Function to show the popup with the appropriate message
	function showPopup(message, isSuccess = false) {
		popupText.textContent = message;
		popupOverlay.classList.remove("hidden"); // Show the popup
		popupText.classList.toggle("popup-success", isSuccess);
		popupText.classList.toggle("popup-error", !isSuccess);
		spinner.classList.add("hidden"); // Hide the spinner once the message is shown
		popupClose.classList.remove("hidden"); // Show the close button
	}

	// Function to hide the popup
	function hidePopup() {
		popupOverlay.classList.add("hidden");
	}

	// Handle the upload question paper button click
	uploadQuestionPaperButton.addEventListener("click", function () {
		const fileInput = document.getElementById("question-paper");
		if (!fileInput.files.length) {
			showPopup("Please select a file to upload.", false);
			return;
		}

		const formData = new FormData();
		formData.append("question-paper", fileInput.files[0]);

		const xhr = new XMLHttpRequest();
		xhr.open("POST", "/upload-question-paper", true);

		xhr.onload = function () {
			if (xhr.status >= 200 && xhr.status < 300) {
				const response = JSON.parse(xhr.responseText);
				if (response.success) {
					showPopup("Question Paper Successfully Uploaded!", true);
				} else {
					showPopup(
						"Error occurred, unable to upload question paper.",
						false
					);
				}
			} else {
				showPopup(
					"Error occurred, unable to upload question paper.",
					false
				);
			}
		};

		xhr.onerror = function () {
			showPopup(
				"Error occurred, unable to upload question paper.",
				false
			);
		};

		popupText.textContent = "Uploading Question Paper...";
		spinner.classList.remove("hidden"); // Show the spinner during upload
		popupClose.classList.add("hidden"); // Hide the close button during upload
		popupOverlay.classList.remove("hidden");
		xhr.send(formData);
	});

	// Handle the upload answer sheets button click
	uploadAnswerSheetsButton.addEventListener("click", function () {
		const fileInput = document.getElementById("answer-sheets");
		if (!fileInput.files.length) {
			showPopup("Please select answer sheets to upload.", false);
			return;
		}

		const formData = new FormData();
		for (const file of fileInput.files) {
			formData.append("answer-sheets[]", file);
		}

		const xhr = new XMLHttpRequest();
		xhr.open("POST", "/upload", true);

		xhr.onload = function () {
			if (xhr.status >= 200 && xhr.status < 300) {
				const response = JSON.parse(xhr.responseText);
				if (response.success) {
					showPopup("Answer Sheets Successfully Uploaded!", true);
				} else {
					showPopup(
						"Error occurred, unable to upload answer sheets.",
						false
					);
				}
			} else {
				showPopup(
					"Error occurred, unable to upload answer sheets.",
					false
				);
			}
		};

		xhr.onerror = function () {
			showPopup("Error occurred, unable to upload answer sheets.", false);
		};

		popupText.textContent = "Uploading Answer Sheets...";
		spinner.classList.remove("hidden"); // Show the spinner during upload
		popupClose.classList.add("hidden"); // Hide the close button during upload
		popupOverlay.classList.remove("hidden");
		xhr.send(formData);
	});

	// Handle the start checking sheets button click
	startCheckingSheetsButton.addEventListener("click", function () {
		const xhr = new XMLHttpRequest();
		xhr.open("POST", "/start-checking-sheets", true);

		xhr.onload = function () {
			if (xhr.status >= 200 && xhr.status < 300) {
				const response = JSON.parse(xhr.responseText);
				if (response.success) {
					showPopup("Successfully Evaluated Answer Sheets", true);
				} else {
					showPopup("An Error Occurred", false);
				}
			} else {
				showPopup("An Error Occurred", false);
			}
		};

		xhr.onerror = function () {
			showPopup("An Error Occurred", false);
		};

		popupText.textContent = "Processing Sheets...";
		spinner.classList.remove("hidden"); // Show the spinner during processing
		popupClose.classList.add("hidden"); // Hide the close button during processing
		popupOverlay.classList.remove("hidden");
		xhr.send();
	});

	// Handle popup close button click
	popupClose.addEventListener("click", hidePopup);

	// Ensure clicking outside the popup content also closes the popup
	popupOverlay.addEventListener("click", function (event) {
		if (event.target === popupOverlay) {
			hidePopup();
		}
	});
});

// Function to toggle visibility of Upload Answer Sheets button based on chosen method
function toggleUploadButton() {
	const uploadMethod = document.querySelector(
		'input[name="upload-method"]:checked'
	).value;
	const uploadCard = document.getElementById("upload-card");
	const scanCard = document.getElementById("scan-card");
	const uploadButton = document.getElementById("upload-answer-sheets-button");

	if (uploadMethod === "upload") {
		uploadCard.classList.remove("hidden");
		scanCard.classList.add("hidden");
		uploadButton.classList.remove("hidden");
	} else {
		uploadCard.classList.add("hidden");
		scanCard.classList.remove("hidden");
		uploadButton.classList.add("hidden");
	}
}
