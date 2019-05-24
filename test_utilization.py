#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 21:28:15 2019

@author: beata
"""
import sqlite3

my_names=[]
conn = sqlite3.connect('test2.db') 
c = conn.cursor()

def create_test_utilization_database():
    c.execute(""" CREATE TABLE test_utilization_file (
        class_id integer,
        class_name text,
        teaching_hours blob,
        test_id integer,
        test_level integer,
        test_created_at numeric,
        test_authorized_at numeric not null,
        class_test_number integer
        )""")
    conn.commit()
    c.execute("""SELECT DISTINCT c.id as class_id
                    FROM class_file c join test_file t
                      on c.id = t.class_id
                      where t.authorized_at!=''
                      """)
    ids = c.fetchall()
    for each_id in ids:
        num = 1
        c.execute("""SELECT c.id as class_id,
                          c.name as class_name,
                          c.teaching_hours as teaching_hours,
                          t.id as test_id,
                          t.test_level_id as test_level,
                          t.created_at as test_created_at,
                          t.authorized_at as test_authorized
                          FROM class_file c join test_file t
                          on c.id = t.class_id
                          where t.authorized_at!=''
                          and c.id = ?
                          order by test_id""", each_id)
        query = c.fetchall()
        elements = []
        for line in query:
            elements = line + (num,)
            c.execute(""" INSERT INTO test_utilization_file
                      VALUES (?,?,?,?,?,?,?,?)""", tuple(elements))
            conn.commit()
            num += 1

def main():
    
    create_test_utilization_database()
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    main()
