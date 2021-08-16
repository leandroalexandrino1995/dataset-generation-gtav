import os
import math
import re
import numpy as np

import sys

def main():

	root_dir = '/media/joao/My Passport/Elements/PointCloudsMaterialHash_withIntensity_v2/'

	try:
		f = open("AddItensity.txt", "r")
		GTAFolder = int(f.read())
		toSave = GTAFolder
	except ValueError:
		GTAFolder = 0
		toSave = 0

	for subdir, dirs, files in os.walk(root_dir):
		dirs = sorted(dirs, key=lambda filename: int(filename.replace('LiDAR_PointCloud','')))
		for dirName in dirs[GTAFolder:]:

			try:

				x = 0

				path=os.path.join(root_dir+dirName, 'LiDAR_PointCloud_vehicles_dims.txt')

				with open(path, 'rt') as file:
					dataDims = file.readlines()

				importantData = []

				for k in dataDims:
					if "Car " in k or "Pedestrian " in k:
						toAppend = []
						if "Car " in k:
							toAppend.append("1")
						elif "Pedestrian " in k:
							toAppend.append("0")
						k = k.split()
						toAppend.append(k[12])
						toAppend.append(k[13])
						toAppend.append(k[14])
						if(float(k[-9]) > float(k[-8])):
							toAppend.append(k[-9])
						else:
							toAppend.append(k[-8])
						toAppend.append(k[0])
						importantData.append(toAppend)

				path=os.path.join(root_dir+dirName, 'LiDAR_PointCloud.ply')
				with open(path, 'rt') as file:
					data = file.readlines()

				with open(root_dir+dirName+'/LiDAR_PointCloud_temp.txt', 'w') as file:
					file.write(str(data[8:]).strip())

				path=os.path.join(root_dir+dirName, 'LiDAR_PointCloud_temp.txt')
				with open(path, 'rb') as file:
					data_aux = file.readlines()			

				# liInput = [i.split("\\n")[0] for i in data]

				# print(liInput)

				pointcloud = np.loadtxt(data_aux, dtype=bytes,delimiter='\n').astype('str')
				# pointcloud = np.nan_to_num(pointcloud, nan=0.000000)
				pointcloud = pointcloud.tolist()
				rows = pointcloud[2:-2].splitlines()
				arr = [row.replace("'","").replace("\\n","").replace(",","").replace('"',"").split() for row in rows]
				
				pointcloud = np.array(arr, dtype=np.float32).reshape(-1,4)

				x_points = pointcloud[:, 0]  # x position of point
				y_points = pointcloud[:, 1]  # y position of point
				z_points = pointcloud[:, 2]  # z position of point

				

				x_max = max(x_points)
				x_min = min(x_points)
				y_max = max(y_points)
				y_min = min(y_points)
				z_max = max(z_points)
				z_min = min(z_points)				

				path=os.path.join(root_dir+dirName, 'LiDAR_PointCloud_labels.txt')

				line_num = []

				hashes_lines = dict()

				with open(path, 'r') as file:
					for k in file.readlines():
						if (k == "0\n"):
							line_num.append(x)
						x += 1

				points = []

				path=os.path.join(root_dir+dirName, 'LiDAR_PointCloud_materialHash.txt')

				with open(path, 'r') as file:
					dataHash = file.readlines()

				appendSpot = {}

				dists = []

				for impData in importantData:

					for k in set(line_num):
						line = data[8+k]
						line = line.split()[:3]
						d = math.sqrt(math.pow(float(line[0]) - float(impData[1]), 2) + math.pow(float(line[1]) - float(impData[2]), 2) + math.pow(float(line[2]) - float(impData[3]), 2))
						dists.append(d)
						if d < float(impData[4]) and float(line[2]) <= float(impData[3]):
							points.append(k)

					# print(impData)

					rightSpot = 0

					for i in points:
						if impData[0] == '1' and (dataHash[i] == "282940568\n" or dataHash[i] == "-1301352528\n" or dataHash[i]=="1886546517\n"): #Se carro
							rightSpot += 1
						elif impData[0] == '0' and (dataHash[i] == "1187676648\n" or dataHash[i] == "359120722\n" or dataHash[i]=="1084640111\n"): #Se pessoa
							rightSpot += 1

					if(len(points) > 0):
						appendSpot[impData[-1]] = rightSpot/(len(points))
					else:
						appendSpot[impData[-1]] = 0

				hashes = []

				for x in appendSpot:
					hashes.append(x)

				path=os.path.join(root_dir+dirName, 'LiDAR_PointCloud_labelsDetailed.txt')

				lines_with_hashes = []

				for i in hashes:
					x = 0
					to_hashes_lines = []
					with open(path, 'r') as file:
						for k in file.readlines():
							if (i in k):
								to_hashes_lines.append(x)
								lines_with_hashes.append(x)
							x += 1
					try:
						hashes_lines[appendSpot[i]] = hashes_lines[appendSpot[i]] + to_hashes_lines
					except KeyError:
						hashes_lines[appendSpot[i]] = to_hashes_lines

				number_of_hashesh_lines = 0

				for z in hashes_lines:
					number_of_hashesh_lines += len(hashes_lines[z])

				if number_of_hashesh_lines != len(lines_with_hashes):
					raise Exception("Number of lines != what should be")

				path1=os.path.join(root_dir+dirName, 'LiDAR_PointCloud.ply')

				with open(path1, "r") as file:
					i = file.readlines()

				to_write = "ply\nformat ascii 1.0\nelement vertex " + str(len(lines_with_hashes)+8) + "\nproperty float x\nproperty float y\nproperty float z\nproperty float intensity\nend_header\n"
				to_write += str(x_max) + " " + str(y_max) + " " + str(z_max) + " 0\n"
				to_write += str(x_max) + " " + str(y_max) + " " + str(z_min) + " 0\n"
				to_write += str(x_max) + " " + str(y_min) + " " + str(z_max) + " 0\n"
				to_write += str(x_max) + " " + str(y_min) + " " + str(z_min) + " 0\n"
				to_write += str(x_min) + " " + str(y_max) + " " + str(z_max) + " 0\n"
				to_write += str(x_min) + " " + str(y_max) + " " + str(z_min) + " 0\n"
				to_write += str(x_min) + " " + str(y_min) + " " + str(z_max) + " 0\n"
				to_write += str(x_min) + " " + str(y_min) + " " + str(z_min) + " 0\n"

				for z in hashes_lines:
					for x in hashes_lines[z]:
						to_write += i[x+7][:-3] + " " + str(z) + "\n"

				with open(path1, "w") as file:
					# file.write("ply\nformat ascii 1.0\nelement vertex " + str(len(lines_with_hashes)+8) + "\nproperty float x\nproperty float y\nproperty float z\nproperty float intensity\nend_header\n")
					# file.write(str(x_max) + " " + str(y_max) + " " + str(z_max) + " 0\n")
					# file.write(str(x_max) + " " + str(y_max) + " " + str(z_min) + " 0\n")
					# file.write(str(x_max) + " " + str(y_min) + " " + str(z_max) + " 0\n")
					# file.write(str(x_max) + " " + str(y_min) + " " + str(z_min) + " 0\n")

					# file.write(str(x_min) + " " + str(y_max) + " " + str(z_max) + " 0\n")
					# file.write(str(x_min) + " " + str(y_max) + " " + str(z_min) + " 0\n")
					# file.write(str(x_min) + " " + str(y_min) + " " + str(z_max) + " 0\n")
					# file.write(str(x_min) + " " + str(y_min) + " " + str(z_min) + " 0\n")

					# for z in hashes_lines:
					# 	for x in hashes_lines[z]:
					# 		file.write(i[x+7][:-1] + " " + str(z) + "\n")

					file.write(to_write)

				toSave += 1
				f = open("AddItensity.txt", "w")
				f.write(str(toSave))
				f.close()

				

			except KeyboardInterrupt:
				f = open("tryAgainStands.txt", "a")
				f.write(str(toSave) + " ")
				f.close()
				sys.exit("KeyboardInterrupt")
			except Exception as e:
				print("Error occured")
				print(e)
				f = open("tryAgainStands.txt", "a")
				f.write(str(toSave) + " ")
				f.close()

	return

if __name__=="__main__":
	main()
