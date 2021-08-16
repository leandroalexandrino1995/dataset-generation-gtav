from shutil import copyfile
import os

arr = ["000167", "000383", "000177", "000222", "007286"]

root_dir = '/media/joao/My Passport/Elements/MaterialHash_withIntensity_v2/GTAtoKITTI/kitti/'

aux = 0
for subdir, dirs, files in os.walk(root_dir+"extra/calib"):
        for file in files[300:]:
            copyfile(root_dir+"extra/calib/"+file, root_dir+"training/calib/"+arr[aux]+".txt")
            copyfile(root_dir+"extra/label_2/"+file, root_dir+"training/label_2/"+arr[aux]+".txt")
            copyfile(root_dir+"extra/image_2/"+file[:-4]+".png", root_dir+"training/image_2/"+arr[aux]+".png")
            copyfile(root_dir+"extra/velodyne/"+file[:-4]+".bin", root_dir+"training/velodyne/"+arr[aux]+".bin")
            aux+=1
