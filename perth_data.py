# from multi_lanes import Car, Road
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib import animation
import pandas as pd
# import seaborn as sns

raw_counts = pd.read_csv('Data/dft_rawcount_local_authority_id_31.csv')

print(raw_counts.head())
m90data = raw_counts[raw_counts['road_name'] == 'M90']
avg_flow = m90data['all_motor_vehicles'].mean()
print(avg_flow)

# plots
lanes = 4
length = 3219
t_vals = np.arange(10000)
roadworks = [0,400,600]

my_road = Road(length = length, density = 0.05, p = 0.1 , v_max = 31.3, no_lanes = lanes, roadworks=roadworks)

x_vals = np.zeros((lanes, length, len(t_vals)))

for t in t_vals:   
    x_vals[:,:,t] = my_road.road_to_values()
    my_road.timestep()

coords = []

for l in range(lanes):
    for t in t_vals: 
        for p, v in enumerate(x_vals[l,:,t]):
            if v != -1:
                coords.append((l, t, p, v))
    
average_speed_by_position = np.zeros((lanes, length))
count_by_position = np.full((lanes, length), 0.01)

for coord in coords:
    if coord[3] != -2:
        average_speed_by_position[coord[0],coord[2]] += coord[3]
        count_by_position[coord[0],coord[2]] += 1

average_speed_by_position = average_speed_by_position/count_by_position
average_speed_by_position[roadworks[0]][roadworks[1]:roadworks[2]] = -1

fig, ax = plt.subplots(1, 1, figsize = (12, 2))

ax = sns.heatmap(average_speed_by_position, cbar_kws={'label': 'Speed (m/s)'})
ax = sns.heatmap(average_speed_by_position, mask= average_speed_by_position != -1, cmap='Greens', cbar = False)

ticks = list(np.linspace(0, length, 21).astype('int64'))
ax.set_xticks(ticks)
ax.set_xticklabels(ticks)

plt.xlabel('Position on road')
plt.ylabel('Lane')
plt.legend()
plt.show()

fig.savefig(f'M90-Heatmap', bbox_inches = 'tight')