import pandas as pd
import requests
import psycopg2
import sys
import re
import streamlit as st
import pydeck as pdk

try:
    conn = psycopg2.connect("dbname = 'finalproject' user = 'postgres' password='postgres' host = 'localhost'")
except psycopg2.DatabaseError:
    print('I am unable to connect the database')
    sys.exit(1)

st.markdown("# **Welcome to Database Application**")
st.sidebar.markdown("## **Select Options**")
    
#Restaurants
with conn.cursor() as cursor:
    cursor.execute("""SELECT latitude, longitude FROM restuarants WHERE longitude < -70""")
    res_records = cursor.fetchall()
res_records = pd.DataFrame(res_records, columns = ["latitude","longitude"])
    
#RestAreas
with conn.cursor() as cursor:
    cursor.execute("""SELECT latitude, longitude FROM restareas""")
    area_records = cursor.fetchall()
area_records = pd.DataFrame(area_records, columns = ["latitude","longitude"])

#Trails  
with conn.cursor() as cursor:
    cursor.execute("""SELECT latitude, longitude FROM trails""")
    trail_records = cursor.fetchall()
trail_records = pd.DataFrame(trail_records, columns = ["longitude", "latitude"])

#Covid
with conn.cursor() as cursor:
    cursor.execute("""SELECT * FROM covid""")
    covid_records = cursor.fetchall()
covid_records = pd.DataFrame(covid_records, columns = ["updateDate", "county", "testsPerformeted", "newPostives"])

#Map Initialisation
viewport = pdk.ViewState(latitude=42.730610, longitude=-75.935242, zoom=5.5)
restareas = pdk.Layer('ScatterplotLayer', data = area_records, get_position = '[longitude, latitude]', get_color='[0, 255, 0, 600]', get_radius=4000)
trails = pdk.Layer('ScatterplotLayer', data = trail_records, get_position = '[longitude, latitude]', get_color='[0, 0, 255, 600]', get_radius=1000)
restuarants = pdk.Layer('ScatterplotLayer', data = res_records, get_position = '[longitude, latitude]', get_color='[255, 0, 0, 600]', get_radius=1000)

layers = []

if st.sidebar.checkbox("Show map of NY state"):
    st.sidebar.markdown("Please select the options you want to see on the map")
    if st.sidebar.checkbox("Show Restareas"):
        layers.append(restareas)
    if st.sidebar.checkbox("Show Trails"):
        layers.append(trails)
    if st.sidebar.checkbox("Show Restaurants"):
        layers.append(restuarants)

    st.pydeck_chart(pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state = viewport, layers = layers))


#Queries to do
#Restaurants with most violations
#Restaurants with least violations
#RestAreas in low covid counties
#Trails in low covid counties
#Top 10 highest covid counties in NY
#Top 10 lowest covid counties in NY

if st.sidebar.checkbox("Search by county"):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT DISTINCT county FROM cities ORDER BY county ASC""")
        records = cursor.fetchall()
    records = pd.DataFrame(records)
    county = st.sidebar.selectbox("Please select a county", (records))
    
    with conn.cursor() as cursor:
        cursor.execute("""SELECT DISTINCT city FROM cities WHERE county = %s ORDER BY city ASC """, (county,))
        records = cursor.fetchall()
    records = pd.DataFrame(records)
    city = st.sidebar.selectbox("Please select a city", (records))
    
    with conn.cursor() as cursor:
        cursor.execute("""SELECT restuarants.longitude, restuarants.latitude, restuarants.restuarantName, restuarants.restuarantAddress, inspections.critViolations, inspections.nonCritViolations FROM restuarants INNER JOIN inspections ON restuarants.restuarantID = inspections.restuarantID WHERE zipcode IN (SELECT zipcode FROM cities WHERE county = %s AND city = %s)""", (county,city,))
        records = cursor.fetchall()
    records = pd.DataFrame(records, columns = ["longitude", "latitude", "restuarantName", "restuarantAddress", "critViolations" ,"nonCritViolations"])
    
    restaurants = st.selectbox("Select a Restaurant", (records["restuarantName"]))
    map_plot = records[records.restuarantName == restaurants]
    st.dataframe(map_plot[["restuarantName", "restuarantAddress", "critViolations" ,"nonCritViolations"]])
    st.map(map_plot, zoom = 12)
    
    if st.button("Show COVID data for County"):
        with conn.cursor() as cursor:
            cursor.execute("""SELECT updateDate, testsPerformeted, newPostives FROM covid WHERE county = %s ORDER BY updateDate DESC""", (county.title(),))
            records = cursor.fetchall()
        records = pd.DataFrame(records, columns = ["updateDate", "testsPerformeted", "newPostives"])
        st.line_chart(records.rename(columns={'updateDate':'index'}).set_index('index'))
    