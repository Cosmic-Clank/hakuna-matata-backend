from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


# SMTP_SERVER = "smartidealtrading.com"
# SMTP_PORT = "465"
# SENDER_EMAIL = "sales@smartidealtrading.com"
# SENDER_PASSWORD = "AminaShafi@sales"
# to_email = "tayyabsajidq41321@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = "465"
SENDER_EMAIL = "info.hakunamatatauae@gmail.com"
SENDER_PASSWORD = "qwqx bzqd yygk aknn"
to_email = "tayyabsajidq41321@gmail.com"

otp = 11111
html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f9f9f9; color: #333;">
        <div style="max-width: 600px; margin: 20px auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #ffffff; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
            <h2 style="color: #fe5e00; text-align: center; margin-bottom: 20px;">Your OTP Code</h2>
            <p style="margin: 0 0 15px;">Hi there,</p>
            <p style="margin: 0 0 15px;">We're sending you a one-time password (OTP) to verify your account: 
                <span style="text-decoration: underline; font-weight: bold;">{to_email}</span>.
            </p>
            <p style="font-size: 24px; font-weight: bold; text-align: center; color: #fe5e00; margin: 20px 0;">{otp}</p>
            <p style="margin: 0 0 15px;">Please do not share this code with anyone.</p>
            <p style="margin: 0 0 15px;">Thank you for choosing our service!</p>
            <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            <p style="text-align: center; font-size: 12px; color: #777;">
                &copy; 2025 HakunaMatata supermarket app. All rights reserved.
            </p>
        </div>
    </body>
    </html>
"""


msg = MIMEMultipart("alternative")
msg['Subject'] = 'Your OTP Code'
msg['From'] = SENDER_EMAIL
msg['To'] = to_email

msg.attach(MIMEText(html_content, "html"))

with smtplib.SMTP_SSL(SMTP_SERVER, int(SMTP_PORT)) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    print(f"OTP sent to {to_email}")
