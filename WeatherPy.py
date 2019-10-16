#!/usr/bin/env python
# coding: utf-8

# # WeatherPy
# ----
# 
# #### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Setup Depeindencies
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import requests
import time
import urllib
from pprint import pprint

# import/hide api keys
from api_keys import api_key
api_key = f'&APPID={api_key}'

# url for openweathermap 
url = 'http://api.openweathermap.org/data/2.5/weather?q=' + api_key
print(url)


# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)


# ## Generate Cities List

# In[2]:


# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations based on a uniform distribution
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)
lat_lngs

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to the cities list
    if city not in cities:
        cities.append(city)

# Print the total number for the city count in cities to to confirm sufficient count
len(cities)


# In[3]:


# set list for city info
city_info = []


# In[4]:


# print to log beginning of call
print("Beginning Data Retrieval")
print('------------------------')

# set counters
record_count = 1
set_count = 1

# loops through all cities in the list
# enumerate function adds a counter to an iterable and returns it 
# based on the object enumerated
for i, city in enumerate(cities):
    
    
    # group cities in sets of 50 for logging purposes
    if (i % 50 == 0 and i >= 50):
        set_count += 1
        record_count = 0
        
    # create an endpoint url with each city    
    city_url = url + "&q=" + urllib.request.pathname2url(city)
    
    # log url, record and set numbers for the city data
    print(f"Processing Record {record_count} of Set {set_count} | {city}")
    print(city_url)
    
    # add 1 to the record counter
    record_count += 1
    
    # run an API request for each of the cities
    try:
          # parse the json and retrieve data
          city_weather = requests.get(city_url).json()
        
          # parse out the max temp, humidity, clouds, and wind speed
          city_lat = city_weather['coord']['lat']
          city_lng = city_weather['coord']['lng']
          city_max_temp = city_weather['main']['temp_max']
          city_humidity = city_weather['main']['humidity']
          city_clouds = city_weather['clouds']['all']
          city_wind = city_weather['wind']['speed']
          city_country = city_weather['sys']['country']
          city_date = city_weather['dt']
          
          # append information into a dataframe
          cityinfo.append({'City':city,
                          'Lats':city_lat,
                          'Lngs':city_lng,
                          'Temp':city_max_temp,
                          'Humidities':city_humidity,
                          'Cloudy':city_clouds,
                          'Wind':city_wind,
                          'Country':city_country,
                          'Date':city_date})
            
    # if an error is experienced skip it
    except:
          print('City not found. Skipping...')
          pass

# indicate when the load is complete
print('-----------------------')
print('Data Retrieval Complete')
print('-----------------------')


# ### Perform API Calls
# * Perform a weather check on each city using a series of successive API calls.
# * Include a print log of each city as it'sbeing processed (with the city number and city name).
# 

# In[5]:


# Base url for API call
url2 = 'http://api.openweathermap.org/data/2.5/weather?q=' 

# set information from the url API call into respective lists
New_Cities = []
Clouds = []
Countries = []
Humidities = []
Latitudes = []
Longitudes = []
Max_Temperatures = []
Wind_Speeds = []
Dates = []

# set forloop for the unique city for the different lng/lat of the cities data
for city in cities:
        
    Weather = requests.get(url2 + city + api_key).json()
        #pprint(Weather)
    
    if Weather['cod'] == 200:
        
        # append the information from the cities into the respective lists
        New_Cities.append(city)
            
        Cloudiness = Weather['clouds']['all']
        Clouds.append(Cloudiness)
    
        Country = Weather['sys']['country']
        Countries.append(Country)
    
        Humidity = Weather['main']['humidity']
        Humidities.append(Humidity)
    
        Lat = Weather['coord']['lat']
        Latitudes.append(Lat)
    
        Lng = Weather['coord']['lon']
        Longitudes.append(Lng)
    
        Max_Temp = Weather['main']['temp_max']
        Max_Temperatures.append(Max_Temp)
    
        Wind_Speed = Weather['wind']['speed']
        Wind_Speeds.append(Wind_Speed)
    
        Date = Weather['dt']
        Dates.append(Date)
        
# confirmation data retrieval is complete
print('Data Retrieval Complete')


# ### Convert Raw Data to DataFrame
# * Export the city data into a .csv.
# * Display the DataFrame
# 

# In[6]:


# using an f series, print the number of data points in the respective categories
print(f"cities: {len(New_Cities)}")
print(f"Clouds: {len(Clouds)}")
print(f"Countries: {len(Countries)}")
print(f"Humidities: {len(Humidities)}")
print(f"Latitudes: {len(Latitudes)}")
print(f"Longitudes: {len(Longitudes)}")
print(f"Max Temperatures: {len(Max_Temperatures)}")
print(f"Wind Speeds: {len(Wind_Speeds)}")
print(f"Dates: {len(Dates)}")


# In[9]:


# build a datafram using a new title and adding the appended info from the lists
city_data = pd.DataFrame({'City': New_Cities,
                           'Cloudiness': Clouds,
                           'Country': Countries,
                           'Date' : Dates,
                           'Humidity': Humidities,
                           'Lat': Latitudes,
                           'Lng': Longitudes,
                           'Max Temp': Max_Temperatures,
                           'Wind Speed': Wind_Speeds})

city_data.head()

output_data_file = "output_data_file/city_data.csv"
city_data.to_csv(output_data_file)


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### Latitude vs. Temperature Plot

# In[10]:


# set a scatterplot for the max temp
sns.set()
plt.scatter(city_data["Lat"], city_data["Max Temp"], marker="o", edgecolor='black', linewidth=1)

# Incorporate title, x and y label, and grids inth the graph properties
plt.title("City Latitude vs. Temperature (F)" + time.strftime('%x'))
plt.ylabel("Temperature")
plt.xlabel("Latitutde")
plt.grid(True)

# Save the figure
plt.savefig("Latitude_vs_Temp.png")

# Show plot
plt.show()


# #### Latitude vs. Humidity Plot

# In[11]:


# set a scatter plot for the humidity of the cities
sns.set()
plt.scatter(city_data["Lat"], city_data["Humidity"], marker="o", edgecolor='black', linewidth=1)

# Incorporate title, x and y label, and grids inth the graph properties
plt.title("City Latitude vs. Humidity (%)" + time.strftime('%x'))
plt.ylabel("Humidity (%)")
plt.xlabel("Latitutde")
plt.grid(True)

# Save the figure
plt.savefig("Latitude_vs_Humidity.png")

# Show plot
plt.show()


# #### Latitude vs. Cloudiness Plot

# In[12]:


# set a scatter plot for the cloudiness of the cities
sns.set()
plt.scatter(city_data["Lat"], city_data["Cloudiness"], marker="o", edgecolor='black', linewidth=1)

# Incorporate title, x and y label, and grids inth the graph properties
plt.title("City Latitude vs. Cloudiness (%)" + time.strftime('%x'))
plt.ylabel("Cloudiness (%)")
plt.xlabel("Latitutde")
plt.grid(True)

# Save the figure
plt.savefig("Latitude_vs_Cloudiness.png")

# Show plot
plt.show()


# #### Latitude vs. Wind Speed Plot

# In[13]:


# set a scatter plot for the wind speed of the cities
sns.set()
plt.scatter(city_data["Lat"], city_data["Wind Speed"], marker="o", edgecolor='black', linewidth=1)

# Incorporate title, x and y label, and grids inth the graph properties
plt.title("City Latitude vs. Windspeed (mph)" + time.strftime('%x'))
plt.ylabel("Windspeed (mph)")
plt.xlabel("Latitutde")
plt.grid(True)

# Save the figure
plt.savefig("Latitude_vs_Windspeed.png")

# Show plot
plt.show()


# In[ ]:




