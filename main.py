from fastapi import FastAPI
from dotenv import load_dotenv
import json
import os
import db
load_dotenv()

app = FastAPI()
database = db.Database()


@app.get("/get-user-by-id/{user_id}")
def get_user_by_id(user_id: int):
    return {"name": database.get_user_by_id(user_id)}


@app.post("/register")
def register_user(user_data: dict):
    if not database.check_user_exists_by_email(user_data['email']):
        database.insert_user(user_data)
        return {"status": "success", "statusCode": 201, "message": "User registered successfully"}
    else:
        return {"status": "fail", "statusCode": 209, "message": "User already exists"}


@app.post("/login")
def login_user(user_data: dict):
    if database.check_user_exists_by_email(user_data['email']):
        CUST_DATA = database.check_user_phone_given_email(
            user_data['email'], user_data['mobileNumber'])
        if CUST_DATA:
            return {"status": "success", "statusCode": 200, "message": "User logged in successfully", "data": CUST_DATA}
        else:
            return {"status": "fail", "statusCode": 401, "message": "Invalid credentials"}
    else:
        return {"status": "fail", "statusCode": 404, "message": "User not found"}


@app.get("/")
def health_check():
    return {"status": "ok"}
