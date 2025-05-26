import geopandas as gpd
import json

# Load GeoJSON file from a file path
# geojson_data = gpd.read_file('data/Bicycle_parking.geojson')
# print(type(geojson_data)) # <class 'geopandas.geodataframe.GeoDataFrame'>

# Paste your geojson snippet here as a string or dict
geojson_data = {
    "type": "FeatureCollection",
    "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
    "features": [
        {
            "type": "Feature",
            "id": 1,
            "geometry": {
                "type": "Point",
                "coordinates": [151.205525524575, -33.8741663156203]
            },
            "properties": {
                "OBJECTID": 1,
                "AssetID": "00393974",
                "Type": "O-Ring",
                "StreetName": "Bathurst Street",
                "Suburb": "Sydney",
                "Postcode": "2000"
            }
        },
        {
            "type": "Feature",
            "id": 2,
            "geometry": {
                "type": "Point",
                "coordinates": [151.205647494692, -33.8741702563197]
            },
            "properties": {
                "OBJECTID": 2,
                "AssetID": "00393975",
                "Type": "O-Ring",
                "StreetName": "Bathurst Street",
                "Suburb": "Sydney",
                "Postcode": "2000"
            }
        },
    ]
}

print(type(geojson_data))

# Convert to GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])
print(type(gdf))

# Set the CRS if it's not automatically recognized
gdf.set_crs("EPSG:4326", inplace=True)

# Preview the result
print(gdf.head())
