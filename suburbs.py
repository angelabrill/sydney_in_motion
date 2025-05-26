import geopandas as gpd
import matplotlib.pyplot as plt

def nsw_lgas():

    # Load the GeoJSON file
    gdf = gpd.read_file("data/LGAs_Sydney_and_surrounds.json")

    output_folder = "output"

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
            row['NSW_LGA__3'],  # or any other field for label
            fontsize=5,
            ha='center'
        )

    ax.set_title("New South Wales LGAs", fontsize=16)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/NSW_LGAs.png", dpi=300)
    plt.show()


def nsw_lgas():

    # Load the GeoJSON file
    gdf = gpd.read_file("data/Sydney_LGAs.json")
    print(type(gdf))

    output_folder = "output"

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
            row['NSW_LGA__3'],  # or any other field for label
            fontsize=6,
            ha='center'
        )

    ax.set_title("Sydney LGAs", fontsize=16)
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(f"{output_folder}/Sydney_LGAs.png", dpi=300)
    plt.show()


nsw_lgas()