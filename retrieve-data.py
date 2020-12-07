import psycopg2
import sys
import os

try:
    conn = psycopg2.connect("dbname = 'dbms_final_project' user = 'dbms_project_user' password='dbms_password' host = 'localhost'")
except psycopg2.DatabaseError:
    print('I am unable to connect the database')
    sys.exit(1)

with conn.cursor() as cursor:
    setup_queries = open('schema.sql', 'r').read()
    cursor.execute(setup_queries)
    conn.commit()
    
os.system('data-loading.py')