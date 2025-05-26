import contextily as ctx
import requests
import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
import matplotlib.pyplot as plt


def load_dataset(path):
    
    gdf = gpd.read_file(path)
    # print(type(gdf)) <class 'geopandas.geodataframe.GeoDataFrame'>
    gdf.set_crs("EPSG:4326", inplace=True)
    print(gdf.head())
    
    return gdf

if __name__ == "__main__":
    path = 'data/Cycle_network.geojson'
    output_folder = 'output'
    gdf = load_dataset(path)
    # Reproject to EPSG:3857
    gdf = gdf.to_crs(epsg=3857)

    # Basic stats
    print("Route Types:\n", gdf["RouteType"].value_counts())
    print("\nTotal Length:", gdf["Shape__Length"].sum())
    print("Average Length:", gdf["Shape__Length"].mean())
    print("Source:\n", gdf["Source"].value_counts())
    
    # Save value counts and grouped stats as CSV
    gdf["RouteType"].value_counts().to_csv(f"{output_folder}/route_type_counts.csv")
    gdf["Source"].value_counts().to_csv(f"{output_folder}/source_counts.csv")
    

    # Grouped stats
    length_by_type = gdf.groupby("RouteType")["Shape__Length"].sum()
    length_by_type.to_csv(f"{output_folder}/length_by_route_type.csv")
    print("\nTotal length by Route Type:\n", length_by_type)

    # Visualisation 
    
    # Plot with basemap
    fig, ax = plt.subplots(figsize=(12, 8))
    gdf.plot(column="RouteType", ax=ax, legend=True, alpha=0.7, edgecolor='k')
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik) 
    plt.title("Sydney Cycleways by Route Type with Basemap")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/sydney_cycleways_with_basemap.png", dpi=300)
    plt.close()
    
  
