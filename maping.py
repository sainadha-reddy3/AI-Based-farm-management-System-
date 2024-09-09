import streamlit as st
from shapely.geometry import Polygon, shape
from geopy.distance import geodesic
from streamlit_folium import folium_static
import folium
from folium import plugins
import json
import base64
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('bg.jpg')
# App title
st.title("Field Mapping for Farmers")

# Sidebar
st.sidebar.title("Enter GPS Coordinates")
# Input GPS coordinates
latitude = st.sidebar.number_input('Enter latitude', -90.0, 90.0, 0.0)
longitude = st.sidebar.number_input('Enter longitude', -180.0, 180.0, 0.0)

# Create a map centered at the input coordinates
m = folium.Map(location=[latitude, longitude], zoom_start=13)

# Add drawing tool to the map
draw = plugins.Draw(export=True)
draw.add_to(m)

# Display the map in the Streamlit app
folium_static(m)

# File uploader for the GeoJSON file
st.sidebar.title("Upload GeoJSON")
uploaded_file = st.sidebar.file_uploader("Upload the GeoJSON file")

if uploaded_file is not None:
    # Load the GeoJSON file
    geojson_data = json.load(uploaded_file)
    i=0
    # Get the coordinates of the polygon
    for feature in geojson_data['features']:
        i+=1
        if feature['geometry']['type'] == 'Polygon':
            # Get the vertices
            vertices = feature['geometry']['coordinates'][0]
            vertices = [(lon, lat) for lon, lat in vertices]  # Flip coordinates

            # Calculate and display the area if there are enough vertices
            if len(vertices) >= 3:
                polygon = Polygon(vertices)
                area = polygon.area
                st.header(f"Area of the Feild{i}: \n{area} square units")

            # Calculate and display the distances between the vertices
            for i in range(len(vertices) - 1):
                distance = geodesic(vertices[i], vertices[i+1]).miles
                st.header("boundary distance")
                st.write(f"Distance between point {i+1} and point {i+2}: {distance} miles")
