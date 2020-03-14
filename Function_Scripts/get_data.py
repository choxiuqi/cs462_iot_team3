import psycopg2
from datetime import datetime
from pytz import timezone
import pytz
import requests

conn = psycopg2.connect(host="127.0.0.1", dbname="cs462team3db", user="team3user", password="password")
# Cursor is created by the Connection object and using the Cursor object we will be able to execute our commands.
cur = conn.cursor()
conn.autocommit = True

cur.execute('SELECT * FROM uss_record')
records = cur.fetchall()

output_file='uss_record.csv'
with open(output_file, 'w') as f1:
    for i in records:
        i2 = str(i) + "\n"
        f1.write(i2)