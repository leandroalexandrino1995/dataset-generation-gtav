import os
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

    root_dir='/media/joao/My Passport/Elements/BonsDadosComHashes-backup/'+args.rd
    # root_dir=args.rd
    inv = args.inv
    filename=os.listdir(root_dir)
    file_number=len(filename)

    folder_num = []

    for i in range(file_number):
        path=os.path.join(root_dir, filename[i])
        folder_num.append(int(path.split("LiDAR_PointCloud")[1]))

    folder_num.sort()

    for i in range(file_number):
        try:
            file_stats = os.stat(path)
            if (file_stats.st_size == 0):
                try:
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]))
                except OSError:
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
                    shutil.rmtree(root_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)

        except FileNotFoundError:
            continue

if __name__=="__main__":
    main()
