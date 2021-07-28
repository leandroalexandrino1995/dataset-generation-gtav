import numpy as np
import os

 
root_dir = '/media/joao/My Passport/Elements/data_object_velodyne/testing/velodyne'

for subdir, dirs, files in os.walk(root_dir):
    for file in files:
        filename = "/media/joao/My Passport/Elements/testing/"+file[:-3]+"txt"
        if not os.path.isfile(filename):
            pointcloud = np.fromfile(root_dir+"/"+file, dtype=np.float32, count=-1).reshape([-1,4])

            x = pointcloud[:, 0]  # x position of point
            y = pointcloud[:, 1]  # y position of point
            z = pointcloud[:, 2]  # z position of point
            r = np.zeros(pointcloud.shape[0])  # reflectance value of point

            to_write = "ply\nformat ascii 1.0\nelement vertex " + str(pointcloud.shape[0]) +  "\nproperty float x\nproperty float y\nproperty float z\nproperty float intensity\nend_header\n"
            for i in set(range(pointcloud.shape[0])):
                to_write += str(x[i])+" "+str(y[i])+" "+str(z[i])+" "+str(r[i])+"\n"

            with open(filename, "w") as f:
                f.write(to_write)