# Audition_task_DE_Pearson_2019

I loaded all csv files which I had received (class.csv, test.csv, test_level.csv).

The first one script - loads.py realises the first two tasks. It load appropriate rows to tables in database.
To use this script you should type: ./loads.py database_name.db

The second one - test_utilization.py realises task 3. 
To use this script you should type: ./test_utilization.py database_name.db

The third one - test_average_scores.py realises task 4. 
To use this script you should type: ./test_average_scores.py database_name.db

The last one - to_csv.py comes back to csv format.
To use this script you should type: ./to_csv.py database_name.db table_name
As a result you have table_name table converted to the csv file format.

File all.py realises all scripts in order. As a result you get database .db with tables: test_file, test_level_file and class_file and new tables: test_utilization_file and test_average_scores_file. You get also the new ones databases in csv-file form.
To use this script you should type: ./all.py database_name.db 
