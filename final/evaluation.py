import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
orb_slam = pd.read_csv('KeyFrameTrajectory.txt', sep=' ', names=['frame', 'x', 'y', 'z', 'q_x', 'q_y', 'q_z', 'q_w'])
colmap = pd.read_csv('colmap.txt', sep=' ', names=['frame', 'focal_length', 'q_w', 'q_x', 'q_y', 'q_z', 'x', 'y', 'z', 'radial_distortion', '0'])
orb_slam = orb_slam.drop(['q_x', 'q_y', 'q_z', 'q_w'], axis=1)
colmap = colmap.drop(['focal_length', 'q_w', 'q_x', 'q_y', 'q_z', 'radial_distortion', '0'], axis=1)
for i in range(colmap.shape[0]):
    temp = ''
    for j in range(len(colmap.iloc[i, 0])):
        if colmap.iloc[i, 0][j].isnumeric():
            temp += colmap.iloc[i, 0][j]
    colmap.iloc[i, 0] = temp
colmap['frame'] = colmap['frame'].astype(int)
orb_slam['frame'] = orb_slam['frame'].astype(int)

colmap = colmap.sort_values(by=['frame']).reset_index(drop=True)
orb_slam = orb_slam.sort_values(by=['frame']).reset_index(drop=True)
#A*T=B, T=inverse(A)*B 
i = 25
j = 40
k = 87
i0 = orb_slam['frame'][i]
j0 = orb_slam['frame'][j]
k0 = orb_slam['frame'][k]
A = np.matrix([[orb_slam['x'][i], orb_slam['y'][i], orb_slam['z'][i]], [orb_slam['x'][j], orb_slam['y'][j], orb_slam['z'][j]], [orb_slam['x'][k], orb_slam['y'][k], orb_slam['z'][k]]])
B = np.matrix([[colmap['x'][i0], colmap['y'][i0], colmap['z'][i0]],[colmap['x'][j0], colmap['y'][j0], colmap['z'][j0]],[colmap['x'][k0], colmap['y'][k0], colmap['z'][k0]]])
T = np.linalg.inv(100*A)*(100*B)
orb_slam_transformed = pd.DataFrame(columns=['x', 'y', 'z'])
for i in range(orb_slam.shape[0]):
    a = np.matrix([[orb_slam['x'][i], orb_slam['y'][i], orb_slam['z'][i]]])
    b = pd.DataFrame(a*T,columns=['x', 'y', 'z'])
    orb_slam_transformed = pd.concat([orb_slam_transformed, b], ignore_index=True)
total_error = 0
j = 0
for i in range(orb_slam_transformed.shape[0]):
    frame = orb_slam['frame'][i]
    while colmap['frame'][j] != frame:
        if j+1<colmap.shape[0]:
            j += 1
        else:
            break
    total_error += ((orb_slam_transformed['x'][i]-colmap['x'][j])**2 + (orb_slam_transformed['y'][i]-colmap['y'][j])**2 + (orb_slam_transformed['z'][i]-colmap['z'][j])**2)**0.5
print('Total error: %.4f' % total_error)
print('Average error: %.4f' % (total_error/orb_slam_transformed.shape[0]))

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter3D(orb_slam_transformed['x'], orb_slam_transformed['y'], orb_slam_transformed['z'], color=[0.5, 0, 0], label='ORB-SLAM2')
ax.scatter3D(colmap['x'], colmap['y'], colmap['z'], color=[0, 0, 0.5], label='COLMAP')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.title('ORB-SLAM2 and COLMAP')
plt.legend()
plt.show()