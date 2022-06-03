
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv

#####
raw_data = pd.read_csv('output-performance-evaluation-20220531210546.csv')

print(raw_data)

#####
udf=pd.DataFrame(raw_data)
sdf=udf.sort_values(by=['Trial no.','Test case', 'Source IP', 'Destination IP'])

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

# Select and reshape data
selected_data = sdf['Average RTT (ms)']

rtt_data_2d = np.reshape(selected_data.to_numpy(), (int(len(selected_data)/peer_len), peer_len ))

print("rtt_data_2d: ")
print(rtt_data_2d)
print("len rtt_dat_2d: ")
print(len(rtt_data_2d))



# figsize_x = 12
# figsize_y = 8
# v_max = 500
# v_min = 0
# ##### Display the test case 1 - Internet communication + No encryption
# start_index = 0
# print(start_index)
# df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
# df.index = target_peers

# plt.figure(figsize=(figsize_x, figsize_y))

# ax = sns.heatmap(df, 
#     cbar=True,
#     cmap="YlOrRd", 
#     annot=True, 
#     fmt=".2f", 
#     vmin=v_min, 
#     vmax=v_max, 
#     linewidths=1,
#     square=True)

# title = "Round Trip Time (ms) - Internet communication, no encryption"
# plt.title(title)
# plt.draw()
# plt.pause(0.001)

# ##### Display the test case 2 - Internet communication + Encryption
# start_index = start_index + peer_len

# print(start_index)
# df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
# df.index = target_peers

# plt.figure(figsize=(figsize_x, figsize_y))

# ax = sns.heatmap(df, 
#     cbar=True,
#     cmap="YlOrRd", 
#     annot=True, 
#     fmt=".2f", 
#     vmin=v_min, 
#     vmax=v_max,
#     linewidths=1,
#     square=True)

# title = "Round Trip Time (ms) - Internet communication, encryption"
# plt.title(title)
# plt.draw()
# plt.pause(0.001)

# ##### Display the test case 3 - Cost-prioritized communication + No encryption
# start_index = start_index + peer_len

# print(start_index)
# df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
# df.index = target_peers

# plt.figure(figsize=(figsize_x, figsize_y))

# ax = sns.heatmap(df, 
#     cbar=True,
#     cmap="YlOrRd", 
#     annot=True, 
#     fmt=".2f", 
#     vmin=v_min, 
#     vmax=v_max,
#     linewidths=1,
#     square=True)

# title = "Round Trip Time (ms) - Cost-prioritized communication, no encryption"
# plt.title(title)
# plt.draw()
# plt.pause(0.001)

# ##### Display the test case 4 - Cost-prioritized communication + Encryption
# start_index = start_index + peer_len

# print(start_index)
# df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
# df.index = target_peers

# plt.figure(figsize=(figsize_x, figsize_y))

# ax = sns.heatmap(df, 
#     cbar=True,
#     cmap="YlOrRd", 
#     annot=True, 
#     fmt=".2f", 
#     vmin=v_min, 
#     vmax=v_max,
#     linewidths=1,
#     square=True)

# title = "Round Trip Time (ms) - Cost-prioritized communication, encryption"
# plt.title(title)
# plt.draw()
# plt.pause(0.001)

# input("Press [enter] to quit.")

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

# Get columns which are destination peers
df2 = sdf[['Source IP', 'Destination IP', 'Average RTT (ms)']]
df2 = df2[:peer_len*peer_len]
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

# # Constants = parameters controling the plot layout:
# upperLimit = 100
# lowerLimit = 30
# labelPadding = 4

# # Compute max and min in the dataset
# max = df2['Average RTT (ms)'].max()

# # Let's compute heights: they are a conversion of each item value in those new coordinates
# # In our example, 0 in the dataset will be converted to the lowerLimit (10)
# # The maximum will be converted to the upperLimit (100)
# slope = (max - lowerLimit) / max
# HEIGHT = slope * df2['Average RTT (ms)'] + lowerLimit

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

plt.show()