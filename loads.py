#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 21:24:17 2019

@author: beata
"""

import csv
import sqlite3
import re

my_names=[]
conn = sqlite3.connect('test2.db') 
c = conn.cursor()

def create_table_class_file():
    c.execute(""" CREATE TABLE class_file ( 
        id integer primary key not null,
        institution_id integer not null,
        owner_id integer not null,
        name text,
        created_at numeric,
        updated_at numeric,
        teaching_hours blob,
        latest_test_time numeric,
        has_student_with_scored_test numeric
        )""")
    conn.commit()

    
def create_table_test_file():
    c.execute(""" CREATE TABLE test_file (
        id integer not null,
        student_id integer not null,
        class_id integer not null,
        created_at numeric,
        updated_at numeric,
        last_event_time blob,
        overall_score real,
        test_status blob,
        institution_id integer not null,
        authorized_at numeric,
        confidence_level real,
        speaking_score real,
        writing_score real,
        reading_score real,
        listening_score real,
        test_level_id integer,
        licence_id integer
        )""")
    conn.commit()

    
def create_table_test_level_file():
    c.execute(""" CREATE TABLE test_level_file ( 
        id integer not null,
        name text,
        displayName text,
        created_at numeric,
        updated_at numeric
        )""")
    conn.commit()

    
def unconnect_to_database(conn):
    conn.commit()
    conn.close()
    
def send_correct_data_to_class_database():
    with open('class.csv', 'r') as csv_file:
        file_contest = csv.reader(csv_file, delimiter=';')
    
        pattern1 = re.compile(r'\d-[a-zA-Z]\b$')
        pattern2 = re.compile(r'\W\d[a-zA-Z]\b$')
    
        for line in file_contest:
            matches1 = pattern1.finditer(line[3])
            for match in matches1:
                c.execute("INSERT INTO class_file VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", line)
            matches2 = pattern2.finditer(line[3])
            for match in matches2:
                c.execute("INSERT INTO class_file VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", line)
    conn.commit()
                
def send_correct_data_to_test_database():
    with open('test.csv', 'r') as csv_file:
        file_contest = csv.reader(csv_file, delimiter=';')

        for line in file_contest:
            c.execute("INSERT INTO test_file VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", line)
    conn.commit()

def send_correct_data_to_test_level_database():
    with open('test_level.csv', 'r') as csv_file:
        file_contest = csv.reader(csv_file, delimiter=';')
    
        for line in file_contest:
            c.execute("INSERT INTO test_level_file VALUES (?, ?, ?, ?, ?)", line)
    conn.commit()

def main():
    
    create_table_class_file()
    create_table_test_file()
    create_table_test_level_file()
    send_correct_data_to_class_database()
    send_correct_data_to_test_database()
    send_correct_data_to_test_level_database()
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    main()