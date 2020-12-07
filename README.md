# fall-2020-itws-4250-6250-final-project

## Database Setup ##
Run database-setup.sql file in your command prompt using

`psql master_dbname master_dbuser < db-setup.sql`

This should setup your database **dbms_final_project** with user **dbms_project_user**

## Loading Data ##
Run data-loading.py in you command prompt using

`python data-loading.py`

This should load the data into your database as per the **schema.sql** file

## Launch Application ##
Run data-querying in your command prompt using

`streamlit run data-querying.py`

This should launch the application in your local browser

## Data Reset ##
There are two ways of doing this

-Use the **Reset Data** button in application

-Run `python retreive-data.py` in your command prompt
