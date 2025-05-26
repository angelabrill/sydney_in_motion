import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
import matplotlib.pyplot as plt
import contextily as ctx


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

    # Basic stats
    print("Route Types:\n", gdf["RouteType"].value_counts())
    print("\nTotal Length:", gdf["Shape__Length"].sum())
    print("Average Length:", gdf["Shape__Length"].mean())
    
    # Save value counts and grouped stats as CSV
    gdf["RouteType"].value_counts().to_csv(f"{output_folder}/route_type_counts.csv")
    gdf["Source"].value_counts().to_csv(f"{output_folder}/source_counts.csv")
    

    # Grouped stats
    length_by_type = gdf.groupby("RouteType")["Shape__Length"].sum()
    length_by_type.to_csv(f"{output_folder}/length_by_route_type.csv")
    print("\nTotal length by Route Type:\n", length_by_type)

    # Visualisation 
    
    # Plot Sydney Cycleways by Route Type
    fig, ax = plt.subplots(figsize=(12, 8))
    gdf.plot(column="RouteType", ax=ax, legend=True)
    plt.title("Sydney Cycleways by Route Type")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/sydney_cycleways_by_route_type.png", dpi=300)
    plt.close()
    
 
    # Plot RouteType distribution
    plt.figure(figsize=(8, 5))
    gdf["RouteType"].value_counts().plot(kind='bar', color='skyblue')
    plt.title("Count of Route Types")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/route_type_counts.png")
    plt.close()

    # Plot total length by RouteType
    plt.figure(figsize=(8, 5))
    length_by_type.plot(kind='bar', color='orange')
    plt.title("Total Length by Route Type")
    plt.ylabel("Length")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/length_by_route_type.png")
    plt.close()
    
    
    # Plot with basemap
    gdf_basemap = gdf.to_crs(epsg=3857)
    # Define custom color map
    unique_types = gdf_basemap["RouteType"].unique()
    color_map = dict(zip(unique_types, plt.cm.Set1.colors[:len(unique_types)]))
        
    fig, ax = plt.subplots(figsize=(12, 8))
    # Plot each RouteType separately to control color
    for route_type, color in color_map.items():
        subset = gdf_basemap[gdf_basemap["RouteType"] == route_type]
        subset.plot(ax=ax, color=color, label=route_type, edgecolor="k", alpha=0.7)
        
    # Add basemap
    # gdf_basemap.plot(column="RouteType", ax=ax, legend=True, alpha=0.7, edgecolor='k', categorical=True)
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron) 
    plt.title("Sydney Cycleways by Route Type with Basemap")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/sydney_cycleways_with_basemap.png", dpi=300)
    plt.close()
    

