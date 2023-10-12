import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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
nst_min = int(df['nst'].min())
nst_max = int(df['nst'].max())
nst_range = st.sidebar.slider("Select Nst Range", nst_min, nst_max, (nst_min, nst_max))
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

# Interactive Map with Time Slider
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

# Interactive Visualization with Dropdowns
st.write("## Interactive Visualization with Dropdowns")
st.write("This scatter plot allows users to interactively select and compare two metrics of their choice, such as magnitude versus depth. By analyzing the relationship between these metrics, one can derive insights into the nature and impact of different earthquakes.")
x_axis = st.selectbox("Select X-axis metric", ['magnitude', 'gap'])
y_axis = st.selectbox("Select Y-axis metric", ['depth', 'nst'])
fig_scatter = px.scatter(filtered_df, x=x_axis, y=y_axis, color='magnitude', hover_name='location',
                         title=f'Scatter Plot of Earthquake Data ({x_axis} vs {y_axis})')
st.plotly_chart(fig_scatter)

# Magnitude Distribution histogram
st.write("## Interactive Magnitude Distribution")
st.write(f"This histogram showcases the distribution of earthquake magnitudes for the selected continent. It provides insights into the frequency of different magnitude earthquakes, helping in understanding the seismic activity in a region.")
fig_histogram = px.histogram(filtered_df, x='magnitude', nbins=20, title=f'Magnitude Distribution in {selected_continent}')
st.plotly_chart(fig_histogram)

# 3D scatter plot for magnitude, depth, and significance
st.write("## 3D Visualization of Earthquake Data")
st.write("This 3D scatter plot offers a multi-dimensional view of earthquakes based on their magnitude, depth, and significance. The color indicates the alert level, and the size represents the number of reporting stations. By selecting different years, users can explore the earthquake characteristics over time and understand the distribution and intensity of seismic events.")

def create_3d_scatter(year):
    year_filtered_df = filtered_df[filtered_df['year'] == year]
    
    # Setting color scale based on alert level
    color_scale = {
        'green': 'green',
        'yellow': 'yellow',
        'orange': 'orange',
        'red': 'red'
    }
    colors = year_filtered_df['alert'].map(color_scale)
    
    # Plotting the 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=year_filtered_df['magnitude'],
        y=year_filtered_df['depth'],
        z=year_filtered_df['sig'],
        mode='markers',
        marker=dict(
            size=year_filtered_df['nst'] / 10,  # scaling size for better visualization
            color=colors,
            opacity=0.8,
            colorscale='Viridis',
            sizemode='diameter'
        ),
        text=year_filtered_df['location']
    )])

    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis_title='Magnitude',
            yaxis_title='Depth',
            zaxis_title='Significance'
        ),
        title=f"3D Visualization of Earthquakes for {year}"
    )
    return fig

selected_year = st.slider("Select a Year for 3D Visualization", year_min, year_max, year_max)
fig_3d = create_3d_scatter(selected_year)
st.plotly_chart(fig_3d)
