from shutil import copyfile

train_set = ["000150", "000205", "000775", "000808", "000871", "001584", "001599", "001955", "002738", "003473", "003592", "007328"]

for i in train_set:
    # copyfile("../../MaterialHash_noBackground//GTAtoKITTI/kitti/training/label_2/"+i+".txt", "../../eyeball_test/train/"+i+"/"+i+".txt")
    # copyfile("../../MaterialHash_noBackground/GTAtoKITTI/kitti/training/image_2/"+i+".png", "../../eyeball_test/train/"+i+"/"+i+".png")
    # copyfile("../../MaterialHash_noBackground/GTAtoKITTI/kitti/training/velodyne/"+i+".bin", "../../eyeball_test/train/"+i+"/"+i+".bin")
    copyfile("../../MaterialHash_noBackground//GTAtoKITTI/kitti/training/calib/"+i+".txt", "../../eyeball_test/train/"+i+"/"+i+"_calib.txt")


val_set = ["000001", "000167", "000379", "000917", "001088", "001583", "001776", "002258", "003552", "003629", "006478", "007085"]

for i in val_set:
    # copyfile("../../MaterialHash_noBackground//GTAtoKITTI/kitti/training/label_2/"+i+".txt", "../../eyeball_test/val/"+i+"/"+i+".txt")
    # copyfile("../../MaterialHash_noBackground/GTAtoKITTI/kitti/training/image_2/"+i+".png", "../../eyeball_test/val/"+i+"/"+i+".png")
    # copyfile("../../MaterialHash_noBackground/GTAtoKITTI/kitti/training/velodyne/"+i+".bin", "../../eyeball_test/val/"+i+"/"+i+".bin")
    copyfile("../../MaterialHash_noBackground//GTAtoKITTI/kitti/training/calib/"+i+".txt", "../../eyeball_test/val/"+i+"/"+i+"_calib.txt")
