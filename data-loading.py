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
client = Socrata("data.ny.gov", None)
results = client.get("mj5h-8ei4", limit=2000)
results_df = pd.DataFrame.from_records(results)
print(results_df)

'''
# Trails 
results = client.get("7gkb-pzs9", limit=2000)
results_df = pd.DataFrame.from_records(results)

# Covid 
client = Socrata("health.data.ny.gov", None)
results = client.get("xdss-u53e", limit=2000)
results_df = pd.DataFrame.from_records(results)

# restaurants 
results = client.get("cnih-y5dw", limit=2000)
results_df = pd.DataFrame.from_records(results)
'''

#Inserting data into restareas
for index, row in results_df.iterrows():
    cursor.execute("INSERT INTO project-schema.restareas values(%s,%s,%s,%s,geography::STPointFromText('LINESTRING(%s %s)', 4326))", 
                   (row.tp_id, row.route_location, row.latitude, row.longitude, row.location[0], row.location[1]))                          # Not working stPointFromText doesn't exist. This column is a geography data type. Not sure how to handle this

#Inserting data into trails
#Inserting data into covid
#Inserting data into restaurants
    
conn.close()
connection_string.close()
