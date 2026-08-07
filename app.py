import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Firm Details
FIRM_DATA = {
    "name": "ONE TRADE",
    "address": "Bijwar, Sitapur, UP, 261001",
    "mobile": "+91-9795650090",
    "whatsapp": "919795650090",
    "category": "Building Material",
    "products": ["TMT Fe 550 Sariya", "TMT Fe 550D Sariya"],
    "brands": [
        "OMPL", "GOVINDA", "MAZBOOT", "RUNGTA", "RASHMI", "POWERPLUS",
        "SKY", "MARUTI", "GALLANT", "ANKUR", "KAMDHENU", "TATA TISCON",
        "JSW", "JSW Neosteel", "SAIL", "APOLLO", "APOLLO TMT", "JINDAL"
    ],
    "target_audience": [
        {"name": "Contractors", "icon": "fa-helmet-safety", "bg": "bg-sky-200 text-sky-900"},
        {"name": "Builders", "icon": "fa-city", "bg": "bg-sky-300 text-sky-950"},
        {"name": "End Consumers", "icon": "fa-house-chimney", "bg": "bg-teal-200 text-teal-900"},
        {"name": "Retailers & Wholesalers", "icon": "fa-cart-shopping", "bg": "bg-emerald-200 text-emerald-950"},
        {"name": "Architects & Engineers", "icon": "fa-compass-drafting", "bg": "bg-teal-300 text-teal-950"},
        {"name": "Masons", "icon": "fa-trowel-bricks", "bg": "bg-amber-200 text-amber-950"}
    ]
}

# SMTP Email Configuration (Set via Environment Variables or direct credentials)
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_app_password")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "onetrade.sitapur@gmail.com")

def send_email_notification(name, contact, inquiry_type, message):
    """Sends an email notification via SMTP when a new inquiry arrives."""
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f"New Inquiry from {name} - ONE TRADE"

        body = f"""
        New Lead Received for ONE TRADE:

        Name: {name}
        Contact (Email/Phone): {contact}
        Inquiry Type: {inquiry_type}
        Message: {message}

        Address: Bijwar, Sitapur, UP, 261001
        """
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"SMTP Email Error (Check App Password/Settings): {e}")
        return False

@app.route('/')
def home():
    return render_template('index.html', data=FIRM_DATA)

@app.route('/api/inquiry', methods=['POST'])
def handle_inquiry():
    data = request.json or {}
    name = data.get('name', 'N/A')
    contact = data.get('contact', 'N/A')
    inquiry_type = data.get('inquiryType', 'General Quote')
    message = data.get('message', '')

    # Dispatch Email Notification
    email_sent = send_email_notification(name, contact, inquiry_type, message)

    return jsonify({
        "status": "success",
        "email_sent": email_sent,
        "message": "Inquiry recorded successfully."
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)