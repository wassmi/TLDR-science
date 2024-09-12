function extractText() {
    return document.body.innerText;
  }
  
  chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
    if (request.action === "extractText") {
      const text = extractText();
      chrome.runtime.sendMessage({ action: "textExtracted", text });
    }
  });