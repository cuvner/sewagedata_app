import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import numpy as np

# Load the JSON data
with open("../data/js_map.json") as f:
    data = json.load(f)

# Extract relevant data
outflows = data["outflows"]

# Create a DataFrame
df = pd.DataFrame(outflows)

# Convert latitude and longitude to numeric values
df["lat"] = pd.to_numeric(df["lat"], errors='coerce')
df["lon"] = pd.to_numeric(df["lon"], errors='coerce')
df["spillCount"] = pd.to_numeric(df["spillCount"], errors='coerce').fillna(1)

# Normalize spillCount to a specific range for the cone sizes
min_size, max_size = 20, 40
df["scaled_spillCount"] = np.interp(df["spillCount"], (df["spillCount"].min(), df["spillCount"].max()), (min_size, max_size))

# Streamlit app
st.title("Outflows Locations 3D Scatter Plot with Cones")

st.write("This app visualizes the outflows locations with 3D cones based on the provided data.")

# Create 3D scatter plot with cones
fig = go.Figure()

# Add cones
fig.add_trace(go.Cone(
    x=df["lon"],
    y=df["lat"],
    z=[0]*len(df),  # Start all cones at z=0
    u=[0]*len(df),
    v=[0]*len(df),
    w=df["scaled_spillCount"],  # Use scaled spillCount to define cone heights
    colorscale='Viridis',
    sizemode="scaled",
    sizeref=0.1,
    anchor="tail",
    showscale=True,
    colorbar=dict(title="Spill Count")
))

# Set plot layout
fig.update_layout(
    scene=dict(
        xaxis_title='Longitude',
        yaxis_title='Latitude',
        zaxis_title='Height (Scaled Spill Count)',
        camera=dict(eye=dict(x=1.25, y=1.25, z=1.25))
    )
)

# Display the plot in Streamlit
st.plotly_chart(fig)
