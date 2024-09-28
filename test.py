import pyodbc
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};SERVER=COSMIC-PC;DATABASE=BigData;Trusted_Connection=yes;TrustServerCertificate=yes')

cursor = conn.cursor()
cursor.execute("select * from Subscribers_mtbl")
print(cursor.fetchone())
