import psycopg2

DB_NAME = ""
DB_USER = ""
DB_PASS = ""
DB_HOST = ""
DB_PORT = ""

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
postgreSQL_select_Query = """ SELECT * FROM EXCHANGE WHERE CHATID = %s"""
postgre_insert_query = """ INSERT INTO exchange (INVALUTE, OUTVALUTE, INVALUE, OUTVALUE, USERNAME, CHATID,
    CURDATE) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
