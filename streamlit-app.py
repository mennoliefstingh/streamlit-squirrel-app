import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pydeck as pdk
import numpy as np

data = pd.read_csv("data/2018_Central_Park_Squirrel_Census.csv")
data = data.rename(columns={"X": "lon", "Y": "lat"})
data = data.fillna("None")

st.title("Squirrels! 🐿")
st.image("data/central_park.jpg")
st.markdown(
    """As part of the [Squirrel Census](https://www.thesquirrelcensus.com/) in 2018, volunteers counted all squirrels in Central Park and
     recorded features like their color, where they were sighted and whether they were doing anything 
     interesting at that time. Strangely, this was the first time anyone had ever attempted anything like this. 
     The results? Central Park is the home of 3023 squirrels, most of which are gray! A few of them must be 
     especially fast, since the Census volunteers weren't even able to see what color they were 🐿💨"""
)
custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)
sns.color_palette("Set2")
fig, ax = plt.subplots(figsize=(10, 5))


ax = sns.countplot(data["Primary Fur Color"])
st.pyplot(fig)


st.markdown(
    f"""The Squirrel Census website mentions a number of 2373 squirrels in Central Park, but our 
most recent data suggests a much larger number of {len(data)}. Does this mean that Central Park squirrels 
are doing well? """
)
col1, col2, col3 = st.columns(3)
col1.metric("Number of recorded squirrels", len(data), len(data) - 2373)
col2.metric(
    "Squirrels per hectare",
    round(len(data) / 350, 2),
    round((len(data) - 2373) / 350, 2),
)
col3.metric("Number of primary colors", 3)

st.markdown(
    """Apart from _counting the number of squirrels_, 
the volunteers also recorded their location and gave them all a unique name. 
What's your favorite squirrel name? Mine is definitely **18C-PM-1018-02**, so cute 🥰.

Check out the full data below: hover over each point to reveal the squirrels name and what
he (or she) was doing when they were spotted. You can also use the selection box to focus on specific
fur colors. 

Can you find the two squirrels that were chasing
each other through the trees? I wonder what those little rodents were in such a big fight about.  """
)

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

st.markdown(
    """If you haven't seen enough squirrels yet, have a look at the 
    [data](https://data.cityofnewyork.us/Environment/2018-Central-Park-Squirrel-Census-Squirrel-Data/vfnx-vebw)
yourself or check out Mark Rober's video below to learn more about these surprisingly cool critters!"""
)

st.video("https://www.youtube.com/watch?v=hFZFjoX2cGg")
