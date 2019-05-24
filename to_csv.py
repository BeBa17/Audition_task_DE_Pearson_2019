#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 22:29:38 2019

@author: beata
"""

import csv
import sqlite3
import sys

database_name = sys.argv[1]
table_name = sys.argv[2]
conn = sqlite3.connect(database_name) 
c = conn.cursor()

t = [str(table_name)]
c.execute("SELECT * FROM %s " %tuple(t))
res = c.fetchall()

with open(table_name+".csv", 'w') as csv_file:
        file_contest = csv.writer(csv_file, delimiter=';')

        for line in res:
            file_contest.writerow(line)