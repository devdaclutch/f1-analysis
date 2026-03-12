import fastf1
import streamlit as st
import os
import numpy as np
import plotly.graph_objects as go

# Setup
os.makedirs('./f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('./f1_cache')

st.set_page_config(layout="wide")
st.title("F1 Driver Comparison Tool")

# Sidebar inputs
year = st.sidebar.selectbox("Select Year", list(range(2025, 2018, -1)))

@st.cache_data(show_spinner="Loading schedule...")
def get_schedule(year):
    schedule = fastf1.get_event_schedule(year)
    return schedule[schedule['EventFormat'] != 'testing']['EventName'].tolist()

tracks = get_schedule(year)
track = st.sidebar.selectbox("Select Grand Prix", tracks)
session_type = st.sidebar.selectbox("Select Session", ["Q", "R", "FP1", "FP2", "FP3"])

# Cached session loader
@st.cache_resource(show_spinner="Loading session...")
def load_session(year, event_name, session_type):
    event = fastf1.get_event(year, event_name)
    session = event.get_session(session_type)
    session.load()
    return session

try:
    session = load_session(year, track, session_type)
except ValueError as e:
    st.error(f"Failed to load session: {e}")
    st.stop()

# Driver options
drivers = sorted(session.laps['Driver'].unique())
driver1 = st.sidebar.selectbox("Driver 1", drivers, index=0)
driver2 = st.sidebar.selectbox("Driver 2", drivers, index=1)

# Get fastest laps
lap1 = session.laps.pick_drivers(driver1).pick_fastest()
lap2 = session.laps.pick_drivers(driver2).pick_fastest()

lap1_time = lap1['LapTime']
lap2_time = lap2['LapTime']

st.sidebar.markdown(f"**{driver1} Fastest Lap:** {lap1_time}")
st.sidebar.markdown(f"**{driver2} Fastest Lap:** {lap2_time}")

# Get speed telemetry for speed trace
tel1 = lap1.get_car_data().add_distance()
tel2 = lap2.get_car_data().add_distance()

# Interpolate for speed trace
common_distance = np.linspace(0, min(tel1['Distance'].max(), tel2['Distance'].max()), 500)
tel1_interp = tel1.set_index('Distance').reindex(common_distance, method='nearest').interpolate()
tel2_interp = tel2.set_index('Distance').reindex(common_distance, method='nearest').interpolate()

speed1 = tel1_interp['Speed']
speed2 = tel2_interp['Speed']

# Get full positional telemetry for track map
tel1_pos = lap1.get_telemetry().add_distance()
tel2_pos = lap2.get_telemetry().add_distance()

common_distance_map = np.linspace(0, min(tel1_pos['Distance'].max(), tel2_pos['Distance'].max()), 1000)
tel1_map = tel1_pos.set_index('Distance').reindex(common_distance_map, method='nearest').interpolate()
tel2_map = tel2_pos.set_index('Distance').reindex(common_distance_map, method='nearest').interpolate()

speed_delta = (tel1_map['Speed'] - tel2_map['Speed']).to_numpy()
x = tel1_map['X'].values
y = tel1_map['Y'].values

# Build two traces: one for driver1-faster segments, one for driver2-faster
d1_x, d1_y = [], []
d2_x, d2_y = [], []

for i in range(len(x) - 1):
    if speed_delta[i] > 0:
        d1_x.extend([x[i], x[i+1], None])
        d1_y.extend([y[i], y[i+1], None])
    else:
        d2_x.extend([x[i], x[i+1], None])
        d2_y.extend([y[i], y[i+1], None])

fig_map = go.Figure()

fig_map.add_trace(go.Scatter(
    x=d1_x, y=d1_y, mode='lines',
    line=dict(color='blue', width=5),
    hoverinfo='text', text=f"{driver1} faster",
    name=driver1
))
fig_map.add_trace(go.Scatter(
    x=d2_x, y=d2_y, mode='lines',
    line=dict(color='orange', width=5),
    hoverinfo='text', text=f"{driver2} faster",
    name=driver2
))

# Add sector lines and labels
track_len = tel1_map.index.max()
sector_markers = [track_len/3, 2*track_len/3]
sector_points = [tel1_map.iloc[(np.abs(tel1_map.index.to_numpy() - d)).argmin()] for d in sector_markers]


for i, point in enumerate(sector_points):
    x_s = point['X']
    y_s = point['Y']
    fig_map.add_trace(go.Scatter(
        x=[x_s], y=[y_s],
        mode='text',
        text=[f"Sector {i+2}"],
        textposition='top center',
        showlegend=False
    ))


fig_map.update_layout(
    title="Track Dominance Map (Broadcast Style)",
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False, scaleanchor="x", scaleratio=1),
    height=700,
    plot_bgcolor='white'
)

# Create speed trace
fig_speed = go.Figure()
fig_speed.add_trace(go.Scatter(x=common_distance, y=speed1, name=f"{driver1} ({lap1_time})", line=dict(color='blue')))
fig_speed.add_trace(go.Scatter(x=common_distance, y=speed2, name=f"{driver2} ({lap2_time})", line=dict(color='orange')))
fig_speed.update_layout(title="Speed Trace", xaxis_title="Distance (m)", yaxis_title="Speed (km/h)", height=400)

# Show both plots
st.plotly_chart(fig_speed, use_container_width=True)
st.plotly_chart(fig_map, use_container_width=True)
