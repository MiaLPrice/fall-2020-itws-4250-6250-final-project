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

# Convert to pandas DataFrame
results_df = pd.DataFrame.from_records(results)

# Covid 
client = Socrata("health.data.ny.gov", None)
results = client.get("xdss-u53e", limit=2000)

results_df = pd.DataFrame.from_records(results)

# restuarants 
resultcs = client.get("cnih-y5dw", limit=2000)

results_df = pd.DataFrame.from_records(results)

'''