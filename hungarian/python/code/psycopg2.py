#!/usr/bin/env python
import psycopg2
conn = psycopg2.connect("postgresql:///siki")
#conn = psycopg2.connect("dbname=siki user=siki")
cur = conn.cursor()
#cur.execute("INSERT INTO pdata (id, easting, northing, elev, d)) VALUES (%s, %f, %f, %f, %s)", ('100', 1111.111, 2222.222, 333.333, '2017.02.16 11:22'))
cur.execute("SELECT * FROM pdata")
for row in cur:
    print row
cur.close()
conn.close()
