import fastf1
from fastf1.plotting import setup_mpl
import matplotlib.pyplot as plt
import argparse
import os

# --- Setup ---
os.makedirs('./f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('./f1_cache')
setup_mpl()

# --- Argument parser ---
parser = argparse.ArgumentParser(description="Compare F1 drivers' fastest laps")
parser.add_argument('--year', type=int, required=True)
parser.add_argument('--track', type=str, required=True)
parser.add_argument('--session', type=str, default='Q')
parser.add_argument('--driver1', type=str, required=True)
parser.add_argument('--driver2', type=str, required=True)
args = parser.parse_args()

# --- Load session ---
session = fastf1.get_session(args.year, args.track, args.session.upper())
session.load()

# --- Get laps ---
lap1 = session.laps.pick_driver(args.driver1.upper()).pick_fastest()
lap2 = session.laps.pick_driver(args.driver2.upper()).pick_fastest()

# --- Get telemetry with distance ---
tel1 = lap1.get_car_data().add_distance()
tel2 = lap2.get_car_data().add_distance()

# --- Interpolate both to 1m resolution for comparison ---
import numpy as np
common_distance = np.linspace(0, min(tel1['Distance'].max(), tel2['Distance'].max()), 500)

tel1_interp = tel1.set_index('Distance').reindex(common_distance, method='nearest').interpolate()
tel2_interp = tel2.set_index('Distance').reindex(common_distance, method='nearest').interpolate()

# --- Extract speed ---
speed1 = tel1_interp['Speed']
speed2 = tel2_interp['Speed']

# --- Delta computation ---
# Convert speeds from km/h to m/s
speed1_ms = speed1 / 3.6
speed2_ms = speed2 / 3.6

# Distance step for each sample (in meters)
dist_step = np.gradient(common_distance)

# Cumulative time delta in seconds (positive means driver2 is faster)
delta = np.cumsum(dist_step * (1 / speed1_ms - 1 / speed2_ms))

# --- Plot ---
fig, axs = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

axs[0].plot(common_distance, speed1, label=args.driver1.upper())
axs[0].plot(common_distance, speed2, label=args.driver2.upper())
axs[0].set_ylabel('Speed (km/h)')
axs[0].legend()
axs[0].grid(True)
axs[0].set_title(f'Speed Trace - {args.driver1.upper()} vs {args.driver2.upper()} - {args.track} {args.year} {args.session.upper()}')

axs[1].plot(common_distance, delta, color='purple')
axs[1].set_ylabel(f"Delta Time ({args.driver2.upper()} - {args.driver1.upper()}) [s]")
axs[1].set_xlabel('Distance (m)')
axs[1].axhline(0, color='gray', linestyle='--')
axs[1].grid(True)
axs[1].set_title('Cumulative Time Delta')

plt.tight_layout()
plt.show()
