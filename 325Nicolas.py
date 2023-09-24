import streamlit as st
import pandas as pd
import plotly.express as px

# Load earthquake data
df = pd.read_csv("earthquake_data.csv")

# Introductory page content
st.title("Earthquakes")
st.header("MSBA 325")
st.subheader("Nicolas Araman")

# Paragraph about high magnitude earthquakes
st.write(
    """
    High magnitude earthquakes can cause significant devastation, including widespread damage to buildings, 
    infrastructure, and loss of lives. The intensity and impact of these earthquakes highlight the urgent need 
    for preparedness, monitoring, and proactive measures to mitigate potential damage and save lives.
    """
)

# Interactive map with time slider
st.write("## Interactive Map with Time Slider")

# Convert the 'date_time' column to datetime and sort in increasing order
df['date_time'] = pd.to_datetime(df['date_time'])
df.sort_values(by='date_time', inplace=True)

# Display earthquakes on a map with a time slider
fig_map_time = px.scatter_geo(df, lat='latitude', lon='longitude', color='magnitude',
                              animation_frame='date_time', projection="natural earth",
                              title='Earthquake Locations with Time')
fig_map_time.update_layout(updatemenus=[dict(type='buttons', showactive=False,
                                              buttons=[dict(label='Play',
                                                             method='animate',
                                                             args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True, mode='immediate')]),
                                                       dict(label='Pause',
                                                             method='animate',
                                                             args=[[None], dict(mode='immediate')])])])
st.plotly_chart(fig_map_time)

# Interactive visualization using slider and dropdown
st.write("## Interactive Visualization with Slider and Dropdown")

# Dropdown to select earthquake
selected_earthquake = st.selectbox("Select an Earthquake", df['title'].unique())

# Check if the selected earthquake title exists
magnitude_slider_value = df[df['title'] == selected_earthquake]['magnitude'].values[0] if selected_earthquake in df['title'].values else 0

# Slider for magnitude
magnitude_slider = st.slider("Magnitude", min_value=0, max_value=10, value=magnitude_slider_value)

# Display selected earthquake details
st.write(f"Selected Earthquake: {selected_earthquake}")
st.write(f"Magnitude: {magnitude_slider}")
