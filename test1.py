#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 23 12:51:17 2019

@author: beata
"""
import csv
import sqlite3
import re

my_names=[]
conn = sqlite3.connect('test1.db') 
c = conn.cursor()

def connect_to_database():
    return sqlite3.connect('test1.db'), sqlite3.connect('test1.db').cursor()
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
        #print(each_id)
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
            #print(elements)
            c.execute(""" INSERT INTO test_utilization_file
                      VALUES (?,?,?,?,?,?,?,?)""", tuple(elements))
            conn.commit()
            num += 1
            #print(line)
            
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
    #conn, c = connect_to_database()
    
    #create_table_class_file()
    #create_table_test_file()
    #create_table_test_level_file()
    #send_correct_data_to_class_database()
    #send_correct_data_to_test_database()
    #send_correct_data_to_test_level_database()
    #create_test_utilization_database()
    #c.execute("drop table test_average_scores_file")
    #create_test_average_scores_database()
    conn.commit()
    conn.close()
    #unconnect_to_database(conn)
    
if __name__ == '__main__':
    main()
    
    


        #for coll in file_contest.fieldnames:



#c.execute("INSERT INTO class_file VALUES (10, 22, 32, 'naaame', 54, 32, 4-6, 43,1)")

#print(c.execute("select * from class_file"))
#c.execute("delete from class_file where id=10")
#c.execute("drop table class_file")



