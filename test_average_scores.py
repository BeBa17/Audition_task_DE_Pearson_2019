#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 21:32:47 2019

@author: beata
"""

import sqlite3
import sys

my_names=[]
database_name = sys.argv[1]
conn = sqlite3.connect(database_name) 
c = conn.cursor()
            
def create_test_average_scores_database():
    c.execute(""" CREATE TABLE test_average_scores_file (
        class_id integer,
        class_name text,
        teaching_hours blob,
        test_created_at numeric,
        test_authorized_at numeric not null,
        avg_class_test_overall_score real
        )""")
    conn.commit()
    c.execute(""" SELECT b.id as class_id,
              b.name as class_name,
              b.sum_hours as teaching_hours,
              b.created_at as test_created_at,
              b.authorized_at as test_authorized_at,
              a.avg_sum as avg_class_test_overall_score
              FROM
              (
              SELECT avg(sum_score) as avg_sum, id FROM 
               (SELECT (t.speaking_score + t.writing_score + t.reading_score + t.listening_score)
               as sum_score,
               c.id as id
               FROM class_file c join test_file t
               on c.id = t.class_id
               where t.authorized_at!='' and t.test_status='SCORING_SCORED') d
      group by d.id
              ) a
               join 
               (
               SELECT c.id as id, c.name as name,
              sum(teaching_hours) as sum_hours,
              c.created_at as created_at,
              max(t.authorized_at) as authorized_at
              from class_file c join test_file t on c.id = t.class_id
              group by c.id
               ) b
               on a.id = b.id """)
    query = c.fetchall()
    for line in query:
        c.execute(""" INSERT INTO test_average_scores_file
                      VALUES (?,?,?,?,?,?)""", line)
    conn.commit()
    

def main():
    
    create_test_average_scores_database()
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    main()