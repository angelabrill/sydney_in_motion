from shapely.geometry import box
import geopandas as gpd
import matplotlib.pyplot as plt



def revise_sa2():

    # Load your large GeoJSON
    gdf = gpd.read_file("data/NSW_SA2.geojson")

    # Define bounding box for Sydney CBD (adjust as needed)
    cbd_bbox = box(151.160, -33.918, 151.225, -33.850)

    # Filter features that intersect the CBD bounding box
    cbd_gdf = gdf[gdf.intersects(cbd_bbox)]

    # Save to a new GeoJSON
    cbd_gdf.to_file("data/Sydney_SA2.geojson", driver="GeoJSON")
    

def show_sa2():
    # Load the GeoJSON file
    gdf = gpd.read_file("data/Sydney_SA2.geojson")
    print(type(gdf))

    output_folder = "output/sa2"
    
    gdf_save = gdf
    gdf_save.drop(columns="geometry").to_csv("data/sydney_sa2_data.csv", index=False)

    # Plot with boundaries and labels
    fig, ax = plt.subplots(figsize=(12, 10))
    gdf.boundary.plot(ax=ax, color="black")  # draw boundaries
    gdf.plot(ax=ax, color="lightblue", alpha=0.5)  # fill polygons

    # Add labels (e.g., LGA name from properties)
    for idx, row in gdf.iterrows():
        if row.geometry.representative_point().is_empty:
            continue
        plt.text(
            row.geometry.representative_point().x,
            row.geometry.representative_point().y,
            row['nsw_loca_2'],  # or any other field for label
            fontsize=6,
            ha='center'
        )

    ax.set_title("Sydney SA2s", fontsize=16)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/Sydney_SA2s.png", dpi=300)
    plt.show()
    
    

revise_sa2()
show_sa2()
