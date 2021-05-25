import os

def main():

    root_dir='/media/joao/Elements/Removed/TestMePapi'
    filename=os.listdir(root_dir)
    file_number=len(filename)

    x = 0
    j = 0

    line_num = []

    path=os.path.join(root_dir, 'LiDAR_PointCloud94/LiDAR_PointCloud_labels.txt')
    with open(path, 'r') as file:
        for k in file.readlines():
            if (k == "0\n"):
                line_num.append(x)
                j += 1
            x += 1

    path=os.path.join(root_dir, 'LiDAR_PointCloud94/LiDAR_PointCloud_labelsDetailed.txt')

    elements = set()

    with open(path, 'r') as file:
        i2 = file.readlines()

        for x in line_num:
            elements.add(i2[x])

    elements = list(elements)

    print(len(elements))
    divider = round(len(elements)/4)

    path1=os.path.join(root_dir, 'LiDAR_PointCloud94/LiDAR_PointCloud.ply')

    with open('test2.ply', "w") as file:
        file.write("ply\nformat ascii 1.0\nelement vertex " + str(len(line_num)) + "\nproperty float x\nproperty float y\nproperty float z\nproperty uchar red\nproperty uchar green\nproperty uchar blue\nend_header\n")
        with open(path1, "r") as file1:
            i = file1.readlines()
            for k in line_num:
                if(int(elements.index(i2[k]))+1 < divider):
                    file.write(i[k+7][:-2] + " " + str(round(255/(int(elements.index(i2[k]))+1))) + " " + str(255) + " " + str(255) + "\n")
                elif(int(elements.index(i2[k]))+1 < divider*2):
                    file.write(i[k+7][:-2] + " " + str(255) + " " + str(round(255/(int(elements.index(i2[k]))+1))) + " " + str(255) + "\n")
                elif(int(elements.index(i2[k]))+1 < divider*2):
                    file.write(i[k+7][:-2] + " " + str(255) + " " + str(255) + " " + str(round(255/(int(elements.index(i2[k]))+1))) + "\n")    
                else:
                    file.write(i[k+7][:-2] + " " + str(round(255*((int(elements.index(i2[k])))/len(elements)))) + " " + str(round(255*((int(elements.index(i2[k])))/len(elements)))) + " " + str(round(255*((int(elements.index(i2[k])))/len(elements)))) + "\n")

if __name__=="__main__":
    main()