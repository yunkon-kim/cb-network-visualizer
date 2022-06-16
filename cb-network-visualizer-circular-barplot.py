
from tkinter import font
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv

#####
raw_data = pd.read_csv('output-performance-evaluation-20220613205712-20R1VM.csv')

print(raw_data)

#####
udf = pd.DataFrame(raw_data)

##### To sort IP address
udf = udf.assign(x=udf['Source IP'].replace(['/.*',r'\b(\d{1})\b',r'\b(\d{2})\b'], ['',r'00\1',r'0\1'], regex=True))
udf = udf.assign(y=udf['Destination IP'].replace(['/.*',r'\b(\d{1})\b',r'\b(\d{2})\b'], ['',r'00\1',r'0\1'], regex=True))

# sdf = udf.sort_values(by=['Trial no.','Test case', 'x', 'y'])
sdf = udf.sort_values(by=['Trial no.','Test case', 'x', 'y'])

print("sdf: ")
print(sdf)

# Count destination peers
is_not_first = False
peer_len = 0
current_source_ip = ""
previous_source_ip = ""

for label, rows in sdf.iterrows():
    
    previous_source_ip = current_source_ip    
    current_source_ip = rows['Source IP']

    if previous_source_ip != current_source_ip and is_not_first:
        break

    peer_len += 1
    is_not_first = True

# Get columns which are destination peers
selected_destination_ip = sdf['Destination IP']
target_peers = selected_destination_ip[:peer_len]

print("target_peers: ")
print(target_peers)

start_index = 0
# Get columns which are destination peers
df2 = sdf[['Destination IP', 'Average RTT (ms)']]
df2 = df2[start_index:start_index+peer_len]
df2 = df2.reset_index(drop=True)
df2 = df2.sort_values(by=['Average RTT (ms)'])


# Constants = parameters controling the plot layout:
upperLimit = 500
lowerLimit = 0
labelPadding = 20

LEFT=0.2
BOTTOM=0.2
RIGHT=0.8
TOP=0.8
WSPACE=0.2
HSPACE=0.2

# Compute max and min in the dataset
max = df2['Average RTT (ms)'].max()
# max = 500

###
# initialize the figure
plt.figure(figsize=(12,12))
ax = plt.subplot(111, polar=True)
plt.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP, wspace=WSPACE, hspace=HSPACE)
plt.axis('off')

# Let's compute heights: they are a conversion of each item value in those new coordinates
# In our example, 0 in the dataset will be converted to the lowerLimit (10)
# The maximum will be converted to the upperLimit (100)
slope = (max - lowerLimit) / max
heights = slope * df2['Average RTT (ms)'] + lowerLimit

# Compute the width of each bar. In total we have 2*Pi = 360°
width = 2*np.pi / len(df2.index)

# Compute the angle each bar is centered on:
indexes = list(range(1, len(df2.index)+1))
angles = [element * width for element in indexes]
angles

# Draw bars
bars = ax.bar(
    x=angles, 
    height=heights, 
    width=width, 
    bottom=lowerLimit,
    linewidth=3, 
    edgecolor="white",
    color="#61a4b2",
)

df2['label'] = df2['Destination IP'] + " (" + df2['Average RTT (ms)'].astype(str) + " ms)"
print(df2['label'])

# Add labels
for bar, angle, height, label in zip(bars, angles, heights, df2['label']):

    # Labels are rotated. Rotation must be specified in degrees :(
    rotation = np.rad2deg(angle)

    # Flip some labels upside down
    alignment = ""
    if angle >= np.pi/2 and angle < 3*np.pi/2:
        alignment = "right"
        rotation = rotation + 180
    else: 
        alignment = "left"

    # Finally add the labels
    ax.text(
        x=angle, 
        y=lowerLimit + bar.get_height() + labelPadding, 
        s=label, 
        ha=alignment, 
        va='center', 
        rotation=rotation, 
        rotation_mode="anchor")


title = "Round Trip Time (ms) from " + previous_source_ip +" - Internet communication, no encryption"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)

################################################################################
################################################################################
################################################################################

start_index = start_index + peer_len*peer_len
# Get columns which are destination peers
df2 = sdf[['Destination IP', 'Average RTT (ms)']]
df2 = df2[start_index:start_index+peer_len]
df2 = df2.reset_index(drop=True)
df2 = df2.sort_values(by=['Average RTT (ms)'])


###
# initialize the figure
plt.figure(figsize=(12,12))
ax = plt.subplot(111, polar=True)
plt.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP, wspace=WSPACE, hspace=HSPACE)
plt.axis('off')

# Compute max and min in the dataset
max = df2['Average RTT (ms)'].max()

# Let's compute heights: they are a conversion of each item value in those new coordinates
# In our example, 0 in the dataset will be converted to the lowerLimit (10)
# The maximum will be converted to the upperLimit (100)
slope = (max - lowerLimit) / max
heights = slope * df2['Average RTT (ms)'] + lowerLimit

# Compute the width of each bar. In total we have 2*Pi = 360°
width = 2*np.pi / len(df2.index)

# Compute the angle each bar is centered on:
indexes = list(range(1, len(df2.index)+1))
angles = [element * width for element in indexes]
angles

# Draw bars
bars = ax.bar(
    x=angles, 
    height=heights, 
    width=width, 
    bottom=lowerLimit,
    linewidth=3, 
    edgecolor="white",
    color="#61a4b2",
)

df2['label'] = df2['Destination IP'] + " (" + df2['Average RTT (ms)'].astype(str) + " ms)"
print(df2['label'])

# Add labels
for bar, angle, height, label in zip(bars, angles, heights, df2['label']):

    # Labels are rotated. Rotation must be specified in degrees :(
    rotation = np.rad2deg(angle)

    # Flip some labels upside down
    alignment = ""
    if angle >= np.pi/2 and angle < 3*np.pi/2:
        alignment = "right"
        rotation = rotation + 180
    else: 
        alignment = "left"

    # Finally add the labels
    ax.text(
        x=angle, 
        y=lowerLimit + bar.get_height() + labelPadding, 
        s=label, 
        ha=alignment, 
        va='center', 
        rotation=rotation, 
        rotation_mode="anchor")


title = "Round Trip Time (ms) from " + previous_source_ip +" - Internet communication, encryption"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)

################################################################################
################################################################################
################################################################################

start_index = start_index + peer_len*peer_len
# Get columns which are destination peers
df2 = sdf[['Destination IP', 'Average RTT (ms)']]
df2 = df2[start_index:start_index+peer_len]
df2 = df2.reset_index(drop=True)
df2 = df2.sort_values(by=['Average RTT (ms)'])


###
# initialize the figure
plt.figure(figsize=(12,12))
ax = plt.subplot(111, polar=True)
plt.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP, wspace=WSPACE, hspace=HSPACE)
plt.axis('off')

# Compute max and min in the dataset
max = df2['Average RTT (ms)'].max()

# Let's compute heights: they are a conversion of each item value in those new coordinates
# In our example, 0 in the dataset will be converted to the lowerLimit (10)
# The maximum will be converted to the upperLimit (100)
slope = (max - lowerLimit) / max
heights = slope * df2['Average RTT (ms)'] + lowerLimit

# Compute the width of each bar. In total we have 2*Pi = 360°
width = 2*np.pi / len(df2.index)

# Compute the angle each bar is centered on:
indexes = list(range(1, len(df2.index)+1))
angles = [element * width for element in indexes]
angles

# Draw bars
bars = ax.bar(
    x=angles, 
    height=heights, 
    width=width, 
    bottom=lowerLimit,
    linewidth=3, 
    edgecolor="white",
    color="#61a4b2",
)

df2['label'] = df2['Destination IP'] + " (" + df2['Average RTT (ms)'].astype(str) + " ms)"
print(df2['label'])

# Add labels
for bar, angle, height, label in zip(bars, angles, heights, df2['label']):

    # Labels are rotated. Rotation must be specified in degrees :(
    rotation = np.rad2deg(angle)

    # Flip some labels upside down
    alignment = ""
    if angle >= np.pi/2 and angle < 3*np.pi/2:
        alignment = "right"
        rotation = rotation + 180
    else: 
        alignment = "left"

    # Finally add the labels
    ax.text(
        x=angle, 
        y=lowerLimit + bar.get_height() + labelPadding, 
        s=label, 
        ha=alignment, 
        va='center', 
        rotation=rotation, 
        rotation_mode="anchor")


title = "Round Trip Time (ms) from " + previous_source_ip +" - Cost-prioritized communication, no encryption"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)

################################################################################
################################################################################
################################################################################

start_index = start_index + peer_len*peer_len
# Get columns which are destination peers
df2 = sdf[['Destination IP', 'Average RTT (ms)']]
df2 = df2[start_index:start_index+peer_len]
df2 = df2.reset_index(drop=True)
df2 = df2.sort_values(by=['Average RTT (ms)'])


###
# initialize the figure
plt.figure(figsize=(12,12))
ax = plt.subplot(111, polar=True)
plt.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP, wspace=WSPACE, hspace=HSPACE)
plt.axis('off')

# Compute max and min in the dataset
max = df2['Average RTT (ms)'].max()

# Let's compute heights: they are a conversion of each item value in those new coordinates
# In our example, 0 in the dataset will be converted to the lowerLimit (10)
# The maximum will be converted to the upperLimit (100)
slope = (max - lowerLimit) / max
heights = slope * df2['Average RTT (ms)'] + lowerLimit

# Compute the width of each bar. In total we have 2*Pi = 360°
width = 2*np.pi / len(df2.index)

# Compute the angle each bar is centered on:
indexes = list(range(1, len(df2.index)+1))
angles = [element * width for element in indexes]
angles

# Draw bars
bars = ax.bar(
    x=angles, 
    height=heights, 
    width=width, 
    bottom=lowerLimit,
    linewidth=3, 
    edgecolor="white",
    color="#61a4b2",
)

df2['label'] = df2['Destination IP'] + " (" + df2['Average RTT (ms)'].astype(str) + " ms)"
print(df2['label'])

# Add labels
for bar, angle, height, label in zip(bars, angles, heights, df2['label']):

    # Labels are rotated. Rotation must be specified in degrees :(
    rotation = np.rad2deg(angle)

    # Flip some labels upside down
    alignment = ""
    if angle >= np.pi/2 and angle < 3*np.pi/2:
        alignment = "right"
        rotation = rotation + 180
    else: 
        alignment = "left"

    # Finally add the labels
    ax.text(
        x=angle, 
        y=lowerLimit + bar.get_height() + labelPadding, 
        s=label, 
        ha=alignment, 
        va='center', 
        rotation=rotation, 
        rotation_mode="anchor")


title = "Round Trip Time (ms) from " + previous_source_ip +" - Cost-prioritized communication, encryption"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)

input("Press [enter] to quit.")