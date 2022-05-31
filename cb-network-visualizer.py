
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
selected_destination_ip = sdf['Destination name']
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



figsize_x = 12
figsize_y = 8
v_max = 500
v_min = 0
##### Display the test case 1 - Internet communication + No encryption
start_index = 0
print(start_index)
df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
df.index = target_peers

plt.figure(figsize=(figsize_x, figsize_y))

ax = sns.heatmap(df, 
    cbar=True,
    cmap="YlOrRd", 
    annot=True, 
    fmt=".2f", 
    vmin=v_min, 
    vmax=v_max, 
    linewidths=1,
    square=True)

title = "Round Trip Time (ms) - Internet communication, no encryption"
plt.title(title)
plt.draw()
plt.pause(0.001)

##### Display the test case 2 - Internet communication + Encryption
start_index = start_index + peer_len

print(start_index)
df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
df.index = target_peers

plt.figure(figsize=(figsize_x, figsize_y))

ax = sns.heatmap(df, 
    cbar=True,
    cmap="YlOrRd", 
    annot=True, 
    fmt=".2f", 
    vmin=v_min, 
    vmax=v_max,
    linewidths=1,
    square=True)

title = "Round Trip Time (ms) - Internet communication, encryption"
plt.title(title)
plt.draw()
plt.pause(0.001)

##### Display the test case 3 - Cost-prioritized communication + No encryption
start_index = start_index + peer_len

print(start_index)
df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
df.index = target_peers

plt.figure(figsize=(figsize_x, figsize_y))

ax = sns.heatmap(df, 
    cbar=True,
    cmap="YlOrRd", 
    annot=True, 
    fmt=".2f", 
    vmin=v_min, 
    vmax=v_max,
    linewidths=1,
    square=True)

title = "Round Trip Time (ms) - Cost-prioritized communication, no encryption"
plt.title(title)
plt.draw()
plt.pause(0.001)

##### Display the test case 4 - Cost-prioritized communication + Encryption
start_index = start_index + peer_len

print(start_index)
df = pd.DataFrame(rtt_data_2d[start_index:start_index+peer_len], columns=target_peers)
df.index = target_peers

plt.figure(figsize=(figsize_x, figsize_y))

ax = sns.heatmap(df, 
    cbar=True,
    cmap="YlOrRd", 
    annot=True, 
    fmt=".2f", 
    vmin=v_min, 
    vmax=v_max,
    linewidths=1,
    square=True)

title = "Round Trip Time (ms) - Cost-prioritized communication, encryption"
plt.title(title)
plt.draw()
plt.pause(0.001)

input("Press [enter] to quit.")