#!/usr/bin/env python3
# -*- coding: UTF-8 -*- 
""" adott szöveget tartalmazó sorok kiírása egy fájlból """
from os import path						# file létezik-hez
from sys import argv					# paraméterekhez

if len(argv) < 3:
	print("Usage: {} <fájl> <keresett_szöveg>".format(argv[0]))
	exit(1)
if not path.exists(argv[1]):
	print("{} fájlt nem találom".argv[1])
	exit(2)

with open(argv[1]) as f:
	for line in f:						# soronként olvasás
		if line.find(argv[2]) >= 0:
			print(line.strip('\n\r'))
