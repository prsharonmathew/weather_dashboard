"""
    This program intends to create visualisations from data taken from the SQLite3 DataBase.
    Three plots are created. Plot 1 gives information about,1. Temperature V/s Date
    2. Feelslie V/s Date 3. Humidity V/s Date. Plot 2 gives information about Average, min and
    max temerature of each day. Plot 3 compares average temperature of the day for the entire 
    period with the last year data for the same period. 
    The final dashboard will be saved to the local device.

    Created Date : 21/10/2024
    Last Modified Date : 24/10/2024

"""

# Importing necessary modules
import matplotlib.pyplot as plt
import pandas as pd
import sqlite3

#connecting to database and retriving necessary data
conn = sqlite3.connect('weatherData.db')
cur = conn.cursor()
query1 = "SELECT datetime, humidity, tempmax, tempmin, temp, feelslike FROM weather_data"
query2 = "SELECT datetime, temp FROM past_weather_data"
df1 = pd.read_sql_query(query1, conn)
df2 = pd.read_sql_query(query2, conn)

#checking both tables contains data about the same city
cityname1 = [i for i in cur.execute(''' SELECT DISTINCT name FROM weather_data''')]
cityname2 = [i for i in cur.execute(''' SELECT DISTINCT name FROM past_weather_data''')]
conn.close()

city = None
if cityname1 == cityname2:
    city = cityname1[0][0]
else:
    raise ValueError("Error: The city names do not match.")

# Convert the 'datetime' column to datetime
df1['datetime'] = pd.to_datetime(df1['datetime'])

# Create figure layout
fig = plt.figure(figsize=(12, 8))
fig.suptitle(f'Weather Analysis Dashboard for {city}')

# Set up grid layout
gs = fig.add_gridspec(2, 2, height_ratios=[1, 1])

# Temperature, Feelslike, and Humidity V/s Date
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(df1['datetime'], df1['temp'], label='Temperature', marker='o')
ax1.plot(df1['datetime'], df1['feelslike'], label='Feelslike', marker='*', linestyle='--')
ax1.plot(df1['datetime'], df1['humidity'], label='Humidity', marker='+')
ax1.set_ylim(bottom=0)
ax1.set_ylabel('Temperature(°C) Humidity(g.m-3)')
ax1.set_xlabel('Date YY-MM-DD')
ax1.set_title('Temp, Feelslike, and Humidity over Time')
ax1.legend()
ax1.grid(True)

# Minimum, Maximum and Average Temperature V/s Date
ax2 = fig.add_subplot(gs[0, 1])
ax2.errorbar(df1['datetime'], df1['temp'], yerr=[df1['temp'] - df1['tempmin'], df1['tempmax'] - df1['temp']], fmt='o', ecolor='blue', capsize=5, label='Temperature')
ax2.set_ylim(bottom=0)
ax2.set_ylabel('Temperature (°C)')
ax2.set_xlabel('Date YY-MM-DD')
ax2.set_title('Min, Max, and Avg Temp')
ax2.legend()
ax2.grid(True)

# Current vs Previous Year Temp comparison
df1['mmdd'] = pd.to_datetime(df1['datetime']).dt.strftime('%m-%d')
df2['mmdd'] = pd.to_datetime(df2['datetime']).dt.strftime('%m-%d')

ax3 = fig.add_subplot(gs[1, :])
ax3.plot(df1['mmdd'], df1['temp'], label='Current Year', marker='o')
ax3.plot(df2['mmdd'], df2['temp'], label='Previous Year', marker='o', linestyle='--')
ax3.set_ylim(bottom=0)
ax3.set_ylabel('Temperature (°C)')
ax3.set_xlabel('Date MM-DD')
ax3.set_title('Current vs Previous Year Temperature Comparison')
ax3.legend()
ax3.grid(True)

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.savefig(f'weathergraph_{city}.jpg')
plt.show()