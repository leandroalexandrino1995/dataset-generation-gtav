import os
from posixpath import expanduser
# import argparse

import shutil

def main():

    sf = ["PointCloudsMaterialHash_vPAI"]
    		#\"PointCloudsMaterialHash", 

#    df_dir='/media/joao/My Passport/Elements/BonsDadosComHashes-backup/AllPointClouds/'
    df_dir='/media/joao/My Passport/Elements/PointCloudsMaterialHash/'

    filename=os.listdir(df_dir)
    num=len(filename)
    
    num += 1
    
    print(num)

    for x in sf:
##        sf_dir='/media/joao/My Passport/Elements/BonsDadosComHashes-backup/'+x

        sf_dir='/media/joao/My Passport/Elements/'+x

        print(sf_dir)

        filename=os.listdir(sf_dir)

        for name in filename:

            source_dir=sf_dir+'/'+name

            dest_dir=df_dir+''+name[:16]+''+str(num)
            
            try:
                shutil.copytree(source_dir, dest_dir)
            except FileExistsError:
                print(dest_dir + " already exists")

            num += 1

if __name__=="__main__":
    main()
