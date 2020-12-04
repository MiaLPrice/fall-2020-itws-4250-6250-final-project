# We import the requests module which allows us to make the API call
import pandas as pd
import json
import requests
import psycopg2
from sodapy import Socrata
import sys
import re

'''
    table                 done
    restuarants            
    covid                 
    restuarants            
    restareas                            
    counties              
    trails
'''

try:
    conn = psycopg2.connect("dbname = 'finalproject' user = 'postgres' password='password' host = 'localhost'")
except psycopg2.DatabaseError:
    print('I am unable to connect the database')
    sys.exit(1)

with conn.cursor() as cursor:
    setup_queries = open('project-schema.sql', 'r').read()
    cursor.execute(setup_queries)
    conn.commit()

# Parking/Rest Areas

'''
Column Names: title,milepost,route_location,direction,route,icon_anchor,tp_id,latitude,longitude,location
''' 

client = Socrata("data.ny.gov", None)
results = client.get("mj5h-8ei4")
results_df = pd.DataFrame.from_records(results)
lenResults = len(results_df)

with conn.cursor() as cursor:
    for i in range(0, lenResults): 
        query = """INSERT INTO restareas VALUES (%s, %s, %s, %s)"""   
        record = (results_df['tp_id'][i], results_df['title'][i], results_df['latitude'][i],results_df['longitude'][i])
        cursor.execute(query, record)
        conn.commit()

# Trails 
'''
column names: the_geom, unit,facility,fac_unq,name,alt_name,asset,asset_unq,colldate,blaze,blaze_2,surface,condition,corridor_w,tread_widt,height,atv,foot,horse,bike,xc,motorv,snowmb,admin,accessible,source,shape_leng,abbrev

results = client.get("7gkb-pzs9", limit=9599)
results_df = pd.DataFrame.from_records(results)
lenResults = len(results_df)
print(results_df)
with conn.cursor() as cursor:
    for i in range(0, lenResults): 
        query = """INSERT INTO trails VALUES (%s, %s, %s, %s)"""   
        record = (i, results_df['name'][i], results_df['shape_length'][i], results_df['the_geom'][i])
        print(record)
        cursor.execute(query, record)
        conn.commit()    

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)
'''


# Covid 
'''colnames: test_date  county new_positives cumulative_number_of_positives total_number_of_tests cumulative_number_of_tests'''

client = Socrata("health.data.ny.gov", None)
results = client.get("xdss-u53e", limit=50000)

results_df = pd.DataFrame.from_records(results)
lenResults = len(results_df)

with conn.cursor() as cursor:
    for i in range(0, lenResults): 
        query = """INSERT INTO covid VALUES (%s, %s, %s, %s)"""   
        record = (results_df['test_date'][i], results_df['county'][i], results_df['total_number_of_tests'][i], results_df['new_positives'][i])
        cursor.execute(query, record)
        conn.commit() 

# restuarants 
results = client.get("cnih-y5dw", limit=2000)

results_df = pd.DataFrame.from_records(results)
lenResults = len(results_df)
print(results_df)


