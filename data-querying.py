import pandas as pd
import requests
import psycopg2
import sys
import re
import streamlit as st
import pydeck as pdk
import xml.etree.ElementTree as ET

try:
    conn = psycopg2.connect("dbname = 'finalproject' user = 'postgres' password='postgres' host = 'localhost'")
except psycopg2.DatabaseError:
    print('I am unable to connect the database')
    sys.exit(1)

st.markdown("# **Welcome to Database Application**")
    
#Restaurants
with conn.cursor() as cursor:
    cursor.execute("""SELECT latitude, longitude FROM restuarants WHERE longitude < -70""")
    res_records = cursor.fetchall()
res_records = pd.DataFrame(res_records, columns = ["latitude","longitude"])
    
#RestAreas
tree = ET.parse('C:\\Users\\admin\\Desktop\\fall-2020-itws-4250-6250-final-project-main\\restareas.xml')
root = tree.getroot()
rows = []

for elem in root:
    latitude = float(elem.find('latitude').text)
    longitude = float(elem.find('longitude').text)
    rows.append({"latitude": latitude, "longitude": longitude})
    
area_records = pd.DataFrame(rows, columns = ["latitude", "longitude"])

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
#Top 10 highest covid counties in NY
#Top 10 lowest covid counties in NY

st.sidebar.markdown("## **Search Restaurants**")
if st.sidebar.checkbox("Would you like to search a restaurant?"):
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
        cursor.execute("""SELECT restuarants.longitude, restuarants.latitude, restuarants.restuarantName, restuarants.restuarantAddress, inspections.critViolations, inspections.nonCritViolations 
        FROM restuarants LEFT JOIN inspections ON restuarants.restuarantID = inspections.restuarantID 
        WHERE zipcode IN (SELECT zipcode FROM cities WHERE county = %s AND city = %s) ORDER BY restuarants.restuarantName""", (county,city,))
        records = cursor.fetchall()
    records = pd.DataFrame(records, columns = ["longitude", "latitude", "restuarantName", "restuarantAddress", "critViolations" ,"nonCritViolations"])
    
    restaurants = st.sidebar.selectbox("Select a restaurant", (records["restuarantName"]))
    map_plot = records[records.restuarantName == restaurants]
    st.dataframe(map_plot[["restuarantName", "restuarantAddress", "critViolations" ,"nonCritViolations"]].assign(hack='').set_index('hack'))
    st.map(map_plot, zoom = 12)
    
    if st.button("Show COVID data for County"):
        with conn.cursor() as cursor:
            cursor.execute("""SELECT updateDate, testsPerformeted, newPostives FROM covid WHERE county = %s ORDER BY updateDate DESC""", (county.title(),))
            records = cursor.fetchall()
        records = pd.DataFrame(records, columns = ["updateDate", "testsPerformeted", "newPostives"])
        st.line_chart(records.rename(columns={'updateDate':'index'}).set_index('index'))

    #Show inspections vs covid
    if st.sidebar.checkbox("Show comparison between Critical Violations and New COVID Cases for each city in county"):
        with conn.cursor() as cursor:
            cursor.execute("""SELECT covid.county, cities.city, MAX(covid.updatedate) as updatedate, SUM(inspections.critviolations) as CriticalViolations, SUM(covid.newpostives) AS NewPositives 
            FROM inspections
            LEFT JOIN restuarants
            ON restuarants.restuarantid = inspections.restuarantid
            LEFT JOIN cities
            ON cities.zipcode = restuarants.zipcode
            LEFT JOIN covid
            ON LOWER(covid.county) = LOWER(cities.county)
            GROUP BY covid.county, cities.city
            ORDER BY covid.county ASC""")
            records = cursor.fetchall()
        records = pd.DataFrame(records, columns = ["county", "city", "updateDate", "CriticalViolations", "NewPositives"])
        records = records[records.county == county.title()]
        st.dataframe(records)
        st.line_chart(records[["city", "NewPositives"]].rename(columns={'city':'index'}).set_index('index'))
        st.line_chart(records[["city", "CriticalViolations"]].rename(columns={'city':'index'}).set_index('index'))
        
        
st.sidebar.markdown("## **Add Restaurant**")
if st.sidebar.checkbox("Would you like to add a restaurant?"):
    with conn.cursor() as cursor:
        cursor.execute("""SELECT DISTINCT county FROM cities ORDER BY county ASC""")
        records = cursor.fetchall()
    records = pd.DataFrame(records)
    county = st.sidebar.selectbox("Select the county of your restaurant", (records))

    with conn.cursor() as cursor:
        cursor.execute("""SELECT DISTINCT city FROM cities WHERE county = %s ORDER BY city ASC """, (county,))
        records = cursor.fetchall()
    records = pd.DataFrame(records)
    city = st.sidebar.selectbox("Select the city of your restaurant", (records))

    name = st.text_input("Enter the name of the Restaurant")
    address = st.text_area("Enter the address of the Restaurant")
    zip = st.text_input("Enter zipcode of the Restaurant")
    spaces = " "*(9-len(zip))
    zip = zip+spaces
    latitude = st.number_input("Enter latitude of the Restaurant")
    longitude = st.number_input("Enter longitude of the Restaurant")
    
    if st.button("Add"):
        with conn.cursor() as cursor:
            query = """SELECT restuarantid FROM restuarants ORDER BY restuarantid DESC LIMIT 1"""
            cursor.execute(query)
            id = cursor.fetchall()
            id = pd.DataFrame(id, columns = ["id"])
            id = int(id["id"][0] + 1)
            query = """INSERT INTO restuarants VALUES (%s, %s, %s, %s, %s, %s)"""        
            record = (id, name, address, zip, latitude, longitude)
            cursor.execute(query, record)
            conn.commit()
            st.success("Your Restaurant was inserted into the database successfully!")


