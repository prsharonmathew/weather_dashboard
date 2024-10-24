"""
   Purpose of this program is to load data using the API call and refactor
   in the required form.Weather data from visualcrossing.com is used. No 
   particular limit w.r.t. API usage is mentioned in the documentation.For
   the three purposes (last 7 days, coming 15 days, previous year) done in
   this project three different url is used. The future temperature values 
   are already predicted by the API provider.

   Created Date : 21/10/2024
   Last Modified Date : 24/10/2024

"""

# Importing necessary modules
import sys
import urllib.request
import codecs
import pandas as pd
import io

def createCSV(url, columns):
   """ Create a CSV file with required columns from the API to load into the database. 

   Args:
       url (string): url of the API
       columns (list): list of columns to be included

   Returns:
       csv: A CSV file with the deired columns is returned.
   """   
   try: 
      urlresponse = codecs.iterdecode(urllib.request.urlopen(url), 'utf-8')
      urlresponse_str = io.StringIO(''.join(urlresponse))

      csv_data = pd.read_csv(urlresponse_str, usecols=columns)
      
      return csv_data

   except urllib.error.HTTPError  as e:
        errorinfo= e.read().decode() 
        print('Error code: ', e.code, errorinfo)
        sys.exit()
   except  urllib.error.URLError as e:
      errorinfo= e.read().decode() 
      print('Error code: ', e.code,errorinfo)
      sys.exit() 

def makeCSV(last7,Next15):
   """Combine the two CSV files into one.

   Args:
       last7 (CSV): Contains data for the last 7 days
       Next15 (CSV):  Contains data for the next 15 days

   Returns:
       CSV: Combined CSV file with full data.
   """
   columns= ['name', 'datetime', 'temp', 'tempmax', 'tempmin' ,'humidity', 'windspeed', 'conditions', 'description','feelslike']

   csv7 = createCSV(last7, columns)
   csv15 = createCSV(Next15, columns)

   comb_file = pd.concat([csv7, csv15], ignore_index=True)

   return comb_file
