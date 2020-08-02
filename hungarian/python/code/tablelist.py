#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import psycopg2 as db	# PostgreSQL meghajtó betöltése
from sys import argv

if len(argv) < 4:
	print("Használat: {} database user password table".format(argv[0]))
	exit(1)
con = None				# kapcsolat változó inicializálása
try:
    con = db.connect(database=argv[1], user=argv[2], password=argv[3])
    cur = con.cursor()						# cursor a lekérdezéshez
    cur.execute('SELECT * FROM varos')		# adatok lekérdezése
    rec = cur.fetchone()					# következő sor a lekérdezésből
    while rec:
        print(rec)
        rec = cur.fetchone()
except db.DatabaseError as e:
    print('Hiba: {}'.format(e))				# hibaüzenet kiírása
    exit(1)
finally:
    if con:									# kapcsolat lezárása
        con.close()
