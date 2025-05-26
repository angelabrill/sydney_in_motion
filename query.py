import requests

# Drinking_fountains
url = "https://services1.arcgis.com/cNVyNtjGVZybOQWZ/arcgis/rest/services/Drinking_fountains/FeatureServer/0/query"

# Parameters 
params = {
    "where": "1=1",           # get all data
    "outFields": "*",         # get all fields
    "outSR": "4326",          # output spatial reference
    "f": "json"               # format
}

# Make the request
response = requests.get(url, params=params)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code {response.status_code}")
