document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 JavaScript Loaded");

    const checkBtn = document.getElementById("checkBtn");
    const codeInput = document.getElementById("codeInput");
    const fileInput = document.getElementById("fileInput");
    const resultBox = document.getElementById("result-box");
    const resultText = document.getElementById("resultText");
    const loading = document.getElementById("loading");

    // ✅ Check if elements exist before using them
    if (!checkBtn || !codeInput || !resultBox || !resultText || !loading) {
        console.error("❌ Required elements missing in HTML!");
        return;
    }

    console.log("✅ Elements loaded successfully");

    // ✅ File Upload Handling
    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function (e) {
                codeInput.value = e.target.result;
            };
            reader.readAsText(file);
        }
    });

    // ✅ Submit Button Click Event
    checkBtn.addEventListener("click", async function (event) {
        event.preventDefault();  // ✅ Prevents form reload
        console.log("🚀 Submit button clicked!");

        const code = codeInput.value.trim();
        if (!code) {
            alert("⚠️ Please enter or upload code!");
            return;
        }

        // ✅ Show Loading Animation
        loading.style.display = "block";
        resultBox.style.display = "none";

        try {
            let response = await fetch("/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ code: code }),
            });

            // Check if the response is ok (status 200-299)
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }

            let data = await response.json();
            console.log("🔥 API Response:", data);

            loading.style.display = "none"; // ✅ Hide loading

            if (data.redirect) {
                window.location.href = data.redirect;  // ✅ Redirect to results page
            } else {
                resultBox.style.display = "block";
                resultText.innerHTML = `⚠️ Error processing request!`;
            }
        } catch (error) {
            console.error("Error:", error);
            resultBox.style.display = "block";
            resultText.innerHTML = "⚠️ Error processing request!";
            loading.style.display = "none";  // ✅ Ensure loading stops
        }
    });
});
