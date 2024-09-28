import pyodbc
import os
import json


class Database:
    def __init__(self):
        server = os.getenv("DB_SERVER")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")

        self.conn = pyodbc.connect(
            'DRIVER={ODBC Driver 18 for SQL Server};SERVER=%s;DATABASE=%s;Trusted_Connection=yes;TrustServerCertificate=yes' % (server, db_name))

        self.cursor = self.conn.cursor()

    def get_user_by_id(self, user_id: int):
        self.cursor.execute(
            "SELECT * FROM Subscribers_mtbl where CUST_CODE = ?", user_id)
        row = self.cursor.fetchone()
        return row.CUST_FNAME

    def check_user_exists_by_email(self, email: str):
        self.cursor.execute(
            "SELECT * FROM Subscribers_mtbl where CUST_EMAIL = ?", email)
        row = self.cursor.fetchone()
        if row:
            return row.CUST_CODE
        return False

    def check_user_phone_given_email(self, email: str, phone: str):
        self.cursor.execute(
            "SELECT * FROM Subscribers_mtbl where CUST_EMAIL = ? AND CUST_MobileNo = ?", email, phone)
        row = self.cursor.fetchone()
        if row:
            return {
                "id": str(row.CUST_CODE),
                "fname": row.CUST_FNAME,
                "lname": row.CUST_LNAME,
                "nationality": str(row.CUST_NATIONALITY),
                "internationalCode": row.CUST_InternationalCode,
                "mobileNumber": row.CUST_MobileNo,
                "email": row.CUST_EMAIL,
                "gender": row.CUST_GENDER,
                "birthDate": str(row.CUST_BIRTHDATE),
                "allergy": row.CUST_ALERGY,
            }
        return False

    def insert_user(self, data: dict):
        birthdate = data['birthdate'].split("T")[0]
        gender = data['gender'][0].upper()
        nationalities = json.loads(open("data.json", 'r').read())[
            "NATIONALITIES"]

        for nationality in nationalities:
            if nationality["value"] == data['nationality']:
                nationality_id = nationality["_id"]

        print(data)

        params = (
            0,
            'QR_CODE_PLACEHOLDER',
            data['fname'],
            data['lname'],
            int(nationality_id),
            data['internationalCode'],
            data['mobileNumber'],
            data['email'].lower(),
            gender,
            birthdate,
            data['allergy']
        )

        self.cursor.execute("""
            EXEC dbo.Apply_Registration_SP 
                @mCUST_CODE = ?, 
                @mCUST_QRCODE = ?, 
                @mCUST_FNAME = ?, 
                @mCUST_LNAME = ?, 
                @mCUST_NATIONALITY = ?, 
                @mCUST_InternationalCode = ?, 
                @mCUST_MobileNo = ?, 
                @mCUST_EMAIL = ?, 
                @mCUST_GENDER = ?, 
                @mCUST_BIRTHDATE = ?, 
                @mCUST_ALERGY = ?
        """, params)

        self.conn.commit()
        return {"status": "User registered"}
