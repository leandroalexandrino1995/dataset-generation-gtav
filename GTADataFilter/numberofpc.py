import os
from posixpath import expanduser
# import argparse

import shutil

def main():

    df_dir='/media/joao/Elements/WeirdTest/+PCs/'

    filename=os.listdir(df_dir)
    file_number=len(filename)

    print(file_number)

if __name__=="__main__":
    main()