from flask import Flask, request, jsonify, send_file
import requests
from fpdf import FPDF
import os
from datetime import datetime
from flask_cors import CORS
import PyPDF2
from dotenv import load_dotenv
from openai import OpenAI
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import tiktoken

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

load_dotenv()

client = OpenAI()

# Twilio credentials
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def truncate_text(text, max_tokens=15000):
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)
    if len(tokens) > max_tokens:
        truncated_tokens = tokens[:max_tokens]
        return encoding.decode(truncated_tokens)
    return text

def summarize_text(text):
    truncated_text = truncate_text(text)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are Wasmi's enthusiastic colleague who loves sharing interesting articles. You are not cringe, not over enthusiastic and you keep it professional. Summarize the key points, focusing on important findings and discussions. Skip less important details like author names."},
            {"role": "user", "content": f"I just read this article and want to tell Wasmi about it:\n\n{truncated_text}\n\nSummarize it as if you're excitedly telling Wasmi about it."}
        ],
        max_tokens=250  # Increased for a more detailed summary
    )
    return response.choices[0].message.content

def send_whatsapp_message(to_number, message):
    try:
        message = twilio_client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{to_number}'
        )
        print(f"WhatsApp message sent: {message.sid}")
        return True
    except TwilioRestException as e:
        print(f"Twilio Error: {e.code} - {e.msg}")
        print(f"More info: {e.more_info}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return False

@app.route('/', methods=['POST'])
def index():
    return jsonify({"message": "Please use the /summarize endpoint"})

@app.route('/summarize', methods=['POST'])
def summarize():
    try:
        data = request.get_json()
        text = data.get('text')
        recipient_number = data.get('recipient_number', '+14384015660')  # Default number if not provided

        if not text:
            return jsonify({"error": "Missing text"}), 400

        summary = summarize_text(text)

        # Create a unique filename for the PDF summary
        current_date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        filename = f"summary-{current_date}.pdf"
        file_path = f"/Users/wasmi/Desktop/automations/articles-pdf/{filename}"

        # Create a PDF file with the summary
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, txt=summary)
        pdf.output(file_path)

        # Send WhatsApp message
        message_sent = send_whatsapp_message(recipient_number, summary)

        return jsonify({
            "message": "Summary created" + (" and sent via WhatsApp" if message_sent else ""),
            "summary": summary,
            "pdf_url": f"http://localhost:5000/download/{filename}"
        })

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = f"/Users/wasmi/Desktop/automations/articles-pdf/{filename}"
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5000)