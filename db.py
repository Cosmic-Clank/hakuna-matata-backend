import pymssql
import os
import json


class Database:
    def __init__(self):
        server = os.getenv("DB_SERVER")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")
        db_name = os.getenv("DB_NAME")

        # Connect to the database
        self.conn = pymssql.connect(
            server=server,
            user=user,
            password=password,
            database=db_name,
            as_dict=True
        )
        self.cursor = self.conn.cursor()

    def get_user_by_id(self, user_id: int):
        self.cursor.execute(
            "SELECT * FROM Subscribers_mtbl WHERE CUST_CODE = %s", (user_id,)
        )
        row = self.cursor.fetchone()
        return row["CUST_FNAME"] if row else None

    def check_user_exists_by_email(self, email: str):
        self.cursor.execute(
            "SELECT * FROM Subscribers_mtbl WHERE CUST_EMAIL = %s", (email,)
        )
        row = self.cursor.fetchone()
        return row["CUST_CODE"] if row else False

    def check_user_phone_given_email(self, email: str, phone: str):
        if phone[0] != "0":
            phone = "0" + phone

        self.cursor.execute(
            "SELECT * FROM Subscribers_mtbl WHERE CUST_EMAIL = %s AND CUST_MobileNo = %s", (
                email, phone)
        )
        row = self.cursor.fetchone()
        if row:
            return {
                "id": str(row["CUST_CODE"]),
                "fname": row["CUST_FNAME"],
                "lname": row["CUST_LNAME"],
                "nationality": str(row["CUST_NATIONALITY"]),
                "internationalCode": row["CUST_InternationalCode"],
                "mobileNumber": row["CUST_MobileNo"],
                "email": row["CUST_EMAIL"],
                "gender": row["CUST_GENDER"],
                "birthDate": str(row["CUST_BIRTHDATE"]),
                "allergy": row["CUST_ALERGY"],
            }
        return False

    def insert_user(self, data: dict):
        birth_date = data['birthDate'].split("T")[0]
        gender = data['gender'][0].upper()
        nationalities = json.loads(open("data.json", 'r').read())[
            "NATIONALITIES"]

        nationality_id = None
        for nationality in nationalities:
            if nationality["value"] == data['nationality']:
                nationality_id = nationality["_id"]
                break

        mobile_number = data['mobileNumber']
        if mobile_number[0] != "0":
            mobile_number = "0" + mobile_number

        params = (
            0,
            'QR_CODE_PLACEHOLDER',
            data['fname'],
            data['lname'],
            int(nationality_id),
            data['internationalCode'],
            mobile_number,
            data['email'].lower(),
            gender,
            birth_date,
            data['allergy']
        )

        print("REGISTERING USER", params)

        self.cursor.execute(
            """
            EXEC dbo.Apply_Registraion_SP 
                @mCUST_CODE = %s, 
                @mCUST_QRCODE = %s, 
                @mCUST_FNAME = %s, 
                @mCUST_LNAME = %s, 
                @mCUST_NATIONALITY = %s, 
                @mCUST_InternationalCode = %s, 
                @mCUST_MobileNo = %s, 
                @mCUST_EMAIL = %s, 
                @mCUST_GENDER = %s, 
                @mCUST_BIRTHDATE = %s, 
                @mCUST_ALERGY = %s
            """,
            params
        )

        self.conn.commit()
        return {"status": "User registered"}

    def update_user_allergies(self, user_id: int, new_allergy: str):
        self.cursor.execute(
            "UPDATE Subscribers_mtbl SET CUST_ALERGY = %s WHERE CUST_CODE = %s", (
                new_allergy, user_id)
        )
        self.conn.commit()
        return {"status": "User allergy updated"}

    def update_user_birthdate(self, user_id: int, new_birthdate: str):
        self.cursor.execute(
            "UPDATE Subscribers_mtbl SET CUST_BIRTHDATE = %s WHERE CUST_CODE = %s", (
                new_birthdate, user_id)
        )
        self.conn.commit()
        return {"status": "User birthdate updated"}

    def get_sales_counter(self, user_id: str):
        self.cursor.execute(
            "SELECT CUST_COUNTER FROM Subscribers_mtbl WHERE CUST_CODE = %s", (
                user_id,)
        )
        row = self.cursor.fetchone()
        return row["CUST_COUNTER"] if row else None

    def update_profile(self, user_id: str, data: dict):
        print(data)
        birth_date = data['birthDate'].split("T")[0]
        allergy = data['allergy']
        fname = data['fname']
        lname = data['lname']
        gender = data['gender'][0].upper()
        mobile_number = data['mobileNumber']

        if mobile_number[0] != "0":
            mobile_number = "0" + mobile_number

        self.cursor.execute(
            """
            UPDATE Subscribers_mtbl 
            SET 
                CUST_FNAME = %s, 
                CUST_LNAME = %s, 
                CUST_BIRTHDATE = %s, 
                CUST_ALERGY = %s, 
                CUST_GENDER = %s, 
                CUST_MOBILENO = %s 
            WHERE CUST_CODE = %s
            """,
            (fname, lname, birth_date, allergy, gender, mobile_number, user_id)
        )
        self.conn.commit()
        return {"status": "User profile updated"}
