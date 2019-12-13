#!/usr/bin/env python
# coding: utf-8

# In[1]:


import gmaps
import gmaps.datasets
import csv
import pandas as pd
import requests
import time
import gmaps.geojson_geometries


# In[2]:

# In[3]:


def lat_long(apikey,address):
    address_change = address.replace(' ','+')
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address_change}&key={apikey}'
    try:
        response = requests.get(url)
        response = response.json()['results'][0]['geometry']['location']
        return response
    except:
        return {}


# In[4]:

if __name__ == "__main__":
    def google_map(apikey,address):
        result = ''
        address_change = address.replace(' ','+')
        url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address_change}&key={apikey}'
        response = requests.get(url)
        response = response.json()['results'][0]['address_components']
        for item in response:
            if item['types'][0] == 'administrative_area_level_1' :
                result = item['short_name']
        return result
    
    
    # In[6]:
    
    data_1 = pd.read_csv('../data/pdtable_content.csv')
    api_key = 'AIzaSyCxhj17KVAxfh0qOZABYxzO5wBJni5z9oU'
    
    result = []
    for item in data_1['job location'][:10]:
        result.append(lat_long(api_key,item))
        time.sleep(0.2)
    
    
    # In[7]:
    
    
    locations = pd.DataFrame(result)
    locations['mg'] = 0.1
    locations[['lat','lng']]
    
    
    # In[8]:
    
    
    gmaps.configure(api_key='AIzaSyCxhj17KVAxfh0qOZABYxzO5wBJni5z9oU')
    
    
    # In[9]:
    
    
    fig = gmaps.figure()
    heatmap_layer = gmaps.heatmap_layer(locations[['lat','lng']],weights = locations['mg'],max_intensity = 2)
    fig.add_layer(heatmap_layer)
    fig

