#!/usr/bin/env python
print "Content-type: text/plain\n\n"
import psycopg2
conn = psycopg2.connect("host=localhost dbname=siki user=siki password=qwerty")
cur = conn.cursor()
cur.execute("SELECT * FROM pdata")
for row in cur:
    print row
cur.close()
conn.close()
