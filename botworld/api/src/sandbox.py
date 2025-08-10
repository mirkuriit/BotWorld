import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="game_db",
        user="mirkuriit",
        password="meow")

cur = conn.cursor()
cur.execute("SELECT 1")
print(cur.execute("SELECT 1"))