import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load earthquake data
df = pd.read_csv("earthquake_data.csv")

# Plotting earthquake locations
st.write("Earthquake Locations")
fig_map = px.scatter_geo(df, lat='latitude', lon='longitude', color='magnitude', hover_name='location',
                         title='Earthquake Locations')
st.plotly_chart(fig_map)

# Magnitude Distribution Over Time (Animated Histogram)
st.write("Magnitude Distribution Over Time")
fig_histogram = px.histogram(df, x='magnitude', nbins=30, title='Magnitude Distribution Over Time')
st.plotly_chart(fig_histogram)

# 3D Scatter Plot
st.write("3D Scatter Plot of Earthquake Data (Depth, Magnitude, Gap)")
fig_3d_scatter = px.scatter_3d(df, x='depth', y='magnitude', z='gap', color='country',
                                size='nst', opacity=0.7, hover_name='title',
                                labels={'depth': 'Depth', 'magnitude': 'Magnitude', 'gap': 'Gap',
                                        'country': 'Country', 'nst': 'NST'},
                                title='3D Scatter Plot of Earthquake Data (Depth, Magnitude, Gap)')
st.plotly_chart(fig_3d_scatter)

# Earthquake Density Contours by Magnitude
st.write("Earthquake Density Contours by Magnitude")
fig_density_contour = px.density_contour(df, x='longitude', y='latitude', color='magnitude',
                                        marginal_x='histogram', marginal_y='histogram',
                                        labels={'longitude': 'Longitude', 'latitude': 'Latitude', 'magnitude': 'Magnitude'},
                                        title='Earthquake Density Contours by Magnitude')
st.plotly_chart(fig_density_contour)

# Cumulative Earthquake Count Over Time (Animated Line Chart)
st.write("Cumulative Earthquake Count Over Time")
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
