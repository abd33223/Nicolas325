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
st.header("MSBA 325")
st.subheader("Nicolas Araman")

# Sidebar for filtering
st.sidebar.write("## Filters")

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

# Dropdown menus for other options
dropdowns = ['alert', 'tsunami', 'net', 'magType']
selected_options = {}
for dropdown in dropdowns:
    options = ['All'] + df[dropdown].unique().tolist()
    selected_option = st.sidebar.selectbox(f"Select {dropdown.capitalize()}", options)
    selected_options[dropdown] = selected_option

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

# Display scatter plot based on user-selected metrics
st.write("## Scatter Plot")
x_axis = st.selectbox("Select X-axis metric", ['magnitude', 'gap'])
y_axis = st.selectbox("Select Y-axis metric", ['depth', 'nst'])

fig_scatter = px.scatter(filtered_df, x=x_axis, y=y_axis, color='magnitude', hover_name='location',
                         title=f'Scatter Plot of Earthquake Data ({x_axis} vs {y_axis})')
st.plotly_chart(fig_scatter)

# Display histogram of earthquake magnitudes
st.write("## Magnitude Distribution")
fig_histogram = px.histogram(filtered_df, x='magnitude', nbins=20, title='Magnitude Distribution')
st.plotly_chart(fig_histogram)

# Display sunburst chart showing distribution by continent and country
st.write("## Sunburst Chart")
fig_sunburst = px.sunburst(filtered_df, path=['continent', 'country'], title='Earthquake Distribution by Continent and Country')
st.plotly_chart(fig_sunburst)
