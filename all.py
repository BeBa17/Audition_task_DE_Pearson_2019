#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 22:18:02 2019

@author: beata
"""

import os
import sys

db = sys.argv[1]

os.system("python3 loads.py "+db)
os.system("python3 test_utilization.py "+db)
os.system("python3 test_average_scores.py "+db)

os.system("python3 to_csv.py "+db+" test_utilization_file")
os.system("python3 to_csv.py "+db+" test_average_scores_file")

print("Done !")