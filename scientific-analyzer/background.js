chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === "sendText") {
      fetch("http://localhost:5000/summarize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: request.text }), // Convert request.text to JSON
      })
        .then((response) => response.json()) // Expect JSON response
        .then((data) => {
          chrome.runtime.sendMessage({ action: "textSent" });
          chrome.runtime.sendMessage({ action: "textReceived", summary: data.summary });
        });
    }
  });