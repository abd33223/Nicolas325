import streamlit as st
import pandas as pd
import plotly.express as px

# Load earthquake data
df = pd.read_csv("earthquake_data.csv")

# Remove NaN values from the 'continent' column
df = df.dropna(subset=['continent'])

# Introductory page content
st.title("Earthquakes")
st.header("MSBA 325")
st.subheader("Nicolas Araman")

# Sidebar for filtering
st.sidebar.write("## Filters")

# Slide ranges for magnitude and depth
magnitude_range = st.sidebar.slider("Select Magnitude Range", float(df['magnitude'].min()), float(df['magnitude'].max()), (float(df['magnitude'].min()), float(df['magnitude'].max())))
depth_range = st.sidebar.slider("Select Depth Range", float(df['depth'].min()), float(df['depth'].max()), (float(df['depth'].min()), float(df['depth'].max())))

# Dropdown menus
dropdowns = ['alert', 'tsunami', 'sig', 'net', 'nst', 'dmin', 'gap', 'magType', 'depth']
selected_options = {}
for dropdown in dropdowns:
    options = df[dropdown].unique().tolist()
    options.append('All')
    selected_option = st.sidebar.selectbox(f"Select {dropdown.capitalize()}", options)
    selected_options[dropdown] = selected_option

# Filter data based on user selections
filtered_df = df[(df['magnitude'] >= magnitude_range[0]) & (df['magnitude'] <= magnitude_range[1]) &
                 (df['depth'] >= depth_range[0]) & (df['depth'] <= depth_range[1])]

for dropdown in dropdowns:
    if selected_options[dropdown] != 'All':
        filtered_df = filtered_df[filtered_df[dropdown] == selected_options[dropdown]]

# Debugging: Print filtered DataFrame info and unique values for important columns
st.write("Filtered DataFrame Info:")
st.write(filtered_df.info())
st.write("Unique values for latitude, longitude, and year:")
st.write(filtered_df['latitude'].unique())
st.write(filtered_df['longitude'].unique())
st.write(filtered_df['year'].unique())

# Convert the 'date_time' column to datetime and extract years
df['date_time'] = pd.to_datetime(df['date_time'])
df['year'] = df['date_time'].dt.year

# Display earthquakes on a map with a time slider
st.write("## Interactive Map with Time Slider")
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

# Dropdowns to select X and Y axes for scatter plot
x_axis = st.selectbox("Select X-axis metric", ['magnitude', 'depth', 'gap'])
y_axis = st.selectbox("Select Y-axis metric", ['depth', 'magnitude', 'gap'])

# Create scatter plot based on user-selected metrics
fig_scatter = px.scatter(filtered_df, x=x_axis, y=y_axis, color='magnitude', hover_name='location',
                         title=f'Scatter Plot of Earthquake Data ({x_axis} vs {y_axis})')
st.plotly_chart(fig_scatter)

# Third interactive visualization using user input
st.write("## Interactive Magnitude Distribution")

# Dropdown to select continent
selected_continent = st.selectbox("Select a Continent", ['All'] + df['continent'].unique().tolist())

# Filter data based on selected continent
filtered_df = df[df['continent'] == selected_continent] if selected_continent != 'All' else df

# Create histogram of earthquake magnitudes for the selected continent
fig_histogram = px.histogram(filtered_df, x='magnitude', nbins=20, title=f'Magnitude Distribution in {selected_continent}')
st.plotly_chart(fig_histogram)
