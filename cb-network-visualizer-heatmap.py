
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv

#####
raw_data = pd.read_csv('output-performance-evaluation-20220614170605-4R4VM.csv')

print(raw_data)

#####
udf = pd.DataFrame(raw_data)

##### To sort IP address
udf = udf.assign(x=udf['Source IP'].replace(['/.*',r'\b(\d{1})\b',r'\b(\d{2})\b'], ['',r'00\1',r'0\1'], regex=True))
udf = udf.assign(y=udf['Destination IP'].replace(['/.*',r'\b(\d{1})\b',r'\b(\d{2})\b'], ['',r'00\1',r'0\1'], regex=True))

sdf = udf.sort_values(by=['Trial no.','Test case', 'x', 'y'])
# sdf = udf.sort_values(by=['Trial no.','Test case', 'x', 'Destination name'])

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

LEFT=0.05
BOTTOM=0.15
RIGHT=0.95
TOP=0.95
WSPACE=0.2
HSPACE=0.2

figsize_x = 13
figsize_y = 10
v_max = sdf['Average RTT (ms)'].max()
# v_max = 500
v_min = 0
##### Display the test case 1 - Internet communication + No encryption
start_index = 0
print(start_index)
df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
df.index = target_peers

plt.figure(figsize=(figsize_x, figsize_y))
plt.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP, wspace=WSPACE, hspace=HSPACE)

ax = sns.heatmap(df, 
    cbar=True,
    cmap="YlOrRd", 
    annot=True, 
    fmt=".1f", 
    vmin=v_min, 
    vmax=v_max, 
    linewidths=1,
    square=True)

title = "Round Trip Time (ms) - Internet communication"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)

##### Display the test case 2 - Internet communication + Encryption
start_index = start_index + peer_len

print(start_index)
df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
df.index = target_peers

plt.figure(figsize=(figsize_x, figsize_y))
plt.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP, wspace=WSPACE, hspace=HSPACE)

ax = sns.heatmap(df, 
    cbar=True,
    cmap="YlOrRd", 
    annot=True, 
    fmt=".1f", 
    vmin=v_min, 
    vmax=v_max,
    linewidths=1,
    square=True)

title = "Round Trip Time (ms) - Internet communication + encryption"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)

##### Display the test case 3 - Cost-prioritized communication + No encryption
start_index = start_index + peer_len

print(start_index)
df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
df.index = target_peers

plt.figure(figsize=(figsize_x, figsize_y))
plt.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP, wspace=WSPACE, hspace=HSPACE)

ax = sns.heatmap(df, 
    cbar=True,
    cmap="YlOrRd", 
    annot=True, 
    fmt=".1f", 
    vmin=v_min, 
    vmax=v_max,
    linewidths=1,
    square=True)

title = "Round Trip Time (ms) - Cost-based communication"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)

##### Display the test case 4 - Cost-prioritized communication + Encryption
start_index = start_index + peer_len

print(start_index)
df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
df.index = target_peers

plt.figure(figsize=(figsize_x, figsize_y))
plt.subplots_adjust(left=LEFT, bottom=BOTTOM, right=RIGHT, top=TOP, wspace=WSPACE, hspace=HSPACE)

ax = sns.heatmap(df, 
    cbar=True,
    cmap="YlOrRd", 
    annot=True, 
    fmt=".1f", 
    vmin=v_min, 
    vmax=v_max,
    linewidths=1,
    square=True)

title = "Round Trip Time (ms) - Cost-based communication + encryption"
plt.title(title, fontsize=15)
plt.draw()
plt.pause(0.001)

input("Press [enter] to go to the next.")
