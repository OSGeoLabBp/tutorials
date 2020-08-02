#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
""" első Python programom
	1 - argv[1] közötti egész számok összege
"""
from sys import argv
if len(argv) < 2:
	print("usage: {} number".format(argv[0]))
	exit(1)
print(sum(range(1, int(argv[1])+1)))
