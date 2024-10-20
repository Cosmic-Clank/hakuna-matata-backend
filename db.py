import pyodbc
import os
import json


class Database:
    def __init__(self):
        server = os.getenv("DB_SERVER")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")

        connection_string = 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s;TrustServerCertificate=yes' % (
            server, db_name, user, password)
        # print(connection_string)

        self.conn = pyodbc.connect(connection_string)

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
        if phone[0] != "0":
            phone = "0" + phone
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
        birthDate = data['birthDate'].split("T")[0]
        gender = data['gender'][0].upper()
        nationalities = json.loads(open("data.json", 'r').read())[
            "NATIONALITIES"]

        for nationality in nationalities:
            if nationality["value"] == data['nationality']:
                nationality_id = nationality["_id"]

        mobileNumber = data['mobileNumber']
        if mobileNumber[0] != "0":
            mobileNumber = "0" + mobileNumber

        params = (
            0,
            'QR_CODE_PLACEHOLDER',
            data['fname'],
            data['lname'],
            int(nationality_id),
            data['internationalCode'],
            mobileNumber,
            data['email'].lower(),
            gender,
            birthDate,
            data['allergy']
        )
        print("REGISTERING USER", params)

        self.cursor.execute("""
            EXEC dbo.Apply_Registraion_SP 
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

    def update_user_allergies(self, user_id: int, new_allergy: str):
        self.cursor.execute(
            "UPDATE Subscribers_mtbl SET CUST_ALERGY = ? WHERE CUST_CODE = ?", new_allergy, user_id)
        self.conn.commit()
        return {"status": "User allergy updated"}

    def update_user_birthdate(self, user_id: int, new_birthdate: str):
        self.cursor.execute(
            "UPDATE Subscribers_mtbl SET CUST_BIRTHDATE = ? WHERE CUST_CODE = ?", new_birthdate, user_id)
        self.conn.commit()
        return {"status": "User birthdate updated"}

    def get_sales_counter(self, user_id: str):
        self.cursor.execute(
            "SELECT * FROM Subscribers_mtbl where CUST_CODE = ?", user_id)
        row = self.cursor.fetchone()
        return row.CUST_COUNTER

    def update_profile(self, user_id: str, data: dict):
        print(data)
        id = user_id
        birthDate = data['birthDate'].split("T")[0]
        allergy = data['allergy']
        fname = data['fname']
        lname = data['lname']
        gender = data["gender"][0].upper()

        self.cursor.execute(
            "UPDATE Subscribers_mtbl SET CUST_FNAME = ?, CUST_LNAME = ?, CUST_BIRTHDATE = ?, CUST_ALERGY = ?, CUST_GENDER = ? WHERE CUST_CODE = ?", fname, lname, birthDate, allergy, gender, id)
        return {"status": "User profile updated"}
