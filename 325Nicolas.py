import streamlit as st
import pandas as pd
import plotly.express as px

# Load earthquake data
df = pd.read_csv("earthquake_data.csv")

# Introductory page content
st.title("Earthquakes")
st.header("MSBA 325")
st.subheader("Nicolas Araman")

# Interactive map with time slider
st.write("## Interactive Map with Time Slider")

# Convert the 'date_time' column to datetime
df['date_time'] = pd.to_datetime(df['date_time'])

# Display earthquakes on a map with a time slider
fig_map_time = px.scatter_geo(df, lat='latitude', lon='longitude', color='magnitude',
                              animation_frame='date_time', projection="natural earth",
                              title='Earthquake Locations with Time')
st.plotly_chart(fig_map_time)

# Interactive game-like visualization
st.write("## Interactive Game-like Visualization")

# Generate a scatter plot with a hidden target point (representing the earthquake location)
target_location = (df['latitude'][0], df['longitude'][0])  # Using the first earthquake's location

# User input for guessing the earthquake location
user_guess_latitude = st.slider("Guess the Latitude", min_value=-90.0, max_value=90.0, step=0.1)
user_guess_longitude = st.slider("Guess the Longitude", min_value=-180.0, max_value=180.0, step=0.1)

# Plot the target point and the user's guess
fig_game = go.Figure()

fig_game.add_trace(go.Scattergeo(
    lat=[target_location[0]],
    lon=[target_location[1]],
    mode='markers',
    marker=dict(
        size=10,
        color='red',
        symbol='x'
    ),
    name='Actual Location'
))

fig_game.add_trace(go.Scattergeo(
    lat=[user_guess_latitude],
    lon=[user_guess_longitude],
    mode='markers',
    marker=dict(
        size=10,
        color='blue',
        symbol='circle'
    ),
    name='Your Guess'
))

fig_game.update_layout(
    geo=dict(
        projection_scale=2,
        center=dict(lat=0, lon=0),
        visible=False
    ),
    title="Earthquake Location Guessing Game"
)

# Provide feedback to the user based on the distance between the target and the guess
distance = ((user_guess_latitude - target_location[0]) ** 2 +
            (user_guess_longitude - target_location[1]) ** 2) ** 0.5

st.plotly_chart(fig_game)
st.write(f"Distance to target: {distance:.2f} degrees")
