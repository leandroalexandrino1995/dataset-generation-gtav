import os
from posixpath import expanduser
# import argparse

import shutil

# def parse_config():
#     parser = argparse.ArgumentParser(description='arg parser')

#     parser.add_argument('--rd', type=str, default=None, required=True, help='Root dir for the pointclouds')
#     parser.add_argument('--inv', type=int, default=0, required=False, help='Inverted number')

#     args = parser.parse_args()

#     return args

def main():

    # args = parse_config()

    sf = ["+PCs"]
        # \, "PointClouds", "PointClouds2ndSession", "PointCloudsASerio", "PointCloudsMesmoASerio", "PointCloudsMesmoASerio_vCARAPAS", \
        #  "PointCloudsMesmoASerio_vPAI", "PointCloudsMesmoASerio_vPAI_NumInv", "OQueGostoMesmoEDePCs_vREALISTA", "OQueGostoMesmoEDePCs_vREALISTA_INV",\
        #  "OQueGostoMesmoEDePCs_vPAI"]

    df_dir='/media/joao/Elements/WeirdTest/AllPointClouds/'

    filename=os.listdir(df_dir)
    num=len(filename)

    # num = 14503
    # 1906

    for x in sf:
        sf_dir='/media/joao/Elements/WeirdTest/'+x

        print(sf_dir)

        filename=os.listdir(sf_dir)
        # file_number=len(filename)

        for name in filename:

            source_dir=sf_dir+'/'+name

            # print(source_dir)

            dest_dir=df_dir+''+name[:16]+''+str(num)
            # try:
            shutil.copytree(source_dir, dest_dir)
            # except FileExistsError:
            #     continue
            # print(dest_dir)
            num += 1
            # break

        # break

        # folder_num = []

        # for i in range(file_number):
        #     path=os.path.join(sf_dir, filename[i])
        #     folder_num.append(int(path.split("LiDAR_PointCloud")[1]))

        # folder_num.sort()

        # for i in range(file_number):
        #     try:
        #         dir = sf_dir+"/LiDAR_PointCloud"+str(folder_num[i])
        #         filename=os.listdir(dir)
        #         path=os.path.join(dir, 'LiDAR_PointCloud_vehicles_dims.txt')
        #         if(inv == 0):
        #             if((folder_num[i]%2 != 0)):
        #                 try:
        #                     shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]))
        #                 except OSError:
        #                     shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
        #                     shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
        #             else:
        #                 file_stats = os.stat(path)
        #                 if (file_stats.st_size == 0):
        #                     try:
        #                         shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]))
        #                     except OSError:
        #                         shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
        #                         shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)


        #         else:
        #             if((folder_num[i]%2 == 0)):
        #                 try:
        #                     shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]))
        #                 except OSError:
        #                     shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
        #                     shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
        #             else:
        #                 file_stats = os.stat(path)
        #                 if (file_stats.st_size == 0):
        #                     try:
        #                         shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]))
        #                     except OSError:
        #                         shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
        #                         shutil.rmtree(sf_dir+"/LiDAR_PointCloud"+str(folder_num[i]), ignore_errors=True)
        #     except FileNotFoundError:
        #         continue

if __name__=="__main__":
    main()