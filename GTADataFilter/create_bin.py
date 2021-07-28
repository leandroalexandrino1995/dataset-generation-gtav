import os
import struct

root_dir = '/media/joao/My Passport/Elements/training/'

for subdir, dirs, files in os.walk(root_dir):
    for file in files:

        directory = '/media/joao/My Passport/Elements/training_velodyne/velodyne/'

        file_tmp = file

        save_file = directory + file_tmp[:-3]+"bin"

        if not os.path.isfile(save_file):

            filename = root_dir + file

            lines = []
            with open(filename) as file_in:
                for line in file_in:
                    lines.append(line)
            tmp_ply_content = lines
            tuple_list = []        

            for i in range(0, len(tmp_ply_content)):
                string_values_list = tmp_ply_content[i].rstrip().split(" ")

                try:
                    if float(string_values_list[0]):
                        string_values_list = tmp_ply_content[i].rstrip().split(" ")
                        t = ()
                        for i in range(0, len(string_values_list)):
                            t += (float(string_values_list[i]),)

                        tuple_list.append(t)
                except ValueError:
                    continue

            with open(save_file, "wb") as f:
                for point in tuple_list:
                    s = struct.pack('f'*len(point), *point)
                    f.write(s)

root_dir = '/media/joao/My Passport/Elements/testing/'

for subdir, dirs, files in os.walk(root_dir):
    for file in files:

        directory = '/media/joao/My Passport/Elements/testing_velodyne/velodyne/'

        file_tmp = file

        save_file = directory + file_tmp[:-3]+"bin"

        if not os.path.isfile(save_file):

            filename = root_dir + file

            lines = []
            with open(filename) as file_in:
                for line in file_in:
                    lines.append(line)
            tmp_ply_content = lines
            tuple_list = []        

            for i in range(0, len(tmp_ply_content)):
                string_values_list = tmp_ply_content[i].rstrip().split(" ")

                try:
                    if float(string_values_list[0]):
                        string_values_list = tmp_ply_content[i].rstrip().split(" ")
                        t = ()
                        for i in range(0, len(string_values_list)):
                            t += (float(string_values_list[i]),)

                        tuple_list.append(t)
                except ValueError:
                    continue

            with open(save_file, "wb") as f:
                for point in tuple_list:
                    s = struct.pack('f'*len(point), *point)
                    f.write(s)