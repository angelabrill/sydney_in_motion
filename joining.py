import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
import matplotlib.pyplot as plt
import contextily as ctx



if __name__ == "__main__":
    cycle_data = 'data/Cycle_network.geojson'
    suburbs_data = 'data/Sydney_LGAs.json'
    output_folder = 'output'
    
    cycle_network_gdf = gpd.read_file(cycle_data)
    cycle_network_gdf.set_crs("EPSG:4326", inplace=True)
    suburbs_gdf = gpd.read_file(suburbs_data)
    suburbs_gdf = suburbs_gdf.to_crs(cycle_network_gdf.crs)
    
    # Attempt to fix invalid geometries
    suburbs_gdf["geometry"] = suburbs_gdf["geometry"].buffer(0)
    
    print(cycle_network_gdf.crs)
    print(suburbs_gdf.crs)
    
    print(suburbs_gdf.is_empty.any(), cycle_network_gdf.is_empty.any())
    print(suburbs_gdf.is_valid.all(), cycle_network_gdf.is_valid.all())
    
    # Join with suburb boundaries
    joined_gdf = gpd.sjoin(cycle_network_gdf, suburbs_gdf, how="left", predicate="intersects")
    joined_gdf.to_file("output/joined_output.geojson", driver="GeoJSON")
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 12))
    suburbs_gdf.plot(ax=ax, facecolor="lightgrey", edgecolor="black", linewidth=0.5, alpha=0.5)
    cycle_network_gdf.plot(ax=ax, color="blue", linewidth=1)

    suburbs_gdf["label_pos"] = suburbs_gdf.geometry.representative_point()
    for idx, row in suburbs_gdf.iterrows():
        ax.text(row["label_pos"].x, row["label_pos"].y, row["NSW_LGA__3"], fontsize=8)

    plt.title("Cycle Network with Suburb Boundaries")
    plt.axis("off")
    ## Uncomment when you want to see the graph
    # plt.savefig(f"{output_folder}/joined_cycle_suburbs.png", dpi=300)
    # plt.close()
    
    # Sum lengths of cycle routes per suburb
    summary = joined_gdf.groupby("NSW_LGA__3")["Shape__Length"].sum().reset_index()
    summary = summary.sort_values("Shape__Length", ascending=False)
    summary["total_km"] = (summary["Shape__Length"] / 1000).round(2)
    summary.to_csv(f"{output_folder}/suburb_cycle_summary.csv", index=False)
    print(summary)
    
    counts = joined_gdf["NSW_LGA__3"].value_counts().reset_index()
    counts.to_csv(f"{output_folder}/suburb_cycle_counts.csv", index=False)
    print(counts)
    
    route_types = joined_gdf.groupby(["NSW_LGA__3", "RouteType"]).size().unstack(fill_value=0).reset_index()
    route_types.to_csv(f"{output_folder}/route_types_by_suburb.csv", index=False)
    print(route_types)
    
