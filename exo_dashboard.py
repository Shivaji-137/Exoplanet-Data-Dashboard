import streamlit as st
import pandas as pd
import plotly.express as px
from astroquery.ipac.nexsci.nasa_exoplanet_archive import NasaExoplanetArchive

# Function to retrieve exoplanet data using Astroquery
@st.cache_data
def fetch_exoplanet_data():
    columns = [
        "pl_name",       # Planet Name
        "hostname",      # Host Star Name
        "discoverymethod",  # Discovery Method
        "sy_dist",       # Distance to Star (pc)
        "pl_bmasse",     # Planet Mass (Earth Masses)
        "pl_rade",       # Planet Radius (Earth Radii)
        "pl_orbper",     # Orbital Period (days)
        "pl_trandep",    # Transit Depth
        "pl_trandur",    # Transit Duration (hours)
        "st_teff",       # Stellar Effective Temperature (K)
        "st_lum",        # Stellar Luminosity (Solar Luminosities)
        "st_rad",        # Stellar Radius (Solar Radii)
        "sy_gaiamag"     # Gaia Magnitude of the Star
    ]
    query = NasaExoplanetArchive.query_criteria(
        table="ps",
        select=",".join(columns),
        where="pl_bmasse IS NOT NULL AND pl_rade IS NOT NULL AND pl_orbper IS NOT NULL"
    )
    return query.to_pandas()

# Main dashboard function
def main():
    st.title("Exoplanet Data Dashboard")
    st.markdown("Explore various properties of exoplanets and their host stars using this interactive dashboard.")
    st.markdown("Created by Shivaji Chaulagain")
    # Fetch data
    with st.spinner("Fetching data from NASA Exoplanet Archive..."):
        data = fetch_exoplanet_data()

    # Sidebar filters
    st.sidebar.header("Filters")
    # st.sidebar.subheader("General Filters")
    discovery_method = st.sidebar.multiselect(
        "Discovery Method", data['discoverymethod'].unique(), default=data['discoverymethod'].unique()
    )
    distance_range = st.sidebar.slider(
        "Distance to Star (parsecs):", float(data['sy_dist'].min()), float(data['sy_dist'].max()), 
        (10.0, 500.0)
    )
    mass_range = st.sidebar.slider(
        "Planetary Mass (Earth Masses):", float(data['pl_bmasse'].min()), float(data['pl_bmasse'].max()), 
        (0.0, 50.0)
    )

    # Filter data based on user selection
    filtered_data = data[
        (data['discoverymethod'].isin(discovery_method)) &
        (data['sy_dist'] >= distance_range[0]) & 
        (data['sy_dist'] <= distance_range[1]) &
        (data['pl_bmasse'] >= mass_range[0]) &
        (data['pl_bmasse'] <= mass_range[1])
    ]

    # Display filtered data
    st.write("### Filtered Dataset")
    st.write("* Data is filtered by distance, mass and discovery method. Check the sidebar for filter options.")
    st.write(f"Number of entries: {len(filtered_data)}")
    st.dataframe(filtered_data)

    # Visualization options
    st.sidebar.header("Visualizations")
    viz_options = st.sidebar.multiselect(
        "Choose Visualizations:",
        ["Discoverymethod distribution Pie plot", "Mass Distribution", "Radius vs Orbital Period", "Transit Depth vs Duration", 
         "Stellar Temperature vs Luminosity", "Custom Scatter Plots"],
        default=["Discoverymethod distribution Pie plot", "Mass Distribution", "Radius vs Orbital Period","Transit Depth vs Duration", 
         "Stellar Temperature vs Luminosity", "Custom Scatter Plots"]
    )

    # Visualizations
    if "Discoverymethod distribution Pie plot" in viz_options:
        st.write("### Exoplanet Distribution by discoverymethod (Pie chart)")
        fig = px.pie(filtered_data, names='discoverymethod', title="Exoplanet Distribution",
                     template="plotly_dark", hole=0.5)
        st.plotly_chart(fig)

    if "Mass Distribution" in viz_options:
        st.write("### Planetary Mass Distribution")
        fig = px.histogram(filtered_data, x='pl_bmasse', nbins=30, title="Mass Distribution",
                           labels={"pl_bmasse": "Mass (Earth Masses)"}, template="plotly_dark", color='discoverymethod', marginal="rug", opacity=0.7)
        st.plotly_chart(fig)

    if "Radius vs Orbital Period" in viz_options:
        st.write("### Radius vs Orbital Period")
        fig = px.scatter(filtered_data, x='pl_orbper', y='pl_rade', size='pl_bmasse', color='discoverymethod',
                         title="Radius vs Orbital Period",
                         labels={"pl_orbper": "Orbital Period (days)", "pl_rade": "Radius (Earth Radii)"},
                         template="plotly_dark")
        st.plotly_chart(fig)

    if "Transit Depth vs Duration" in viz_options:
        st.write("### Transit Depth vs Duration")
        fig = px.scatter(filtered_data, x='pl_trandep', y='pl_trandur', color='discoverymethod', size='pl_bmasse',
                         title="Transit Depth vs Duration",
                         labels={"pl_trandep": "Transit Depth", "pl_trandur": "Transit Duration (hours)"},
                         template="plotly_dark")
        st.plotly_chart(fig)

    if "Stellar Temperature vs Luminosity" in viz_options:
        st.write("### Stellar Temperature vs Luminosity")
        fig = px.scatter(filtered_data, x='st_teff', y='st_lum', color='discoverymethod',
                         title="Stellar Temperature vs Luminosity",
                         labels={"st_teff": "Stellar Temperature (K)", "st_lum": "Stellar Luminosity (L☉)"},
                         template="plotly_dark")
        st.plotly_chart(fig)


    if "Custom Scatter Plots" in viz_options:
        st.write("### Custom Scatter Plot")
        st.write("If you don't understand the terms like pl_bmasse, pl_rade, etc., please refer to the [terms explanation](https://github.com/Shivaji-137/Exoplanet-Data-Dashboard/blob/main/explanation_of_termsin_nasaarchiveexopl.md)")
        x_axis = st.selectbox("X-axis:", data.columns, index=data.columns.get_loc('pl_bmasse'))
        y_axis = st.selectbox("Y-axis:", data.columns, index=data.columns.get_loc('pl_rade'))
        color = st.selectbox("Color By:", data.columns, index=data.columns.get_loc('discoverymethod'))
        fig = px.scatter(filtered_data, x=x_axis, y=y_axis, color=color,
                         title=f"{x_axis} vs {y_axis}",
                         template="plotly_dark")
        st.plotly_chart(fig)

    # Footer
    st.markdown("---")
    st.markdown("Data Source: [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)")
    st.markdown("Created using [Astroquery](https://astroquery.readthedocs.io/) and [Streamlit](https://streamlit.io/)")
    st.markdown('<p style="text-align: center;">Copyright © 2025 Shivaji Chaulagain</p>', unsafe_allow_html=True)
# Run the app
if __name__ == "__main__":
    main()

    