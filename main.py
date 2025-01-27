from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
import db
import util

load_dotenv()

app = FastAPI()
database = db.Database()


@app.get("/get-user-by-id/{user_id}")
def get_user_by_id(user_id: int):
    return {"name": database.get_user_by_id(user_id)}


@app.post("/register")
def register_user(user_data: dict):  # fname, lname, email, password, terms
    CUST_DATA = database.get_user_by_email(user_data['email'])
    if not CUST_DATA:
        success = database.register_user(user_data)
        if success:
            print("User registered successfully", user_data)
            return {"status": "success", "statusCode": 201, "message": "Registeration successfully", "cust_data": user_data}
        else:
            print("Invalid data", user_data)
            return {"status": "fail", "statusCode": 400, "message": "Invalid data entered"}
    elif bool(CUST_DATA["CUST_DELETED"]):
        print("This account has been deleted. Please use another account.", user_data)
        return {"status": "fail", "statusCode": 209, "message": "This account has been deleted. Please use another account."}
    else:
        print("User already exists", user_data)
        return {"status": "fail", "statusCode": 209, "message": "User already exists, please login"}


@app.post("/login")
def login_user(user_data: dict):  # email, password
    CUST_DATA = database.get_user_by_email(user_data['email'])
    print(CUST_DATA)

    if CUST_DATA:
        if CUST_DATA["CUST_DELETED"]:
            print("This account has been deleted. Please use another account.", user_data)
            return {"status": "fail", "statusCode": 209, "message": "This account has been deleted. Please use another account."}

        if util.check_password(user_data['password'], CUST_DATA['CUST_PASSWORD']):
            print("User logged in successfully", CUST_DATA)
            return {"status": "success", "statusCode": 200, "message": "User logged in successfully", "cust_data": CUST_DATA}
        else:
            print("Invalid credentials", user_data)
            return {"status": "fail", "statusCode": 401, "message": "Invalid credentials"}
    else:
        print("User not found", user_data)
        return {"status": "fail", "statusCode": 404, "message": "User not found, please register first"}


@app.get("/get-sales-counter/{user_id}")
def get_sales_counter(user_id: str):
    return {"counter": database.get_sales_counter(user_id)}


@app.put("/update-user-profile/{user_id}")
def update_profile(user_id: str, data: dict):  # newValue, selectedKey
    print(data)
    if not data:
        print("Invalid data", data)
        return {"status": "fail", "statusCode": 400, "message": "Invalid data entered"}
    if not user_id:
        print("Invalid user_id", user_id)
        return {"status": "fail", "statusCode": 400, "message": "Invalid user_id entered"}
    database.update_profile_data(
        user_id, data["selectedKey"], data["newValue"])
    print("Profile updated successfully", {"user_id": user_id, "data": data})
    return {"status": "success", "statusCode": 200, "message": "Profile updated successfully"}


@app.get("/get-user-data/{code}")
def get_user_data(code: str):
    return {"status": "success", "statusCode": 200, "message": "User Data fetched successfully", "userData": database.get_user_by_code(code)}


@app.delete("/delete-user/{user_id}")
def delete_user(user_id: str):
    if not user_id:
        print("Invalid user_id", user_id)
        return {"status": "fail", "statusCode": 400, "message": "Invalid user_id entered"}
    if database.delete_user(user_id):
        print("User deleted successfully", user_id)
        return {"status": "success", "statusCode": 200, "message": "User deleted successfully"}
    else:
        print("User not found", user_id)
        return {"status": "fail", "statusCode": 404, "message": "User not found"}


def send_email(to_email: str, otp: str):
    smtp_server = os.getenv("SMTP_SERVER")
    port = os.getenv("SMTP_PORT")
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

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
    msg['From'] = sender_email
    msg['To'] = to_email
    msg.attach(MIMEText(html_content, "html"))

    try:
        with smtplib.SMTP_SSL(smtp_server, int(port)) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"OTP sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send OTP email")


class OTPRequest(BaseModel):
    email: str
    otp: str  # The frontend will pass the generated OTP


@app.post("/send-otp")
def send_otp(data: OTPRequest):  # email, otp
    send_email(data.email, data.otp)
    return {"status": "success", "statusCode": 201, "message": "OTP sent successfully"}


@app.get("/")
def health_check():
    return {"status": "ok"}
