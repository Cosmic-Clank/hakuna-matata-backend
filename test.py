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

msg = MIMEText(f"Your OTP is: 111111")
msg['Subject'] = 'Your OTP Code'
msg['From'] = SENDER_EMAIL
msg['To'] = to_email

with smtplib.SMTP_SSL(SMTP_SERVER, int(SMTP_PORT)) as server:
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
    print(f"OTP sent to {to_email}")
