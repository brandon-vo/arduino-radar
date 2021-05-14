import warnings

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import serial.tools.list_ports

matplotlib.use('TkAgg')

# Find Arduino port
arduinoPorts = [
    p.device
    for p in serial.tools.list_ports.comports()
    if 'Arduino' in p.description
]
if len(arduinoPorts) == 1:
    print("Arduino port found")
if len(arduinoPorts) > 1:
    warnings.warn(
        "There are multiple Arduinos identified. Using the first identified Arduino port")
if not arduinoPorts:
    raise IOError("No Arduino port found")

# Define Arduino data
arduinoData = serial.Serial(arduinoPorts[0])
arduinoData.flushInput()

# Set title and background
fig = plt.figure("Arduino Radar Scanner", facecolor='black')
fig.set_dpi(180)  # Set resolution of figure
fig.canvas.manager.window.wm_geometry("-340+75")  # Set Window position

# Add polar plot radar
ax = fig.add_subplot(111, polar=True, facecolor='#288526')

# Position of the radar
ax.set_position([-0.05, -0.05, 1.1, 1.1])

# Radar form
ax.set_ylim([0.0, 100])  # Default radar radius set to 100 cm
ax.set_xlim([0.0, np.pi])  # Create semi circle

# Display 7 angles for 0 to 180 degrees
ax.set_thetagrids(np.linspace(0.0, 180.0, 7))

# Styling
ax.tick_params(axis='both', colors='w')  # Set text colour
ax.grid(b=True, which='major', color='#75d950',
        linestyle='-', alpha=0.5)  # Set grid colour
points, = ax.plot([], linestyle='', marker='.', markerfacecolor='#f1fff1',
                  markeredgecolor='w', markersize=8.0)  # Set points style
line, = ax.plot([], color='#79f07b', linewidth=3.0)  # Set radar line style

# Variables
angles = np.arange(0, 181, 1)  # 0 to 180 degrees
theta = angles * (np.pi / 180.0)  # Angle to radians
distances = np.ones((len(angles),))  # Initial distances

fig.canvas.toolbar.pack_forget()  # Remove unused tools

fig.canvas.draw()  # Draw canvas
axbackground = fig.canvas.copy_from_bbox(ax.bbox)  # Background

fig.show()  # Display figure

while True:
    while arduinoData.inWaiting() == 0:  # No data
        pass
    arduinoString = arduinoData.readline()  # Get data
    decodedBytes = arduinoString.decode('utf')  # Decode data to utf-8
    data = (decodedBytes.replace('\r', '')).replace('\n', '')
    # print(data)

    # Get angle and distance from data into a list
    dataList = [float(x) for x in data.split(',')]
    angle = dataList[0]  # Define angle from list
    distance = dataList[1]  # Define distance from list

    # Distances out of range set to 0
    if distance > 100:
        distance = 0

    distances[int(angle)] = distance

    points.set_data(theta, distances)  # Points
    fig.canvas.restore_region(axbackground)  # Redraw background
    ax.draw_artist(points)  # Add points

    line.set_data(np.repeat((angle * (np.pi / 180.0)), 2),  # Draw line from 0 to 180 degrees
                  np.linspace(0.0, 100, 2))  # Draw line for 100 cm distance
    ax.draw_artist(line)  # Draw radar line

    fig.canvas.blit(ax.bbox)  # Re-plot data
    fig.canvas.flush_events()  # Flush GUI events
