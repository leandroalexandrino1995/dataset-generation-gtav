#!/bin/bash

set -e

# cd ../GTADataFilter

# python3 add_intensity_cars.py

# cd -

# python3 Main.py --gtaSamplesPath "../../PointCloudsMaterialHash" --kittiOutputPath "../../MaterialHash_int1/GTAtoKITTI/kitti/" --targetArchitecure "PointPillars"

# scp -r ../../MaterialHash_int1/GTAtoKITTI/kitti/training jgomes@192.168.91.154:/home/jgomes/OpenPCDet/data/kitti_int_car/
# scp -r ../../MaterialHash_int1/GTAtoKITTI/kitti/testing jgomes@192.168.91.154:/home/jgomes/OpenPCDet/data/kitti_int_car/

scp -r ../../MaterialHash_int1/GTAtoKITTI/kitti/testing/label_2 jgomes@192.168.91.154:/home/jgomes/OpenPCDet/data/kitti_int_car/testing/
scp -r ../../MaterialHash_int1/GTAtoKITTI/kitti/testing/velodyne jgomes@192.168.91.154:/home/jgomes/OpenPCDet/data/kitti_int_car/testing/
