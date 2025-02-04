import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import branca.colormap as cm

# Constants
BACKEND_URL = "http://localhost:5003/api/voronoi"
DEFAULT_LOCATION = [53.55, 10.0]  # Default map center (Hamburg example)

# Initialize session state
if "amenity" not in st.session_state:
    st.session_state.amenity = "cafe"
if "voronoi_data" not in st.session_state:
    st.session_state.voronoi_data = None
if "run_query" not in st.session_state:
    st.session_state.run_query = False

# Streamlit UI
st.set_page_config(layout="wide")
st.title("🌍 Voronoi Amenity Map")
st.markdown(f"Voronoi tessellation of {st.session_state.amenity}s in Hamburg using OpenStreetMap data.")

# Sidebar for user inputs
with st.sidebar:
    st.header("⚙️ Settings")
    amenity = st.text_input(
        "Amenity Type:",
        value=st.session_state.amenity,
        help="Type of amenity to search for (e.g., cafe, restaurant, bar, bank)."
    )

    # Button to fetch data
    if st.button("🔍 Generate Voronoi Map"):
        st.session_state.amenity = amenity
        st.session_state.run_query = True

# Fetch Data Only When Button Clicked
if st.session_state.run_query:
    st.write("⏳ Fetching Voronoi data...")

    params = {"amenity": st.session_state.amenity}

    try:
        response = requests.get(BACKEND_URL, params=params)
        if response.status_code == 200:
            st.session_state.voronoi_data = response.json()
            st.success("✅ Voronoi data loaded successfully!")
        else:
            st.error(f"❌ Error loading data: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {e}")

    # Reset query flag
    st.session_state.run_query = False

# Show Map If Data Exists
if st.session_state.voronoi_data:
    # Create a larger Folium map
    m = folium.Map(location=DEFAULT_LOCATION, zoom_start=10, control_scale=True)

    # Define a soft color scale (blue shades)
    colormap = cm.linear.Blues_09.scale(0, 1)  # Soft blue gradient

    # Add Voronoi polygons with smooth styling
    folium.GeoJson(
        st.session_state.voronoi_data,
        name="Voronoi Polygons",
        style_function=lambda feature: {
            "fillColor": colormap(0.5),  # Soft blue color for all cells
            "color": "black",  # Thin black borders
            "weight": 1.5,  # Slightly thicker lines for clarity
            "fillOpacity": 0.4  # Soft transparency for better map visibility
        }
    ).add_to(m)

    # Add amenity markers (optional for better visibility)
    for feature in st.session_state.voronoi_data["features"]:
        if feature["geometry"]["type"] == "Point":
            coords = feature["geometry"]["coordinates"]
            folium.Marker(
                location=[coords[1], coords[0]],
                popup=f"Amenity: {st.session_state.amenity}",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)

    # Display the styled map in Streamlit
    st_folium(m, use_container_width=True, height=1000, key="voronoi_map")