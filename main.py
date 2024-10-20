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
        print("User registered successfully", user_data)
        return {"status": "success", "statusCode": 201, "message": "User registered successfully"}
    else:
        print("User already exists", user_data)
        return {"status": "fail", "statusCode": 209, "message": "User already exists"}


@app.post("/login")
def login_user(user_data: dict):
    if database.check_user_exists_by_email(user_data['email']):
        CUST_DATA = database.check_user_phone_given_email(
            user_data['email'], user_data['mobileNumber'])
        if CUST_DATA:
            print("User logged in successfully", CUST_DATA)
            return {"status": "success", "statusCode": 200, "message": "User logged in successfully", "data": CUST_DATA}
        else:
            print("Invalid credentials", user_data)
            return {"status": "fail", "statusCode": 401, "message": "Invalid credentials"}
    else:
        print("User not found", user_data)
        return {"status": "fail", "statusCode": 404, "message": "User not found"}


@app.put("/update-user-allergies/{user_id}")
def update_allergies(user_id: str, allergies: dict):
    if database.get_user_by_id(user_id):
        database.update_user_allergies(user_id, allergies["allergies"])
        print("Allergies updated successfully", {
              "user_id": user_id, "allergies": allergies})
        return {"status": "success", "statusCode": 200, "message": "Allergies updated successfully"}
    else:
        print("User not found", {"user_id": user_id})
        return {"status": "fail", "statusCode": 404, "message": "User not found"}


@app.put("/update-user-birthdate/{id}")
def update_birthdate(id: str, birthdate: dict):
    if database.get_user_by_id(id):
        database.update_user_birthdate(
            id, birthdate["birthDate"].split("T")[0])
        print("Birthdate updated successfully", {
              "user_id": id, "birthdate": birthdate})
        return {"status": "success", "statusCode": 200, "message": "Birthdate updated successfully"}
    else:
        print("User not found", {"user_id": id})
        return {"status": "fail", "statusCode": 404, "message": "User not found"}


@app.get("/get-sales-counter/{user_id}")
def get_sales_counter(user_id: str):
    return {"counter": database.get_sales_counter(user_id)}


@app.put("/update-user-profile/{user_id}")
def update_profile(user_id: str, data: dict):
    if database.get_user_by_id(user_id):
        database.update_profile(user_id, data)
        print("Profile updated successfully", {
              "user_id": user_id, "data": data})
        return {"status": "success", "statusCode": 200, "message": "Profile updated successfully"}
    else:
        print("User not found", {"user_id": user_id})
        return {"status": "fail", "statusCode": 404, "message": "User not found"}


@app.get("/")
def health_check():
    return {"status": "ok"}
