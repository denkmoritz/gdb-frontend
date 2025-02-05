import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import branca.colormap as cm
from folium.plugins import HeatMap

# Constants
BACKEND_URL = "http://localhost:5003/api"
DEFAULT_LOCATION = [53.55, 10.0]  # Hamburg example

# Initialize session state variables
if "amenity" not in st.session_state:
    st.session_state.amenity = None
if "heatmap_data" not in st.session_state:
    st.session_state.heatmap_data = None
if "voronoi_data" not in st.session_state:
    st.session_state.voronoi_data = None

st.set_page_config(layout="wide")

# Sidebar settings
with st.sidebar:
    st.header("⚙️ Settings")

    # Dropdown selection for amenities
    amenity_options = [
        "restaurant", "cafe", "fast_food", "charging_station",
        "pub", "bicycle_parking", "bicycle_renting", "bicycle_repair_station"
    ]

    amenity = st.selectbox(
        "Select Amenity Type:",
        options=["Select an amenity..."] + amenity_options,
        index=0,
        help="Choose an amenity type from the list."
    )

    # Checkboxes for choosing overlays
    show_voronoi = st.checkbox("Show Voronoi", value=True)
    show_heatmap = st.checkbox("Show Heatmap", value=True)

    # Button to fetch data
    if st.button("🔍 Generate Map"):
        if amenity != "Select an amenity...":
            st.session_state.amenity = amenity
            st.session_state.heatmap_data = None  # Reset heatmap data
            st.session_state.voronoi_data = None  # Reset Voronoi data
        else:
            st.warning("⚠️ Please select a valid amenity type.")

# Show intro page before generating the map
if not st.session_state.amenity:
    st.title("🌍 OSM Amenity Analysis")
    st.markdown("Explore different spatial analyses of OpenStreetMap data in Hamburg.")
    st.markdown("- Select an amenity and choose overlays from the sidebar.")
    st.markdown("- Click 'Generate Map' to visualize the data.")
    st.stop()

# Fetch data only when needed
params = {"amenity": st.session_state.amenity}

if show_heatmap and st.session_state.heatmap_data is None:
    with st.spinner("⏳ Fetching heatmap data..."):
        try:
            response = requests.get(f"{BACKEND_URL}/heatmap", params=params)
            if response.status_code == 200:
                st.session_state.heatmap_data = response.json()
            else:
                st.error(f"Error loading heatmap data: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

if show_voronoi and st.session_state.voronoi_data is None:
    with st.spinner("⏳ Fetching Voronoi data..."):
        try:
            response = requests.get(f"{BACKEND_URL}/voronoi", params=params)
            if response.status_code == 200:
                st.session_state.voronoi_data = response.json()
            else:
                st.error(f"Error loading Voronoi data: {response.text}")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# Create a Folium map
m = folium.Map(location=DEFAULT_LOCATION, zoom_start=11, control_scale=True)

# Add Voronoi first (if selected)
if show_voronoi and st.session_state.voronoi_data:
    colormap = cm.linear.Blues_09.scale(0, 1)

    folium.GeoJson(
        st.session_state.voronoi_data,
        name="Voronoi Polygons",
        style_function=lambda feature: {
            "fillColor": colormap(0.5),
            "color": "black",
            "weight": 1.5,
            "fillOpacity": 0.4
        }
    ).add_to(m)

# Add Heatmap second (so it overlays Voronoi)
if show_heatmap and st.session_state.heatmap_data:
    heatmap_data = [
        [feature["geometry"]["coordinates"][1], feature["geometry"]["coordinates"][0]]
        for feature in st.session_state.heatmap_data["features"]
    ]

    HeatMap(heatmap_data, radius=15, blur=10).add_to(m)

# Display the map
st_folium(m, use_container_width=True, height=1000, key="map")