import numpy as np

 
pointcloud = np.fromfile(str("/home/joao/Desktop/000000.bin"), dtype=np.float32, count=-1).reshape([-1,4])

print(pointcloud.shape)

x = pointcloud[:, 0]  # x position of point
y = pointcloud[:, 1]  # y position of point
z = pointcloud[:, 2]  # z position of point
r = pointcloud[:, 3]  # reflectance value of point

for i in range(pointcloud.shape[0]):
    print(x[i],y[i],z[i],r[i])

# pointcloud = np.fromfile(str("/home/joao/Desktop/000000_noBck.bin"), dtype=np.float32, count=-1).reshape([-1,4])

# print(pointcloud.shape)

# x = pointcloud[:, 0]  # x position of point
# y = pointcloud[:, 1]  # y position of point
# z = pointcloud[:, 2]  # z position of point
# r = pointcloud[:, 3]  # reflectance value of point

# print("noBck")

# for i in range(pointcloud.shape[0]):
#     print(x[i],y[i],z[i],r[i])