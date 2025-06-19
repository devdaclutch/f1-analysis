import fastf1
from fastf1.plotting import setup_mpl
import matplotlib.pyplot as plt

import os
os.makedirs('./f1_cache', exist_ok=True)
fastf1.Cache.enable_cache('./f1_cache')
setup_mpl()

session = fastf1.get_session(2020, 'Monaco', 'R')
session.load()

lap = session.laps.pick_driver('VER').pick_fastest()
car_data = lap.get_car_data().add_distance()

# Extract telemetry
distance = car_data['Distance']
speed = car_data['Speed']
throttle = car_data['Throttle']
brake = car_data['Brake']

# Plotting
fig, ax1 = plt.subplots()

# Speed plot (left y-axis)
ax1.plot(distance, speed, label='Speed (km/h)', color='blue')
ax1.set_xlabel('Distance (m)')
ax1.set_ylabel('Speed (km/h)', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Throttle and brake plot (right y-axis)
ax2 = ax1.twinx()
ax2.plot(distance, throttle, label='Throttle (%)', color='green', alpha=0.7)
ax2.plot(distance, brake * 100, label='Brake (%)', color='red', alpha=0.7)
ax2.set_ylabel('Throttle / Brake (%)')
ax2.set_ylim(0, 105)

# Title and legend
fig.suptitle('VER - 2023 Monaco Q - Speed, Throttle, Brake vs Distance')
fig.legend(loc='upper right')

plt.tight_layout()
plt.show()
