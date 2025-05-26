import geopandas as gpd
import pandas as pd
from shapely.geometry import shape
import matplotlib.pyplot as plt
import contextily as ctx
from adjustText import adjust_text


if __name__ == "__main__":
    cycle_data = 'data/Cycle_network.geojson'
    suburbs_data = 'data/Sydney_SA2.geojson'
    age_data = 'data/age_suburb_census.csv'
    output_folder = 'output/sa2'
    
    cycle_network_gdf = gpd.read_file(cycle_data)
    cycle_network_gdf.set_crs("EPSG:4326", inplace=True)
    suburbs_gdf = gpd.read_file(suburbs_data)
    suburbs_gdf = suburbs_gdf.to_crs(cycle_network_gdf.crs)
    
    age_df = pd.read_csv(age_data)
    # Clean age data
    age_df.columns = ["nsw_loca_2", "age_2021"]
    age_df["age_2021"] = pd.to_numeric(age_df["age_2021"], errors="coerce")
    
    # Attempt to fix invalid geometries
    suburbs_gdf["geometry"] = suburbs_gdf["geometry"].buffer(0)
        
    # Join with suburb boundaries
    joined_gdf = gpd.sjoin(cycle_network_gdf, suburbs_gdf, how="left", predicate="intersects")
    joined_gdf.to_file(f"{output_folder}/SA2_joined_output.geojson", driver="GeoJSON")
    
    # Plot
    fig, ax = plt.subplots(figsize=(12, 12))
    suburbs_gdf.plot(ax=ax, column="nsw_loca_2", cmap="tab20", edgecolor="black", linewidth=0.3, alpha=0.4)
    cycle_network_gdf.plot(ax=ax, color="black", linewidth=0.5)


    plt.title("Cycle Network with Suburb Boundaries")
    plt.axis("off")
    plt.savefig(f"{output_folder}/sa2_joined.png", dpi=300)
    plt.close()
    # plt.show()
    
    # Sum lengths of cycle routes per suburb
    summary_df = joined_gdf.groupby("nsw_loca_2")["Shape__Length"].sum().reset_index()
    summary_df = summary_df.sort_values("Shape__Length", ascending=False)
    summary_df["total_km"] = (summary_df["Shape__Length"] / 1000).round(2)
    summary_df.to_csv(f"{output_folder}/sa2_suburb_cycle_summary.csv", index=False)
    # print(summary_df)
    
    counts_df = joined_gdf["nsw_loca_2"].value_counts().reset_index()
    counts_df.to_csv(f"{output_folder}/sa2_suburb_cycle_counts.csv", index=False)
    # print(counts)
    
    route_types_df = joined_gdf.groupby(["nsw_loca_2", "RouteType"]).size().unstack(fill_value=0).reset_index()
    route_types_df.to_csv(f"{output_folder}/sa2_route_types_by_suburb.csv", index=False)
    # print(route_types)
    
   
    suburbs_age_gdf = suburbs_gdf.merge(age_df, on="nsw_loca_2", how="left")
    
    fig, ax = plt.subplots(figsize=(12, 12))
    suburbs_age_gdf.plot(ax=ax, column="age_2021", cmap="coolwarm_r", edgecolor="black", linewidth=0.3, legend=True)
    cycle_network_gdf.plot(ax=ax, color="black", linewidth=0.5)
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, crs=suburbs_gdf.crs.to_string())

    plt.title("Cycle Network Overlaid with Median Age by Suburb")
    plt.axis("off")
    plt.savefig(f"{output_folder}/sa2_age_overlay.png", dpi=300)
    plt.close()
    
    young_suburbs = suburbs_age_gdf[suburbs_age_gdf["age_2021"] <= 35]
    
    # Merge all dataframes on suburb
    final_df = age_df.merge(summary_df, on="nsw_loca_2", how="left")
    final_df = final_df.merge(counts_df, on="nsw_loca_2", how="left")
    final_df = final_df.merge(route_types_df, on="nsw_loca_2", how="left")
    
    # Fill NaNs with 0 for route analysis
    route_columns = [
        "Direct route with higher traffic", 
        "Low-traffic on-road quiet route", 
        "Off-Road shared path", 
        "Regional cycle route", 
        "Separated off-road cycleway"
    ]
    final_df[route_columns] = final_df[route_columns].fillna(0)
    
    # Top 10 youngest suburbs with most cycling infrastructure
    young_and_cycled = final_df[final_df["age_2021"] <= 35].sort_values(by="total_km", ascending=False)
    print("🟢 Top Young Suburbs with Longest Cycle Routes:")
    print(young_and_cycled[["nsw_loca_2", "age_2021", "total_km", "count"]].head(10))
    young_and_cycled.to_csv(f"{output_folder}/young_cycled.cs")
    

    # Suburbs with high route count but older populations
    older_cycled = final_df[final_df["age_2021"] > 40].sort_values(by="count", ascending=False)
    print("\n🔵 Older Suburbs with Dense Cycling Network:")
    print(older_cycled[["nsw_loca_2", "age_2021", "total_km", "count"]].head(10))

    # Top suburbs with many *low-traffic* or *off-road* paths (more beginner-friendly)
    final_df["friendly_routes"] = final_df["Low-traffic on-road quiet route"] + final_df["Off-Road shared path"] + final_df["Separated off-road cycleway"]
    friendly_suburbs = final_df.sort_values(by="friendly_routes", ascending=False)
    print("\n🟡 Suburbs with Most Beginner-Friendly Routes:")
    print(friendly_suburbs[["nsw_loca_2", "friendly_routes", "age_2021"]].head(10))

    # Suburbs with high youth but low infrastructure (potential targets)
    potential_initiatives = final_df[(final_df["age_2021"] <= 33) & (final_df["total_km"] < 15)]
    print("\n🔴 Young Suburbs with Low Cycling Infrastructure (Opportunities):")
    print(potential_initiatives[["nsw_loca_2", "age_2021", "total_km", "count"]])
    potential_initiatives.to_csv(f"{output_folder}/potential_targets.csv")
    
    
    top_young = final_df[final_df["age_2021"] <= 35].sort_values("total_km", ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(top_young["nsw_loca_2"], top_young["total_km"], color="skyblue")
    plt.xlabel("Total Cycle Route Length (km)")
    plt.title("Top Young Suburbs with Longest Cycle Routes")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(f"{output_folder}/top_young_suburbs_cycle.png", dpi=300)
    plt.show()
    
    plt.figure(figsize=(8, 6))
    plt.scatter(final_df["age_2021"], final_df["total_km"], alpha=0.7)
    plt.xlabel("Median Age (2021)")
    plt.ylabel("Total Cycle Route Length (km)")
    plt.title("Cycle Infrastructure vs Median Age by Suburb")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{output_folder}/age_vs_cycle_length.png", dpi=300)
    plt.show()


    # Define target suburbs
    target_suburbs = final_df[(final_df["age_2021"] <= 33) & (final_df["total_km"] < 15)]
    highlight_gdf = suburbs_gdf[suburbs_gdf["nsw_loca_2"].isin(target_suburbs["nsw_loca_2"])]

    # Base map
    fig, ax = plt.subplots(figsize=(12, 12))
    suburbs_gdf.plot(ax=ax, color="lightgrey", edgecolor="black", linewidth=0.3)
    highlight_gdf.plot(ax=ax, color="orange", edgecolor="red", linewidth=1, label="Target Suburbs")
    cycle_network_gdf.plot(ax=ax, color="black", linewidth=0.4, alpha=0.6)

    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, crs=suburbs_gdf.crs.to_string())
    plt.title("Young Suburbs with Low Cycle Infrastructure")
    plt.axis("off")
    plt.legend()
    plt.savefig(f"{output_folder}/target_youth_lowinfra_map.png", dpi=300)
    plt.show()
    
    
    # Merge suburb geometries with cycle and age data
    merged_gdf = suburbs_gdf.merge(final_df, on="nsw_loca_2", how="left")

    # Filter for target suburbs: young + good cycle infra
    target_suburbs = merged_gdf[
        (merged_gdf["age_2021"] <= 33) & 
        (merged_gdf["total_km"] >= 20)
    ]

    # Plot map
    fig, ax = plt.subplots(figsize=(12, 12))

    # Base suburbs in grey
    merged_gdf.plot(ax=ax, color="lightgrey", edgecolor="white", linewidth=0.3)

    # Highlight target suburbs in green
    target_suburbs.plot(ax=ax, color="mediumseagreen", edgecolor="darkgreen", linewidth=0.7, label="Young + Good Cycle Infra")

    # Add cycle network on top
    cycle_network_gdf.plot(ax=ax, color="black", linewidth=0.5, alpha=0.7)

    # Basemap for context
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron, crs=suburbs_gdf.crs.to_string())

    # Annotations
    plt.title("Target Suburbs: Young Demographic & Cycle Infrastructure", fontsize=14)
    plt.axis("off")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{output_folder}/young_cycle_suburbs_map.png", dpi=300)
    plt.show()