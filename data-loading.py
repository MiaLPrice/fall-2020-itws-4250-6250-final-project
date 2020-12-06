#We import the requests module which allows us to make the API call
import pandas as pd
import json
import requests
import psycopg2
from sodapy import Socrata
import sys
import re

try:
    conn = psycopg2.connect("dbname = 'finalproject' user = 'postgres' password='postgres' host = 'localhost'")
except psycopg2.DatabaseError:
    print('I am unable to connect the database')
    sys.exit(1)

with conn.cursor() as cursor:
    setup_queries = open('project-schema.sql', 'r').read()
    cursor.execute(setup_queries)
    conn.commit()

# Parking/Rest Areas
# Column Names: title,milepost,route_location,direction,route,icon_anchor,tp_id,latitude,longitude,location 

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
# Column Names: the_geom, unit,facility,fac_unq,name,alt_name,asset,asset_unq,colldate,blaze,blaze_2,surface,condition,corridor_w,tread_widt,height,atv,foot,horse,bike,xc,motorv,snowmb,admin,accessible,source,shape_leng,abbrev

results = client.get("7gkb-pzs9", limit=9599)
results_df = pd.DataFrame.from_records(results)
lenResults = len(results_df)

with conn.cursor() as cursor:
    for i in range(0, lenResults): 
        #query = """INSERT INTO trails VALUES (%s, %s, ST_SetSRID(ST_POINT(%s, %s),4326), %s)""" 
        
        query = """INSERT INTO trails VALUES (%s, %s, %s, %s, %s)"""
        
        latitude = results_df['the_geom'][i]['coordinates'][0][0][0]
        longitude = results_df['the_geom'][i]['coordinates'][0][0][1]
        
        # poly = [(points[0], points[1]) for points in results_df['the_geom'][i]['coordinates'][0]]
        # print(poly)
        
        record = (i, results_df['name'][i], latitude, longitude, results_df['shape_leng'][i])
        cursor.execute(query, record)
        conn.commit()    

# Covid 
# Column Names: test_date  county new_positives cumulative_number_of_positives total_number_of_tests cumulative_number_of_tests

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

# Restuarants 
# Column Names: facility, address, date, violations, total_critical_violations, total_crit_not_corrected, total_noncritical_violations, 
# description, local_health_department, county, facility_address, city, zip_code, nysdoh_gazetteer_1980, municipality, 
# operation_name, permit_expiration_date, permitted_corp_name, perm_operator_last_name, perm_operator_first_name, 
# nys_health_operation_id,  inspection_type, inspection_comments, food_service_facility_state, location1, 

results = client.get("cnih-y5dw", limit=30000)

results_df = pd.DataFrame.from_records(results)
results_df['total_critical_violations'].fillna(0, inplace=True)
results_df['total_crit_not_corrected'].fillna(0, inplace=True)

pivot = pd.DataFrame(results_df.location1.values.tolist())
results_df = pd.concat([results_df, pivot], axis=1, sort=False)
results_df = results_df.drop_duplicates(subset = ["latitude", "longitude", "facility"]).reset_index(drop=True)

lenResults = len(results_df)

with conn.cursor() as cursor:
    for i in range(0, lenResults): 
        query = """INSERT INTO restuarants VALUES (%s, %s, %s, %s, %s, %s)"""        
        # latitude = df['location1'][i]['latitude']
        # longitude = df['location1'][i]['longitude']
        record = (i, results_df['facility'][i], results_df['address'][i], results_df['zip_code'][i], results_df['latitude'][i], results_df['longitude'][i])
        cursor.execute(query, record)
        conn.commit()

df = results_df[['city','zip_code','county']].drop_duplicates(subset = ['zip_code'])
with conn.cursor() as cursor:
    query = """INSERT INTO cities VALUES (%s, %s, %s)"""
    for i, row in df.iterrows():   
        record = (row['city'], row['zip_code'], row['county'])
        cursor.execute(query, record)
        conn.commit()

with conn.cursor() as cursor:
    for i in range(0, lenResults): 
        query = """INSERT INTO inspections VALUES (%s, %s, %s, %s)"""
        record = (i, results_df['date'][i], results_df['total_critical_violations'][i], results_df['total_crit_not_corrected'][i])
        cursor.execute(query, record)
        conn.commit()