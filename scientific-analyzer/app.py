from flask import Flask, request, jsonify, send_file
import requests
from fpdf import FPDF
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Set API key and endpoint
api_key = "Your-API-KEY"
endpoint = "https://api.openai.com/v1/chat/completions"

@app.route('/', methods=['POST'])
def index():
    return jsonify({"message": "Please use the /summarize endpoint"})

@app.route('/summarize', methods=['POST'])
def summarize():
    text = request.get_json()['text']

    # Set summarization prompt
    prompt = "Provide me a TLDR of this article. Your answer must have the following sections: 1. About the author(s) - not just their names, but do a websearch to tell me more about them, where the study was conducted, and date of publication. 2. TLDR. 3.Enumerate key findings. 4. Tell me about this paper as if you are a scientist that just read it and wants to discuss (whatever you see important as an expert) " + text

    # Set API request parameters
    params = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 1000,
        "top_p": 1.0
    }

    # Set API request headers
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Send API request
    response = requests.post(endpoint, json=params, headers=headers)

    if response.status_code == 200:
        # Get summary from response
        summary = response.json()["choices"][0]["message"]["content"]

        # Create a unique filename based on current date and time, and a counter
        current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        counter = 1
        while True:
            filename = f"summary-{current_date}-{counter}.pdf"
            file_path = f"/Users/wasmi/Desktop/automations/articles-pdf/{filename}"
            if not os.path.exists(file_path):
                break
            counter += 1

        # Create a PDF file
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)
        pdf.multi_cell(0, 10, txt=summary, align='L')
        pdf.output(file_path)

        # Return the URL for the generated PDF
        pdf_url = f"http://localhost:5000/download/{filename}"
        return jsonify({"message": "PDF generated successfully", "pdf_url": pdf_url})
    else:
        print("Error:", response.json())
        return jsonify({"error": "Failed to get LLM response"})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = f"/Users/wasmi/Desktop/automations/articles-pdf/{filename}"
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)