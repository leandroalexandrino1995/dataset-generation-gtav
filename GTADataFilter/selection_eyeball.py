from shutil import copyfile
import numpy as np

train_set = ["000150", "000205", "000775", "000808", "000871", "001584", "001599", "001955", "002738", "003473", "003592", "007328"]

for i in train_set:
    copyfile("../../MaterialHash//GTAtoKITTI/kitti/training/label_2/"+i+".txt", "../../eyeball_test/train/"+i+"/"+i+".txt")
    copyfile("../../MaterialHash/GTAtoKITTI/kitti/training/image_2/"+i+".png", "../../eyeball_test/train/"+i+"/"+i+".png")
    copyfile("../../MaterialHash/GTAtoKITTI/kitti/training/velodyne/"+i+".bin", "../../eyeball_test/train/"+i+"/"+i+".bin")
    copyfile("../../MaterialHash//GTAtoKITTI/kitti/training/calib/"+i+".txt", "../../eyeball_test/train/"+i+"/"+i+"_calib.txt")
    
    filename = "../../eyeball_test/train/"+i+"/"+i+".ply"

    pointcloud = np.fromfile("../../eyeball_test/train/"+i+"/"+i+".bin", dtype=np.float32, count=-1).reshape([-1,4])

    x = pointcloud[:, 0]  # x position of point
    y = pointcloud[:, 1]  # y position of point
    z = pointcloud[:, 2]  # z position of point
    r = np.zeros(pointcloud.shape[0])  # reflectance value of point

    to_write = "ply\nformat ascii 1.0\nelement vertex " + str(pointcloud.shape[0]) +  "\nproperty float x\nproperty float y\nproperty float z\nproperty float intensity\nend_header\n"
    for i in set(range(pointcloud.shape[0])):
        to_write += str(x[i])+" "+str(y[i])+" "+str(z[i])+" "+str(r[i])+"\n"

    with open(filename, "w") as f:
        f.write(to_write)


val_set = ["000001", "000167", "000379", "000917", "001088", "001583", "001776", "002258", "003552", "003629", "006478", "007085"]

for i in val_set:
    copyfile("../../MaterialHash//GTAtoKITTI/kitti/training/label_2/"+i+".txt", "../../eyeball_test/val/"+i+"/"+i+".txt")
    copyfile("../../MaterialHash/GTAtoKITTI/kitti/training/image_2/"+i+".png", "../../eyeball_test/val/"+i+"/"+i+".png")
    copyfile("../../MaterialHash/GTAtoKITTI/kitti/training/velodyne/"+i+".bin", "../../eyeball_test/val/"+i+"/"+i+".bin")
    copyfile("../../MaterialHash//GTAtoKITTI/kitti/training/calib/"+i+".txt", "../../eyeball_test/val/"+i+"/"+i+"_calib.txt")
    
    filename = "../../eyeball_test/val/"+i+"/"+i+".ply"

    pointcloud = np.fromfile("../../eyeball_test/val/"+i+"/"+i+".bin", dtype=np.float32, count=-1).reshape([-1,4])

    x = pointcloud[:, 0]  # x position of point
    y = pointcloud[:, 1]  # y position of point
    z = pointcloud[:, 2]  # z position of point
    r = np.zeros(pointcloud.shape[0])  # reflectance value of point

    to_write = "ply\nformat ascii 1.0\nelement vertex " + str(pointcloud.shape[0]) +  "\nproperty float x\nproperty float y\nproperty float z\nproperty float intensity\nend_header\n"
    for i in set(range(pointcloud.shape[0])):
        to_write += str(x[i])+" "+str(y[i])+" "+str(z[i])+" "+str(r[i])+"\n"

    with open(filename, "w") as f:
        f.write(to_write)