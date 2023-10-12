import streamlit as st
import pandas as pd
import plotly.express as px

# Load earthquake data
df = pd.read_csv("earthquake_data.csv")

# Remove NaN values from the 'continent' column
df = df.dropna(subset=['continent'])

# Extract year from 'date_time'
df['year'] = pd.to_datetime(df['date_time']).dt.year

# Introductory page content
st.title("Earthquakes")
st.write("Earthquakes are natural disasters caused by the sudden release of energy in the Earth's crust, resulting in seismic waves. Their devastating impact can lead to loss of lives, property damage, and tsunamis.")

st.header("MSBA 325")
st.subheader("Nicolas Araman")

# Introduction to the Dataset Columns
st.write("## Dataset Columns Description")
st.write("Here's a description of each column in the earthquake dataset:")

column_descriptions = {
    'magnitude': "Magnitude measures the energy released by an earthquake on the Richter scale.",
    'date_time': "The date and time when the earthquake occurred.",
    'cdi': "The Community Determined Intensity (CDI) value, representing the intensity of shaking experienced by the community.",
    'mmi': "The Modified Mercalli Intensity (MMI) value, providing a measure of shaking intensity and its effects.",
    'alert': "An alert level indicating the severity of the earthquake (e.g., 'green,' 'yellow,' 'orange,' 'red').",
    'tsunami': "Indicates whether the earthquake generated a tsunami (1 for yes, 0 for no).",
    'sig': "The significance of the earthquake event.",
    'net': "The seismic network or agency that reported the earthquake.",
    'nst': "The number of reporting seismic stations.",
    'dmin': "The minimum distance to the earthquake in degrees.",
    'gap': "The azimuthal gap, representing the gap in coverage between seismic stations for the earthquake event.",
    'magType': "The type of magnitude scale used to measure the earthquake (e.g., 'mb' for body-wave magnitude).",
    'depth': "The depth at which the earthquake occurred in kilometers below the Earth's surface.",
    'latitude': "The latitude coordinate of the earthquake's epicenter.",
    'longitude': "The longitude coordinate of the earthquake's epicenter.",
    'location': "A description of the earthquake's location or region.",
    'continent': "The continent on which the earthquake occurred.",
    'country': "The country where the earthquake's epicenter is located."
}

# Display column descriptions
for column, description in column_descriptions.items():
    st.write(f"- **{column.capitalize()}:** {description}")

# Sidebar for filtering
st.sidebar.write("## Filters")

# Dropdown menus for other options
dropdowns = ['alert', 'tsunami', 'net', 'magType']
selected_options = {}
for dropdown in dropdowns:
    options = ['All'] + df[dropdown].unique().tolist()
    selected_option = st.sidebar.selectbox(f"Select {dropdown.capitalize()}", options)
    selected_options[dropdown] = selected_option

# Dropdown to select continent
selected_continent_options = ['All'] + df['continent'].unique().tolist()
selected_continent = st.sidebar.selectbox("Select a Continent", selected_continent_options)

# Slide ranges for magnitude, depth, dmin, gap, sig
magnitude_range = st.sidebar.slider("Select Magnitude Range", float(df['magnitude'].min()), float(df['magnitude'].max()), (float(df['magnitude'].min()), float(df['magnitude'].max())))
depth_range = st.sidebar.slider("Select Depth Range", float(df['depth'].min()), float(df['depth'].max()), (float(df['depth'].min()), float(df['depth'].max())))
dmin_range = st.sidebar.slider("Select Dmin Range", float(df['dmin'].min()), float(df['dmin'].max()), (float(df['dmin'].min()), float(df['dmin'].max())))
gap_range = st.sidebar.slider("Select Gap Range", float(df['gap'].min()), float(df['gap'].max()), (float(df['gap'].min()), float(df['gap'].max())))
sig_range = st.sidebar.slider("Select Sig Range", float(df['sig'].min()), float(df['sig'].max()), (float(df['sig'].min()), float(df['sig'].max())))

# For Nst Range, ensure it starts with the minimum value
nst_min = int(df['nst'].min())
nst_max = int(df['nst'].max())
nst_range = st.sidebar.slider("Select Nst Range", nst_min, nst_max, (nst_min, nst_max))

# For Year Range, ensure it starts with the minimum value
year_min = int(df['year'].min())
year_max = int(df['year'].max())
year_range = st.sidebar.slider("Select Year Range", year_min, year_max, (year_min, year_max))

# Filter data based on user selections
filtered_df = df[(df['magnitude'] >= magnitude_range[0]) & (df['magnitude'] <= magnitude_range[1]) &
                 (df['depth'] >= depth_range[0]) & (df['depth'] <= depth_range[1]) &
                 (df['dmin'] >= dmin_range[0]) & (df['dmin'] <= dmin_range[1]) &
                 (df['gap'] >= gap_range[0]) & (df['gap'] <= gap_range[1]) &
                 (df['sig'] >= sig_range[0]) & (df['sig'] <= sig_range[1]) &
                 (df['nst'] >= nst_range[0]) & (df['nst'] <= nst_range[1]) &
                 (df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

for dropdown in dropdowns:
    if selected_options[dropdown] != 'All':
        filtered_df = filtered_df[filtered_df[dropdown] == selected_options[dropdown]]

# Filter data based on selected continent
filtered_df = filtered_df[df['continent'] == selected_continent] if selected_continent != 'All' else filtered_df

# Display earthquakes on a map with a time slider
st.write("## Interactive Map with Time Slider")
st.write("This map visualizes the global distribution of earthquakes over time. By playing the time slider, users can observe the chronology of seismic events and identify patterns or trends over the years.")
fig_map_time = px.scatter_geo(filtered_df, lat='latitude', lon='longitude', color='magnitude',
                              animation_frame='year', projection="natural earth",
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
st.write("This scatter plot allows users to compare two metrics of their choice, such as magnitude vs depth. By analyzing the relationship between these metrics, one can derive insights into the nature and impact of different earthquakes.")
x_axis = st.selectbox("Select X-axis metric", ['magnitude', 'gap'])
y_axis = st.selectbox("Select Y-axis metric", ['depth', 'nst'])
fig_scatter = px.scatter(filtered_df, x=x_axis, y=y_axis, color='magnitude', hover_name='location',
                         title=f'Scatter Plot of Earthquake Data ({x_axis} vs {y_axis})')
st.plotly_chart(fig_scatter)

# Third interactive visualization using user input
st.write("## Interactive Magnitude Distribution")
st.write(f"This histogram showcases the distribution of earthquake magnitudes for the selected continent. It provides insights into the frequency of different magnitude earthquakes, helping in understanding the seismic activity in a region.")
fig_histogram = px.histogram(filtered_df, x='magnitude', nbins=20, title=f'Magnitude Distribution in {selected_continent}')
st.plotly_chart(fig_histogram)
