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
rec = records[0]
print('id: ',rec[0], '\n')
print('value: ',rec[1],'\n')
print('timestamp: ',rec[2],'\n')
print('mac add: ',rec[3])

# rec_dic = {}
# rec_dic['results'] = records

# output_file='uss_record_2.csv'
# with open(output_file, 'w') as f1:
#     f1.write(str(rec_dic))

# cur.execute('SELECT * FROM pir_record')
# records = cur.fetchall()

# output_file='pir_record.txt'
# with open(output_file, 'w') as f1:
#     f1.write(str(rec_dic))