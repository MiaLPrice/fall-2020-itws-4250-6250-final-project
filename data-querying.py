import pandas as pd
import requests
import psycopg2
import sys
import re
import streamlit as st

try:
    conn = psycopg2.connect("dbname = 'finalproject' user = 'postgres' password='postgres' host = 'localhost'")
except psycopg2.DatabaseError:
    print('I am unable to connect the database')
    sys.exit(1)

st.markdown("# **Welcome to Database Application**")
st.sidebar.markdown("**Select Options**")
    
#Restaurants
if st.sidebar.checkbox('Show Restaurants on map'):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT latitude, longitude FROM restuarants WHERE longitude < -70""")
        records = cursor.fetchall()
    records = pd.DataFrame(records, columns = ["latitude","longitude"])
    st.map(records)
    
    
#RestAreas
if st.sidebar.checkbox('Show Parking/Rest Areas on map'):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT latitude, longitude FROM restareas""")
        records = cursor.fetchall()
    records = pd.DataFrame(records, columns = ["latitude","longitude"])
    st.map(records)

#Trails
if st.sidebar.checkbox('Show Trails on map'):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT latitude, longitude FROM trails""")
        records = cursor.fetchall()
    records = pd.DataFrame(records, columns = ["longitude", "latitude"])
    st.map(records)

#Covid

#Queries to do
#Restaurants with most violations
#Restaurants with least violations
#RestAreas in low covid counties
#Trails in low covid counties
#Top 10 highest covid counties in NY
#Top 10 lowest covid counties in NY