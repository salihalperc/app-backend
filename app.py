from flask import Flask, request, jsonify
import smtplib
import os
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()  # .env dosyasından çevresel değişkenleri yükle

app = Flask(__name__)
CORS(app)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')
EMAIL_ADRESSS = os.getenv('EMAIL_TO')

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@app.route('/send-mail', methods=['POST'])
def send_mail():
    data = request.json
    message = data.get('message')

    subject = "Özür Mesajı"
    body = f"{message}"

    # UTF-8 destekli MIME mesajı oluştur
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESSS
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        return jsonify({"status": "success", "message": "Mail gönderildi"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run()
