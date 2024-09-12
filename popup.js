let extractionInProgress = false;

document.addEventListener("DOMContentLoaded", function () {
  const extractBtn = document.getElementById("extract-btn");
  extractBtn.addEventListener("click", function () {
    if (!extractionInProgress) {
      extractionInProgress = true;
      // Change button appearance to indicate it was clicked
      extractBtn.style.backgroundColor = "#808080";
      extractBtn.style.cursor = "default";
      chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, { action: "extractText" });
        document.getElementById("step-1").style.display = "block";
      });
    }
  });
});

chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === "textExtracted") {
      document.getElementById("step-2").style.display = "block";
      document.getElementById("step-1").style.display = "none";
      chrome.runtime.sendMessage({ action: "sendText", text: request.text });
    } else if (request.action === "textSent") {
      document.getElementById("step-3").style.display = "block";
      document.getElementById("step-2").style.display = "none";
    } else if (request.action === "textReceived") {
      document.getElementById("step-4").style.display = "block";
      document.getElementById("step-3").style.display = "none";
      extractionInProgress = false;
      // Reset button appearance when extraction is complete
      const extractBtn = document.getElementById("extract-btn");
      extractBtn.style.backgroundColor = "";
      extractBtn.style.cursor = "pointer";
    } else if (request.action === "pdfReady") {
      // Create and display the download link
      const downloadLink = document.createElement("a");
      downloadLink.href = request.pdfUrl;
      downloadLink.download = "extracted_text.pdf";
      downloadLink.textContent = "Download PDF";
      downloadLink.className = "download-link";
      
      const downloadContainer = document.getElementById("download-container");
      downloadContainer.innerHTML = ""; // Clear any existing content
      downloadContainer.appendChild(downloadLink);
      downloadContainer.style.display = "block";
    }
  });