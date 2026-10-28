
from flask import Flask, request, render_template_string
import smtplib
import os
from email.message import EmailMessage

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Gmail Sender</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #dceeff, #e9ddff);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .card {
            background: white;
            padding: 30px;
            border-radius: 18px;
            width: 100%;
            max-width: 480px;
            box-shadow: 0 10px 35px #0002;
        }
        h1 { text-align: center; color: #4731a8; }
        p { color: #666; text-align: center; }
        label {
            display: block;
            margin-top: 15px;
            font-weight: bold;
        }
        input, textarea, button {
            width: 100%;
            padding: 12px;
            margin-top: 7px;
            border: 1px solid #ddd;
            border-radius: 8px;
            font-size: 15px;
        }
        textarea { resize: vertical; }
        button {
            margin-top: 20px;
            border: none;
            background: #6741d9;
            color: white;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover { background: #4c2bb5; }
        .message {
            padding: 12px;
            border-radius: 8px;
            background: #f0f0f0;
            overflow-wrap: anywhere;
        }
        .note { font-size: 13px; }
    </style>
</head>
<body>
<div class="card">
    <h1>✉ Gmail Sender</h1>
    <p>Send emails using Python and Flask</p>

    {% if message %}
        <div class="message">{{ message }}</div>
    {% endif %}

    <form method="POST">
        <label>Recipient Gmail / Email</label>
        <input type="email" name="recipient"
               placeholder="recipient@example.com" required>

        <label>Email Subject</label>
        <input type="text" name="subject"
               placeholder="Enter subject" required>

        <label>Your Message</label>
        <textarea name="body" rows="5"
                  placeholder="Write your email..." required></textarea>

        <button type="submit">Send Email</button>
    </form>

    <p class="note">
        Your Gmail credentials are read from environment variables,
        not from this web form.
    </p>
</div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    message = ""

    if request.method == "POST":
        recipient = request.form.get("recipient", "").strip()
        subject = request.form.get("subject", "").strip()
        body = request.form.get("body", "").strip()

        gmail_user = os.environ.get("GMAIL_ADDRESS")
        gmail_password = os.environ.get("GMAIL_APP_PASSWORD")

        if not gmail_user or not gmail_password:
            message = (
                "Configuration missing. Set GMAIL_ADDRESS and "
                "GMAIL_APP_PASSWORD environment variables."
            )
        else:
            try:
                email = EmailMessage()
                email["From"] = gmail_user
                email["To"] = recipient
                email["Subject"] = subject
                email.set_content(body)

                with smtplib.SMTP("smtp.gmail.com", 587, timeout=20) as server:
                    server.starttls()
                    server.login(gmail_user, gmail_password)
                    server.send_message(email)

                message = "Email sent successfully!"

            except (smtplib.SMTPException, OSError) as error:
                app.logger.exception("Email sending failed")
                message = "Email could not be sent. Check your Gmail settings."

    return render_template_string(HTML, message=message)


if __name__ == "__main__":
    app.run(debug=True)
