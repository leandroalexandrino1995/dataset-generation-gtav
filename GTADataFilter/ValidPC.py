import os
# import numpy as np
# import pandas as pd
import argparse

import shutil

def parse_config():
    parser = argparse.ArgumentParser(description='arg parser')

    parser.add_argument('--rd', type=str, default=None, required=True, help='Root dir for the pointclouds')
    parser.add_argument('--inv', type=int, default=0, required=False, help='Inverted number')

    args = parser.parse_args()

    return args

def main():

    args = parse_config()

    # root_dir='/media/joao/Elements/PointClouds'
    # root_dir='PointClouds'

    root_dir='/media/joao/Elements/Removed/'+args.rd
    root_dir='/media/joao/Elements/'+args.rd
    # root_dir=args.rd
    inv = args.inv
    filename=os.listdir(root_dir)
    file_number=len(filename)

    folder_num = []

    for i in range(file_number):
        path=os.path.join(root_dir, filename[i])
        folder_num.append(int(path.split("LiDAR_PointCloud")[1]))

    folder_num.sort()


    # print(type(folder_num[1]))

    # for i in range(file_number):
    #     root_dir = '/media/joao/Elements/PointClouds'+"/LiDAR_PointCloud"+str(folder_num[i])
    #     filename=os.listdir(root_dir)
    #     print(filename)

    aux = 0
    nice = 0

    for i in range(file_number):
    # root_dir = '/media/joao/Elements/PointClouds'+"/LiDAR_PointCloud"+str(folder_num[i])
        try:
            dir = root_dir+"/LiDAR_PointCloud"+str(folder_num[i])
            filename=os.listdir(dir)
            path=os.path.join(dir, 'LiDAR_PointCloud_labels.txt')
            file = open(path, 'r')
            for k in file.read():
                nice = 0
                if(inv == 0):
                    if((folder_num[i]%2 != 0) and (k == '1' or k == '2')):
                        # print("Folder: " + dir)
                        # print(k)
                        try:
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]))
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i+1]))
                        except OSError:
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i+1]), ignore_errors=True)
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i+1]), ignore_errors=True)
                        # aux += 2
                        break
                    elif((folder_num[i]%2 == 0) and (k == '1' or k == '2')):
                        # print("Folder: " + root_dir)
                        # print(k)
                        nice = 1
                        break
                else:
                    if((folder_num[i]%2 == 0) and (k == '1' or k == '2')):
                        # print("Folder: " + root_dir)
                        # print(k)
                        try:
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]))
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i+1]))
                        except OSError:
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i+1]), ignore_errors=True)
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
                            shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i+1]), ignore_errors=True)
                        # aux += 2
                        break
                    elif((folder_num[i]%2 != 0) and (k == '1' or k == '2')):
                        # print("Folder: " + root_dir)
                        # print(k)
                        aux += 2
                        nice = 1
                        break
            if(inv == 0 and (folder_num[i]%2 == 0) and nice == 0):
                # aux += 2
                try:
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]))
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i-1]))
                except OSError:
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i-1]), ignore_errors=True)
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i-1]), ignore_errors=True)
            elif(inv == 1 and (folder_num[i]%2 != 0) and nice == 0):
                # aux += 2
                try:
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]))
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i-1]))
                except OSError:
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i-1]), ignore_errors=True)
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i-1]), ignore_errors=True)
        except FileNotFoundError:
            continue

    # print("Not to remove: " + str(aux))

if __name__=="__main__":
    main()