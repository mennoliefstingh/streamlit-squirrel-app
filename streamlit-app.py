import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np

data = pd.read_csv("https://data.cityofnewyork.us/api/views/vfnx-vebw/rows.csv")
data = data.rename(columns={"X": "lon", "Y": "lat"})
data = data.fillna("None")

st.title("Squirrels! 🐿")
st.markdown(
    "This app showcases a couple functionalities of Streamlit. One very useful widget incorporated in Streamlit "
)
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
sns.color_palette("Set2")
fig, ax = plt.subplots(figsize=(10, 5))

st.markdown("You can also implement nice 'metric' widgets like these: ")
col1, col2, col3 = st.columns(3)
col1.metric("Number of squirrels", len(data), len(data) - 2800)
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")

ax = sns.countplot(data["Primary Fur Color"].dropna())
st.pyplot(fig)

# Function that constructs a PyDeck scatter layer to display squirrels
def squirrel_layer(data, color):
    return pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_fill_color=color,
        pickable=True,
        opacity=1,
        stroked=True,
        filled=True,
        radius_scale=3,
        radius_min_pixels=5,
        radius_max_pixels=100,
        get_position=["lon", "lat"],
        get_radius=1,
    )


# Define three different layers for the three different colors
map_layers = {
    "Gray": squirrel_layer(
        data.loc[data["Primary Fur Color"] == "Gray"], [130, 130, 130]
    ),
    "Cinnamon": squirrel_layer(
        data.loc[data["Primary Fur Color"] == "Cinnamon"], [97, 54, 19]
    ),
    "Black": squirrel_layer(data.loc[data["Primary Fur Color"] == "Black"], [0, 0, 0]),
}

layers = st.multiselect(
    "Fur colors to show on the map:",
    ["Gray", "Cinnamon", "Black"],
    ["Gray", "Cinnamon", "Black"],
)
# Replace the strings returned by the multiselectbox by the objects mapped in the dict
layers = [map_layers[color] for color in layers]

# Initialize a PyDeck map
map = pdk.Deck(
    map_style="road",
    initial_view_state={
        "latitude": np.average(data["lat"]),
        "longitude": np.average(data["lon"]),
        "zoom": 13,
        "pitch": 0,
    },
    layers=layers,
    tooltip={
        "text": "Squirrel ID: {Unique Squirrel ID}\n Specific location: {Specific Location}\n Other activities: {Other Activities}"
    },
)

# Render the map as html instead of using st.deck() to circumvent a few Pydeck rendering issues
st.components.v1.html(map.to_html(as_string=True), height=500)
