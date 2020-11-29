# We import the requests module which allows us to make the API call
import pandas as pd
import json
import requests
 
# Call API to pull data
# url = 'https://health.data.ny.gov/resource/xdss-u53e.json' #covid data
# url = 'https://health.data.ny.gov/resource/cnih-y5dw.json' #restaurant data
# url = 'https://data.ny.gov/resource/7gkb-pzs9.json' #trails data
url = 'https://data.ny.gov/resource/mj5h-8ei4.json' #rest areas
response = requests.get(url = url)
response_data = response.json()

#connect to DB
# connection_string = "host='%s' dbname='final_project' user='postgres' password='postgres'" % (host,)
# conn = psycopg2.connect(connection_string, cursor_factory=psycopg2.extras.DictCursor)

#insert into DB
for record in response_data:
    print(json.dumps(record))
#     cursor.execute("Insert Into Ticket_Info values ?", json.dumps(record))
#     cursor.commit()
    
# conn.close()
# connection_string.close()