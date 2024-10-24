"""
   Purpose of this program is to load the CSV datasets to SQLite3 DataBase.
   For that necessary tables are created. Data from these tables will be then 
   used for plotting.
   The two tables created only if it dosent exist. Each run of the program makes
   sure that all the exisiting data in the table has been removed and only new
   data will be present.

   Created Date : 21/10/2024
   Last Modified Date : 24/10/2024

"""
# importing necessary modules
import sqlite3
from pathlib import Path
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from API_call import makeCSV, createCSV

def addDB(csv):
    """ Data from the CSV is loaded into the table "weather_data".
        From the table maximum (last) and minimum (earliest) dates 
        are taken.

    Args:
        csv (CSV): CSV with weather data.

    Returns:
        String: Maximum and minumum date values in string format
    """
#    Path('weatherData.db').touch()

    con = sqlite3.connect('weatherData.db')
    cur = con.cursor()

    cur.execute('''
     CREATE TABLE IF NOT EXISTS weather_data (
                name TEXT, datetime DATE, temp FLOAT, tempmax FLOAT, tempmin FLOAT, feelslike FLOAT, humidity FLOAT, windspeed FLOAT,\
                conditions TEXT, description TEXT, PRIMARY KEY (name, datetime))
     ''')
    cur.execute( 'DELETE FROM weather_data' )
    
     #cur.execute('''ALTER TABLE weather_data ADD tempmax FLOAT''')
     #cur.execute('''ALTER TABLE weather_data ADD tempmin FLOAT''')
     #cur.execute('''ALTER TABLE weather_data ADD feelslike FLOAT''')
    weather_data = csv
    weather_data.to_sql('weather_data', con, if_exists='append', index=False)
    con.commit() 
 
    query = 'SELECT MAX(datetime) as max_date, MIN(datetime) as min_date from weather_data'
    df = pd.read_sql_query(query, con)
    con.close()
    df_dict = df.to_dict('list')
    min_date = ((datetime.strptime(df_dict['min_date'][0], '%Y-%m-%d')) - relativedelta(years=1)).strftime('%Y-%m-%d')
    max_date = ((datetime.strptime(df_dict['max_date'][0], '%Y-%m-%d')) - relativedelta(years=1)).strftime('%Y-%m-%d')
 
    return min_date, max_date

def previousyearDB(csv):
    """ Data from the CSV is loaded into the table past_weather_data.
    This CSV contains data pertaining to the same date range but for 
    the previous year.

    Args:
        csv (CSV): Contains weather data for the same period previous year.
    """
    con = sqlite3.connect('weatherData.db')
    cur = con.cursor()

    cur.execute('''
     CREATE TABLE IF NOT EXISTS past_weather_data (
                name TEXT, datetime DATE, temp FLOAT, PRIMARY KEY (name, datetime))
     ''')
    cur.execute( 'DELETE FROM past_weather_data' )

    weather_data = csv
    weather_data.to_sql('past_weather_data', con, if_exists='append', index=False)
    con.commit() 
    con.close()

def main():

    city = input("Welcome to weather analysis. Please enter City Name (Example: New York): ").replace(' ', '%20')

    past_data = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/last7days?unitGroup=metric&include=days&key=YZ52UXBEQZEMH3KVBR5LNNXCT&contentType=csv'

    future_data =f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&include=days&key=YZ52UXBEQZEMH3KVBR5LNNXCT&contentType=csv'

    fromDB = addDB(makeCSV(past_data, future_data))

    last_year_data = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{fromDB[0]}/{fromDB[1]}?unitGroup=metric&include=days&key=YZ52UXBEQZEMH3KVBR5LNNXCT&contentType=csv'
    
    previousyearDB(createCSV(last_year_data, ['name', 'datetime', 'temp']))

if __name__ == "__main__":
   main()