
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv

#####
raw_data = pd.read_csv('output-performance-evaluation-20220608173253-3R5VM.csv')

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

###

def get_label_rotation(angle, offset):
    # Rotation must be specified in degrees :(
    rotation = np.rad2deg(angle + offset)
    if angle <= np.pi:
        alignment = "right"
        rotation = rotation + 180
    else: 
        alignment = "left"
    return rotation, alignment

def add_labels(angles, values, labels, offset, ax):
    
    # This is the space between the end of the bar and the label
    padding = 4
    
    # Iterate over angles, values, and labels, to add all of them.
    for angle, value, label, in zip(angles, values, labels):
        angle = angle
        
        # Obtain text rotation and alignment
        rotation, alignment = get_label_rotation(angle, offset)

        # And finally add the text
        ax.text(
            x=angle, 
            y=value + padding, 
            s=label, 
            ha=alignment, 
            va="center", 
            rotation=rotation, 
            rotation_mode="anchor"
        ) 

start_index = 0
# Get columns which are destination peers
df2 = sdf[['Source IP', 'Destination IP', 'Average RTT (ms)']]
df2 = df2[start_index:start_index+peer_len*peer_len]
df2 = df2.reset_index(drop=True)

# df2 = df2.sort_values(by=['Source name', 'Average RTT (ms)'])

print(df2)

# All this part is like the code above
ANGLES = np.linspace(0, 2 * np.pi, len(df2), endpoint=False)
VALUES = df2['Average RTT (ms)'].values
LABELS = df2['Destination IP'].values
GROUP = df2['Source IP'].values

# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2

# Add three empty bars to the end of each group
PAD = 3
ANGLES_N = len(VALUES) + PAD * len(np.unique(GROUP))
ANGLES = np.linspace(0, 2 * np.pi, num=ANGLES_N, endpoint=False)
WIDTH = (2 * np.pi) / len(ANGLES)

# Obtaining the right indexes is now a little more complicated
offset = 0
IDXS = []
GROUPS_SIZE = [peer_len] * peer_len
print(GROUPS_SIZE)

for size in GROUPS_SIZE:
    IDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD

# # The index contains non-empty bards
# IDXS = slice(0, ANGLES_N - PAD)

print(IDXS)
print(offset)

# Same layout as above
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})

ax.set_theta_offset(OFFSET)
ax.set_ylim(-700, 700)
ax.set_frame_on(False)
ax.xaxis.grid(False)
ax.yaxis.grid(True)
ax.set_xticks([])
# ax.set_yticklabels([])
ax.set_yticks([0, 10, 50, 100, 200, 500])

# Use different colors for each group!
GROUPS_SIZE = [peer_len] * peer_len
COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]

# And finally add the bars. 
# Note again the `ANGLES[IDXS]` to drop some angles that leave the space between bars.
ax.bar(
    ANGLES[IDXS], VALUES, width=WIDTH, color=COLORS, 
    edgecolor="white", linewidth=2
)

add_labels(ANGLES[IDXS], VALUES, LABELS, OFFSET, ax)

# Extra customization below here --------------------

# This iterates over the sizes of the groups adding reference
# lines and annotations.

offset = 0 
for group, size in zip(target_peers, GROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(ANGLES[offset + PAD], ANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -200, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    
    # # Add reference lines at 20, 40, 60, and 80
    # x2 = np.linspace(ANGLES[offset], ANGLES[offset + PAD - 1], num=50)
    # ax.plot(x2, [20] * 50, color="#bebebe", lw=0.8)
    # ax.plot(x2, [40] * 50, color="#bebebe", lw=0.8)
    # ax.plot(x2, [60] * 50, color="#bebebe", lw=0.8)
    # ax.plot(x2, [80] * 50, color="#bebebe", lw=0.8)
    
    offset += size + PAD

title = "Round Trip Time (ms) - Internet communication, no encryption"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)



start_index = start_index+peer_len*peer_len
# Get columns which are destination peers
df2 = sdf[['Source IP', 'Destination IP', 'Average RTT (ms)']]
df2 = df2[start_index:start_index+peer_len*peer_len]
df2 = df2.reset_index(drop=True)

# df2 = df2.sort_values(by=['Source name', 'Average RTT (ms)'])

print(df2)

# All this part is like the code above
ANGLES = np.linspace(0, 2 * np.pi, len(df2), endpoint=False)
VALUES = df2['Average RTT (ms)'].values
LABELS = df2['Destination IP'].values
GROUP = df2['Source IP'].values

# Determines where to place the first bar. 
# By default, matplotlib starts at 0 (the first bar is horizontal)
# but here we say we want to start at pi/2 (90 deg)
OFFSET = np.pi / 2

# Add three empty bars to the end of each group
PAD = 3
ANGLES_N = len(VALUES) + PAD * len(np.unique(GROUP))
ANGLES = np.linspace(0, 2 * np.pi, num=ANGLES_N, endpoint=False)
WIDTH = (2 * np.pi) / len(ANGLES)

# Obtaining the right indexes is now a little more complicated
offset = 0
IDXS = []
GROUPS_SIZE = [peer_len] * peer_len
print(GROUPS_SIZE)

for size in GROUPS_SIZE:
    IDXS += list(range(offset + PAD, offset + size + PAD))
    offset += size + PAD

# # The index contains non-empty bards
# IDXS = slice(0, ANGLES_N - PAD)

print(IDXS)
print(offset)

# Same layout as above
fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={"projection": "polar"})

ax.set_theta_offset(OFFSET)
ax.set_ylim(-700, 700)
ax.set_frame_on(False)
ax.xaxis.grid(False)
ax.yaxis.grid(True)
ax.set_xticks([])
# ax.set_yticklabels([])
ax.set_yticks([0, 10, 50, 100, 200, 500])

# Use different colors for each group!
GROUPS_SIZE = [peer_len] * peer_len
COLORS = [f"C{i}" for i, size in enumerate(GROUPS_SIZE) for _ in range(size)]

# And finally add the bars. 
# Note again the `ANGLES[IDXS]` to drop some angles that leave the space between bars.
ax.bar(
    ANGLES[IDXS], VALUES, width=WIDTH, color=COLORS, 
    edgecolor="white", linewidth=2
)

add_labels(ANGLES[IDXS], VALUES, LABELS, OFFSET, ax)

# Extra customization below here --------------------

# This iterates over the sizes of the groups adding reference
# lines and annotations.

offset = 0 
for group, size in zip(target_peers, GROUPS_SIZE):
    # Add line below bars
    x1 = np.linspace(ANGLES[offset + PAD], ANGLES[offset + size + PAD - 1], num=50)
    ax.plot(x1, [-5] * 50, color="#333333")
    
    # Add text to indicate group
    ax.text(
        np.mean(x1), -200, group, color="#333333", fontsize=14, 
        fontweight="bold", ha="center", va="center"
    )
    
    # # Add reference lines at 20, 40, 60, and 80
    # x2 = np.linspace(ANGLES[offset], ANGLES[offset + PAD - 1], num=50)
    # ax.plot(x2, [20] * 50, color="#bebebe", lw=0.8)
    # ax.plot(x2, [40] * 50, color="#bebebe", lw=0.8)
    # ax.plot(x2, [60] * 50, color="#bebebe", lw=0.8)
    # ax.plot(x2, [80] * 50, color="#bebebe", lw=0.8)
    
    offset += size + PAD

title = "Round Trip Time (ms) - Internet communication, encryption"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)

input("Press [enter] to quit.")