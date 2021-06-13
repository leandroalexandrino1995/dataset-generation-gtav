import os 

'''
	Location (inside the Frustum PointNet project) that this script must be
	located and executed in:
    frustum-pointnets-master\dataset\KITTI\object\training
'''

# Path to the directory holding the dataset's labels
rootDir = './label_2/'
rootDir = '/media/joao/Elements/Removed/GTAtoKITTI/kitti/data_object_label_2/training/label_2/'
#destination_dir = '../../../../kitti/rgb_detections/'
destination_dir = '/home/joao/Desktop/'
image_dir = './image_2/'
dest_dir = "../../../../kitti/image_sets/"

# used to generate the val.txt, test.txt or train.txt
list_sample_prefixes = []

gen_file_name = 'rgb_detection_val.txt'
gen_file_contents = ''
car_label = 2
confidence = 1

print("==== Generating Ground Truth 2D predictions ====")

sample_counter = 0
# walk through all samples in rootDir and create the kitti output accordingly
for subdir, dirs, files in os.walk(rootDir):
    for label_file in files:
        #filename = './label_2/000000.txt'
        print("filename: " + label_file)
        file_prefix = label_file.split('.')[0]
        list_sample_prefixes.append(file_prefix)

        with open(rootDir + label_file) as f:
            content = f.readlines()

        content_list = [x.strip() for x in content] 

        for label in content_list:
            label_values_list = label.split(' ')

            gen_file_contents += image_dir + file_prefix + '.png' + ' ' + str(car_label) + ' ' + str(confidence) + ' ' + label_values_list[4] + ' ' + label_values_list[5] + ' ' + label_values_list[6] + ' ' + label_values_list[7] + '\n'


filename = 'rgb_detection_val.txt'
with open(destination_dir + filename, "w") as text_file:
	text_file.write(gen_file_contents)
			
print("Output: " + destination_dir + filename)
			
# Generating val.txt, or test.txt or train.txt

filename = "val.txt"
 
print("\n\n==== Generating val.txt ====")	
print("\n\t-> Allows for the selection of samples for the validation dataset split.")

#with open(dest_dir + filename, "w") as text_file:

with open(destination_dir + filename, "w") as text_file:
	for pref in list_sample_prefixes:
		print(pref)
		text_file.write(pref + "\n")

print("\nOutput file path: " + destination_dir + filename)
print("Finished!")

