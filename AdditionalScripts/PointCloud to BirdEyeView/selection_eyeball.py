from shutil import copyfile
import os

groundTruthDataDirPath = "../../../eyeball_test/val/"
for subdir, dirs, files in os.walk(groundTruthDataDirPath):
        for dirName in dirs:
            copyfile("../../../eyeball_test/val/"+dirName+"/"+dirName+"_withBB.png", "../../../eyeball_test/all_val/"+dirName+".png")
            # copyfile("../../../eyeball_test/train/"+dirName+"/"+dirName+".ply", "../../eyeball_test/all_train/"+dirName+".ply")

# train_set = ["000150\n", "000871\n", "001955\n", "003473\n"]

# for i in train_set:
#     copyfile("../../MaterialHash_noBackground//GTAtoKITTI/kitti/training/label_2/"+i[:-1]+".txt", "../../eyeball_test/train/"+i[:-1]+"/"+i[:-1]+".txt")
#     copyfile("../../MaterialHash_noBackground/GTAtoKITTI/kitti/training/image_2/"+i[:-1]+".png", "../../eyeball_test/train/"+i[:-1]+"/"+i[:-1]+".png")
#     copyfile("../../MaterialHash_noBackground/GTAtoKITTI/kitti/training/velodyne/"+i[:-1]+".bin", "../../eyeball_test/train/"+i[:-1]+"/"+i[:-1]+".bin")


# val_set = ["000001\n", "000379\n", "001088\n", "002258\n"]

# for i in val_set:
#     copyfile("../../MaterialHash_noBackground//GTAtoKITTI/kitti/training/label_2/"+i[:-1]+".txt", "../../eyeball_test/val/"+i[:-1]+"/"+i[:-1]+".txt")
#     copyfile("../../MaterialHash_noBackground/GTAtoKITTI/kitti/training/image_2/"+i[:-1]+".png", "../../eyeball_test/val/"+i[:-1]+"/"+i[:-1]+".png")
#     copyfile("../../MaterialHash_noBackground/GTAtoKITTI/kitti/training/velodyne/"+i[:-1]+".bin", "../../eyeball_test/val/"+i[:-1]+"/"+i[:-1]+".bin")
