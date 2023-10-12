import streamlit as st
import pandas as pd
import plotly.express as px

# Load earthquake data with caching to speed up subsequent data loads
@st.cache
def load_data():
    return pd.read_csv("earthquake_data.csv")

df = load_data()

# Remove NaN values from the 'continent' column
df = df.dropna(subset=['continent'])

# Extract year from 'date_time'
df['year'] = pd.to_datetime(df['date_time']).dt.year

# Introductory page content
st.title("Earthquakes")
st.write("Earthquakes are natural disasters caused by the sudden release of energy in the Earth's crust, resulting in seismic waves. Their devastating impact can lead to loss of lives, property damage, and tsunamis.")
st.header("MSBA 325")
st.subheader("Nicolas Araman")

# Sidebar for filtering
st.sidebar.write("## Filters")

st.sidebar.write("### General Filters")
# Dropdown menus for other options
dropdowns = ['alert', 'tsunami', 'net', 'magType']
selected_options = {}
for dropdown in dropdowns:
    options = ['All'] + sorted(df[dropdown].unique().tolist())
    selected_option = st.sidebar.selectbox(f"Select {dropdown.capitalize()}", options)
    selected_options[dropdown] = None if selected_option == 'All' else selected_option

# Dropdown to select continent
st.sidebar.write("### Geographic Filter")
selected_continent_options = ['All'] + sorted(df['continent'].unique().tolist())
selected_continent = st.sidebar.selectbox("Select a Continent", selected_continent_options)

st.sidebar.write("### Numeric Filters")
# Slide ranges for magnitude, depth, dmin, gap, sig
magnitude_range = st.sidebar.slider("Magnitude (strength of the earthquake)", float(df['magnitude'].min()), float(df['magnitude'].max()), (float(df['magnitude'].min()), float(df['magnitude'].max())))
depth_range = st.sidebar.slider("Depth (depth of the earthquake below the surface)", float(df['depth'].min()), float(df['depth'].max()), (float(df['depth'].min()), float(df['depth'].max())))
dmin_range = st.sidebar.slider("Dmin (horizontal distance from the epicenter to the nearest station)", float(df['dmin'].min()), float(df['dmin'].max()), (float(df['dmin'].min()), float(df['dmin'].max())))
gap_range = st.sidebar.slider("Gap (largest angular distance between station azimuths)", float(df['gap'].min()), float(df['gap'].max()), (float(df['gap'].min()), float(df['gap'].max())))
sig_range = st.sidebar.slider("Sig (significance of the earthquake)", float(df['sig'].min()), float(df['sig'].max()), (float(df['sig'].min()), float(df['sig'].max())))
nst_min = int(df['nst'].min())
nst_max = int(df['nst'].max())
nst_range = st.sidebar.slider("Nst (number of reporting stations)", nst_min, nst_max, (nst_min, nst_max))
year_min = int(df['year'].min())
year_max = int(df['year'].max())
year_range = st.sidebar.slider("Year (year of the earthquake)", year_min, year_max, (year_min, year_max))

# Filtering process
filtered_df = df.copy()
for dropdown in dropdowns:
    if selected_options[dropdown]:
        filtered_df = filtered_df[filtered_df[dropdown] == selected_options[dropdown]]

filtered_df = filtered_df[
    (filtered_df['magnitude'] >= magnitude_range[0]) & (filtered_df['magnitude'] <= magnitude_range[1]) &
    (filtered_df['depth'] >= depth_range[0]) & (filtered_df['depth'] <= depth_range[1]) &
    (filtered_df['dmin'] >= dmin_range[0]) & (filtered_df['dmin'] <= dmin_range[1]) &
    (filtered_df['gap'] >= gap_range[0]) & (filtered_df['gap'] <= gap_range[1]) &
    (filtered_df['sig'] >= sig_range[0]) & (filtered_df['sig'] <= sig_range[1]) &
    (filtered_df['nst'] >= nst_range[0]) & (filtered_df['nst'] <= nst_range[1]) &
    (filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])
]

if selected_continent != 'All':
    filtered_df = filtered_df[filtered_df['continent'] == selected_continent]

# Display earthquakes on a map with a time slider
st.write("## Interactive Map with Time Slider")
st.write("This map visualizes the global distribution of earthquakes over time. The color intensity signifies the magnitude of the earthquake. By playing the time slider, users can observe the chronology of seismic events and identify patterns or trends over the years.")
fig_map_time = px.scatter_geo(filtered_df, lat='latitude', lon='longitude', color='magnitude',
                              animation_frame='year', projection="natural earth",
                              title='Earthquake Locations with Time', hover_data=['location', 'depth', 'magnitude'])
fig_map_time.update_layout(updatemenus=[dict(type='buttons', showactive=False,
                                              buttons=[dict(label='Play',
                                                             method='animate',
                                                             args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True, mode='immediate')]),
                                                       dict(label='Pause',
                                                             method='animate',
                                                             args=[[None], dict(mode='immediate')])])])
st.plotly_chart(fig_map_time)

# Interactive Visualization with Dropdowns
st.write("## Interactive Visualization with Dropdowns")
st.write("This scatter plot allows users to compare two metrics of their choice, such as magnitude vs depth. The color represents the magnitude of the earthquake, providing an additional layer of information. By analyzing the relationship between these metrics, one can derive insights into the nature and impact of different earthquakes.")
x_axis = st.selectbox("Select X-axis metric", ['magnitude', 'gap'])
y_axis = st.selectbox("Select Y-axis metric", ['depth', 'nst'])
fig_scatter = px.scatter(filtered_df, x=x_axis, y=y_axis, color='magnitude', hover_name='location',
                         title=f'Scatter Plot of Earthquake Data ({x_axis} vs {y_axis})', hover_data=['alert', 'magnitude', 'depth'])
st.plotly_chart(fig_scatter)

# Magnitude Distribution histogram
st.write("## Interactive Magnitude Distribution")
st.write(f"This histogram showcases the distribution of earthquake magnitudes for the selected continent. It provides insights into the frequency of different magnitude earthquakes, aiding in understanding the seismic activity in a region.")
fig_histogram = px.histogram(filtered_df, x='magnitude', nbins=20, title=f'Magnitude Distribution in {selected_continent}', hover_data=['location'])
st.plotly_chart(fig_histogram)

# Display some basic statistics about the filtered data
avg_magnitude = filtered_df['magnitude'].mean()
deepest_eq = filtered_df['depth'].max()
number_of_eq = filtered_df.shape[0]
st.write(f"**Average Magnitude:** {avg_magnitude:.2f}")
st.write(f"**Deepest Earthquake:** {deepest_eq} km")
st.write(f"**Number of Earthquakes in Selected Range:** {number_of_eq}")
