import os

def main():

    root_dir = '/media/joao/My Passport/Elements/PointCloudsMaterialHash_noBackground/'

    f = open("DeleteBack.txt", "r")
    GTAFolder = int(f.read())
    toSave = GTAFolder

    for subdir, dirs, files in os.walk(root_dir):
        dirs = sorted(dirs, key=lambda filename: int(filename.replace('LiDAR_PointCloud','')))
        for dirName in dirs[GTAFolder:]:

            x = 0

            path=os.path.join(root_dir+dirName, 'LiDAR_PointCloud_vehicles_dims.txt')

            with open(path, 'rt') as file:
                dataDims = file.readlines()

            hashes = []

            for k in dataDims:
                if "Car " in k or "Pedestrian " in k:
                    k = k.split()
                    hashes.append(k[0])


            path=os.path.join(root_dir, 'LiDAR_PointCloud_labelsDetailed.txt')

            lines_with_hashes = []

            for i in hashes:
                x = 0
                with open(path, 'r') as file:
                    for k in file.readlines():
                        if (i in k):
                            lines_with_hashes.append(x)
                        x += 1

            path1=os.path.join(root_dir, 'LiDAR_PointCloud.ply')


            with open(path1, "r") as file:
                i = file.readlines()

            with open(path1, "w") as file:
                file.write("ply\nformat ascii 1.0\nelement vertex " + str(len(lines_with_hashes)) + "\nproperty float x\nproperty float y\nproperty float z\nend_header\n")
                for x in lines_with_hashes:
                    file.write(i[x+7])

            toSave += 1
            f = open("DeleteBack.txt", "w")
            f.write(str(toSave))
            f.close()

    return
if __name__=="__main__":
    main()
