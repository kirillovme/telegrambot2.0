import psycopg2

DB_NAME = "bot_database"
DB_USER = "postgres"
DB_PASS = "569274"
DB_HOST = "192.168.2.129"
DB_PORT = "5432"

conn = psycopg2.connect(database=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)
postgreSQL_select_Query = """ SELECT * FROM EXCHANGE WHERE CHATID = %s"""
postgre_insert_query = """ INSERT INTO exchange (INVALUTE, OUTVALUTE, INVALUE, OUTVALUE, USERNAME, CHATID,
    CURDATE) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
