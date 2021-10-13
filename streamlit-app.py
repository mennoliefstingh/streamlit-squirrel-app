import streamlit as st
import pandas as pd
import seaborn as sns
import pydeck as pdk
import numpy as np

data = pd.read_csv("https://data.cityofnewyork.us/api/views/vfnx-vebw/rows.csv")
data = data.rename(columns={"X": "lon", "Y": "lat"})
data = data.fillna("None")
print(data["Primary Fur Color"].value_counts())

st.title("Squirrels! 🐿")

# st.write(data)

# st.text("Hello world :)")

map_args = {
    "pickable": True,
    "opacity": 1,
    "stroked": False,
    "filled": True,
    "radius_scale": 3,
    "radius_min_pixels": 2,
    "radius_max_pixels": 100,
    "get_position": ["lon", "lat"],
    "get_radius": 1,
}


def squirrel_layer(data, color):
    return pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_fill_color=color,
        pickable=True,
        opacity=1,
        stroked=False,
        filled=True,
        radius_scale=3,
        radius_min_pixels=2,
        radius_max_pixels=100,
        get_position=["lon", "lat"],
        get_radius=1,
    )


gray_layer = squirrel_layer(
    data.loc[data["Primary Fur Color"] == "Gray"], [130, 130, 130]
)
cinnamon_layer = squirrel_layer(
    data.loc[data["Primary Fur Color"] == "Cinnamon"], [107, 34, 35]
)
black_layer = squirrel_layer(data.loc[data["Primary Fur Color"] == "Black"], [0, 0, 0])

map = pdk.Deck(
    map_style="road",
    initial_view_state={
        "latitude": np.average(data["lat"]),
        "longitude": np.average(data["lon"]),
        "zoom": 13,
        "pitch": 0,
    },
    layers=[gray_layer, cinnamon_layer, black_layer],
    tooltip={
        "text": "Squirrel ID: {Unique Squirrel ID}\n Specific location:{Specific Location}\n Other activities:{Other Activities}"
    },
)

st.components.v1.html(map.to_html(as_string=True), height=500)
