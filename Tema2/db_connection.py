import mysql.connector

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='1234',
        database='ganaderia_db'
    )
    return conn