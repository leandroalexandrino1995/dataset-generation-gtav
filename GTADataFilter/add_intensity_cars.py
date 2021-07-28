import os
from posixpath import join
import time

def main():

    root_dir = '/media/joao/My Passport/Elements/PointCloudsMaterialHash/'

    f = open("AddInt.txt", "r")
    GTAFolder = int(f.read())
    toSave = GTAFolder

    for subdir, dirs, files in os.walk(root_dir):
        dirs = sorted(dirs, key=lambda filename: int(filename.replace('LiDAR_PointCloud','')))
        for dirName in dirs[GTAFolder:]:

            x = 0

            line_num = []

            lines = 0

            path=os.path.join(root_dir+dirName, 'LiDAR_PointCloud_labels.txt')

            with open(path, 'r') as file:
                i = file.readlines()
                lines = len(i)
                for k in i:
                    if ("2" in k):
                        line_num.append(x)
                    x += 1

            path1=os.path.join(root_dir+dirName, 'LiDAR_PointCloud.ply')

            with open(path1, "r") as file:
                text = file.readlines()[8:]

            line_num_set = set(line_num)

            # start = time.time()

            toWrite = "ply\nformat ascii 1.0\nelement vertex " + str(lines) +  "\nproperty float x\nproperty float y\nproperty float z\nproperty float intensity\nend_header\n"

            for i, x in enumerate(text):
                if i in line_num_set:
                    toWrite += str(x[:-5]) + " 1\n"
                else:
                    toWrite += str(x[:-5]) + " 0\n"

            # print("Demorou ", time.time() -start)

            with open(path1, "w") as file:
                file.write(toWrite)

            # return

            # with open(path1, "w") as file:
            #     file.write("ply\nformat ascii 1.0\nelement vertex " + str(lines) +  "\nproperty float x\nproperty float y\nproperty float z\nproperty float intensity\nend_header\n")
            #     for i, x in enumerate(text):
            #         if i in line_num:
            #             file.write(str(x[:-2]) + " 1\n")
            #         else:
            #             file.write(str(x[:-2]) + " 0\n")

            toSave += 1
            f = open("AddInt.txt", "w")
            f.write(str(toSave))
            f.close()

    return
if __name__=="__main__":
    main()
