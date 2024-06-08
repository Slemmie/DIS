import psycopg2
from config import db, port
import os

os.chdir('data')
with open('parse.py') as file:
	exec(file.read())
os.chdir('..')

conn = psycopg2.connect(db)

cur = conn.cursor()

with open('data/problems.sql', 'r') as file:
    sql_commands = file.read()
cur.execute(sql_commands)
conn.commit()

cur.close()

conn.close()
