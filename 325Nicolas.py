import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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

# Sidebar for user options
st.sidebar.title("Visualization Options")

# Filter out NaN values from the continent column
valid_continents = df["continent"].dropna().unique()

# Allow the user to select a specific continent
selected_continent = st.sidebar.selectbox("Select a Continent", valid_continents)

# Filter the data based on the selected continent
filtered_df = df[df["continent"] == selected_continent]

# Plotting earthquake locations based on selected continent
st.write("## Earthquake Locations")
fig_map = px.scatter_geo(filtered_df, lat='latitude', lon='longitude', color='magnitude', hover_name='location',
                         title=f'Earthquake Locations in {selected_continent}')
st.plotly_chart(fig_map)

# Magnitude Distribution Over Time (Animated Histogram)
st.write("## Magnitude Distribution Over Time")
magnitude_min = st.sidebar.slider("Minimum Magnitude", min_value=min(df['magnitude']), max_value=max(df['magnitude']), value=min(df['magnitude']))
magnitude_max = st.sidebar.slider("Maximum Magnitude", min_value=min(df['magnitude']), max_value=max(df['magnitude']), value=max(df['magnitude']))

filtered_df_magnitude = df[(df['magnitude'] >= magnitude_min) & (df['magnitude'] <= magnitude_max)]
fig_histogram = px.histogram(filtered_df_magnitude, x='magnitude', nbins=30, title='Magnitude Distribution Over Time')
st.plotly_chart(fig_histogram)

# 3D Scatter Plot
st.write("## 3D Scatter Plot of Earthquake Data (Depth, Magnitude, Gap)")
depth_min = st.sidebar.slider("Minimum Depth", min_value=min(df['depth']), max_value=max(df['depth']), value=min(df['depth']))
depth_max = st.sidebar.slider("Maximum Depth", min_value=min(df['depth']), max_value=max(df['depth']), value=max(df['depth']))

filtered_df_depth = df[(df['depth'] >= depth_min) & (df['depth'] <= depth_max)]
fig_3d_scatter = px.scatter_3d(filtered_df_depth, x='depth', y='magnitude', z='gap', color='country',
                                size='nst', opacity=0.7, hover_name='title',
                                labels={'depth': 'Depth', 'magnitude': 'Magnitude', 'gap': 'Gap',
                                        'country': 'Country', 'nst': 'NST'},
                                title='3D Scatter Plot of Earthquake Data (Depth, Magnitude, Gap)')
st.plotly_chart(fig_3d_scatter)

# Earthquake Density Contours by Magnitude
st.write("## Earthquake Density Contours by Magnitude")
fig_density_contour = px.density_contour(filtered_df, x='longitude', y='latitude', color='magnitude',
                                        marginal_x='histogram', marginal_y='histogram',
                                        labels={'longitude': 'Longitude', 'latitude': 'Latitude', 'magnitude': 'Magnitude'},
                                        title='Earthquake Density Contours by Magnitude')
st.plotly_chart(fig_density_contour)

# Cumulative Earthquake Count Over Time (Animated Line Chart)
st.write("## Cumulative Earthquake Count Over Time")
df['date_time'] = pd.to_datetime(df['date_time'])
df.sort_values(by='date_time', inplace=True)
df['cumulative_count'] = range(1, len(df) + 1)

fig_cumulative_count = go.Figure(
    data=[
        go.Scatter(
            x=df['date_time'],
            y=df['cumulative_count'],
            mode='lines+markers',
            line=dict(color='blue', width=2),
            marker=dict(size=6, color='red'),
            name='Cumulative Count'
        ),
    ],
    layout=go.Layout(
        title='Cumulative Earthquake Count Over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Cumulative Count'),
    ),
)

st.plotly_chart(fig_cumulative_count)
