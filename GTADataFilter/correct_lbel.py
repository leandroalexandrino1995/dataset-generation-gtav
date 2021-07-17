import os

root_dir = '/home/joao/Desktop/lbl_test'

for subdir, dirs, files in os.walk(root_dir):
    for file in files:

        path=os.path.join(root_dir, file)

        # print(path)

        with open(path, "r") as f:
            lines = f.readlines()

        dc = []

        good_lines = []

        for line in lines:
            if("Dont" in line):
                dc.append(line)
            else:
                good_lines.append(line)

        with open(path, "w") as f:
            for line in good_lines:
                f.write(line)
            for line in dc:
                f.write(line)