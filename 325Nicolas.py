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

# Interactive visualization using dropdowns
st.write("## Interactive Visualization with Dropdowns")

# Dropdowns to select X and Y axes for scatter plot
x_axis = st.selectbox("Select X-axis metric", ['magnitude', 'depth', 'gap'])
y_axis = st.selectbox("Select Y-axis metric", ['depth', 'magnitude', 'gap'])

# Create scatter plot based on user-selected metrics
fig_scatter = px.scatter(df, x=x_axis, y=y_axis, color='magnitude', hover_name='location',
                         title=f'Scatter Plot of Earthquake Data ({x_axis} vs {y_axis})')
st.plotly_chart(fig_scatter)

# Third interactive visualization using user input
st.write("## Interactive Magnitude Distribution")

# Binning for magnitude distribution
num_bins = st.slider("Select the number of bins", min_value=5, max_value=50, value=20)

# Create histogram of earthquake magnitudes
fig_histogram = px.histogram(df, x='magnitude', nbins=num_bins, title='Magnitude Distribution')
st.plotly_chart(fig_histogram)
