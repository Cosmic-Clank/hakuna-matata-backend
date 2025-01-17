import pymssql
import os
import json
import util


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

    def get_user_by_code(self, code: int):
        self.cursor.execute(
            "SELECT * FROM Subscribers_mtbl WHERE CUST_CODE = %s", (code,)
        )
        row = self.cursor.fetchone()
        return row if row else None

    def get_user_by_email(self, email: str):
        self.cursor.execute(
            "SELECT * FROM Subscribers_mtbl WHERE CUST_EMAIL = %s", (email,)
        )
        row = self.cursor.fetchone()
        return row

    def register_user(self, data: dict):  # fname, lname, email, password
        fname = data['fname']
        lname = data['lname']
        email = data['email']
        password = data['password']

        if not fname or not lname or not email or not password:
            return False

        hashed_password = util.hash_password(password)

        self.cursor.execute(
            """
            INSERT INTO Subscribers_mtbl (CUST_FNAME, CUST_LNAME, CUST_EMAIL, CUST_PASSWORD, CUST_QRCODE, CUST_NATIONALITY, CUST_InternationalCode, CUST_MobileNo, CUST_GENDER, CUST_BIRTHDATE, CUST_ALERGY)
            VALUES (%s, %s, %s, %s, 'QR_CODE_PLACEHOLDER', NULL, NULL, NULL, NULL, NULL, NULL)
            """,
            (fname, lname, email, hashed_password)
        )

        self.conn.commit()

        return True

    def get_sales_counter(self, user_id: str):
        self.cursor.execute(
            "SELECT CUST_COUNTER FROM Subscribers_mtbl WHERE CUST_CODE = %s", (
                user_id,)
        )
        row = self.cursor.fetchone()
        return row["CUST_COUNTER"] if row else None

    def update_profile_data(self, user_id, attribute, newValue):
        self.cursor.execute(
            f"""
            UPDATE Subscribers_mtbl 
            SET 
                {attribute} = %s
            WHERE CUST_CODE = %s
            """,
            (newValue, user_id)
        )
        self.conn.commit()
        return True

    def delete_user(self, user_id):
        self.cursor.execute(
            "UPDATE Subscribers_mtbl "
            "SET CUST_DELETED = 1, CUST_DELETIONDATE = GETDATE() "
            "WHERE CUST_CODE = %s",
            (user_id,)
        )
        self.conn.commit()
        return True
